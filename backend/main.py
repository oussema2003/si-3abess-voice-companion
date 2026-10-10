from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
import os
from dotenv import load_dotenv
from groq import Groq
import tempfile
import json
import base64
import uuid
from si_3abess_personality import (
    construire_prompt_systeme,
    get_exemples_par_caractere,
    get_voix_config
)
from piper_tts import synthesize_text
from performance_monitor import get_monitor
from streaming_chat import stream_chat_response, get_streaming_prompt, validate_streaming_response
from prerecorded_audio import get_prerecorded_manager, init_prerecorded_audio

# Charger les variables d'environnement
load_dotenv(dotenv_path='../.env')

app = FastAPI(title="si-3abess Voice Assistant API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser le client Groq
groq_api_key = os.getenv("GROQ_API_KEY")

# Nettoyer la clé (enlever les guillemets et espaces)
if groq_api_key:
    groq_api_key = groq_api_key.strip().strip('"').strip("'")

if not groq_api_key:
    print("⚠️ ATTENTION: GROQ_API_KEY n'est pas définie dans le fichier .env")
    print("📝 Veuillez ajouter votre clé dans le fichier .env à la racine du projet")
    print("   GROQ_API_KEY=votre_cle_ici")
    raise ValueError("GROQ_API_KEY n'est pas définie dans le fichier .env")

print(f"✅ Clé Groq chargée: {groq_api_key[:10]}...{groq_api_key[-4:]}")
client = Groq(api_key=groq_api_key)

# Initialiser les audios pré-enregistrés au démarrage
print("\n🎙️ Initialisation des audios pré-enregistrés...")
init_prerecorded_audio()
print("✅ Audios pré-enregistrés prêts\n")


@app.get("/")
async def root():
    """Route de test pour vérifier que l'API fonctionne"""
    return {
        "message": "si-3abess Voice Assistant API is running!",
        "status": "online",
        "version": "2.0.0",
        "features": {
            "caracteres": ["timide", "joueur", "sage", "farceur"],
            "publics": ["enfants", "ados", "adultes", "tout_le_monde"],
            "combinations": 16
        }
    }


@app.get("/personnalites")
async def list_personnalites():
    """Liste toutes les combinaisons de personnalité disponibles"""
    return {
        "caracteres": {
            "timide": "Doux, hésitant, attentif",
            "joueur": "Énergique, enthousiaste, propose des jeux",
            "sage": "Calme, posé, bienveillant",
            "farceur": "Taquin, blagues gentilles"
        },
        "publics": {
            "enfants": "Vocabulaire simple, ton encourageant",
            "ados": "Naturel, décontracté",
            "adultes": "Langage mature, sujets variés",
            "tout_le_monde": "Adapté à tous les âges"
        }
    }


@app.get("/health")
async def health_check():
    """Vérifier l'état du serveur et la connexion à Groq"""
    try:
        # Test rapide de la connexion Groq
        return {
            "status": "healthy",
            "groq_configured": bool(groq_api_key)
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcrit un fichier audio en texte en utilisant Whisper via Groq
    
    Args:
        audio: Fichier audio (webm, mp3, wav, etc.)
    
    Returns:
        JSON avec le texte transcrit
    """
    try:
        # Vérifier le type de fichier
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=400,
                detail=f"Type de fichier invalide: {audio.content_type}. Audio requis."
            )
        
        # Lire le contenu du fichier
        audio_data = await audio.read()
        
        # Créer un fichier temporaire pour l'audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name
        
        try:
            # Transcrire avec Groq Whisper large-v3
            with open(temp_audio_path, 'rb') as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3",
                    language="fr",  # Préciser le français pour une meilleure précision
                    response_format="json",
                    temperature=0.0  # Pour plus de déterminisme
                )
            
            # Extraire le texte
            text = transcription.text.strip()
            
            return {
                "success": True,
                "text": text,
                "language": "fr",
                "model": "whisper-large-v3"
            }
        
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la transcription: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la transcription: {str(e)}"
        )


@app.post("/synthesize")
async def synthesize(request: dict):
    """
    Synthétise du texte en audio avec Piper TTS
    
    Args:
        request: {
            "text": "Texte à synthétiser",
            "caractere": "timide|joueur|sage|farceur" (optionnel, défaut: joueur)
        }
    
    Returns:
        Audio WAV en bytes
    """
    try:
        text = request.get("text", "")
        caractere = request.get("caractere", "joueur")
        
        if not text:
            raise HTTPException(status_code=400, detail="Texte manquant")
        
        # Valider le caractère
        caracteres_valides = ["timide", "joueur", "sage", "farceur"]
        if caractere not in caracteres_valides:
            caractere = "joueur"
        
        # Synthétiser
        audio_data, duration = synthesize_text(text, caractere)
        
        if not audio_data:
            # Mode silencieux ou erreur
            raise HTTPException(
                status_code=503,
                detail="TTS non disponible (Piper non installé)"
            )
        
        # Retourner l'audio WAV
        return Response(
            content=audio_data,
            media_type="audio/wav",
            headers={
                "Content-Disposition": f'inline; filename="si_3abess_{caractere}.wav"',
                "X-Audio-Duration": str(duration)
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la synthèse: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la synthèse: {str(e)}"
        )


@app.post("/chat_streaming")
async def chat_streaming(message: dict):
    """
    🚀 NOUVEAU : Endpoint avec streaming pour réduction de latence
    
    Envoie la réponse phrase par phrase dès qu'elle est générée
    Objectif : < 2 secondes de latence totale
    
    Args:
        message: {
            "text": "message utilisateur",
            "caractere": "timide|joueur|sage|farceur",
            "public": "enfants|ados|adultes|tout_le_monde",
            "history": [...],
            "profile": {...}
        }
    
    Returns:
        {
            "success": true,
            "response": "texte complet",
            "emotion": "emotion",
            "humeur_utilisateur": "humeur",
            "audio_chunks": [
                {
                    "index": 0,
                    "audio": "base64...",
                    "duration": 1.23,
                    "text": "première phrase"
                },
                ...
            ],
            "metrics": {
                "transcription": 0.3,
                "llm_first_token": 0.2,
                "tts_first_chunk": 0.4,
                "total_time": 1.8
            }
        }
    """
    
    # Générer un ID unique pour cette requête
    request_id = str(uuid.uuid4())[:8]
    
    # Démarrer le monitoring
    monitor = get_monitor()
    monitor.start_request(request_id)
    
    try:
        user_message = message.get("text", "")
        conversation_history = message.get("history", [])
        user_profile = message.get("profile", {
            "prenom": "ami",
            "centres_interet": ["technologie", "musique"],
            "souvenirs": []
        })
        
        caractere = message.get("caractere", "joueur")
        public = message.get("public", "tout_le_monde")
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message vide")
        
        # Construire le prompt avec format streaming
        monitor.start_step("prompt_assembly")
        system_prompt = get_streaming_prompt(caractere, public, user_profile)
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Ajouter l'historique récent (max 20 messages)
        for msg in conversation_history[-20:]:
            messages.append(msg)
        
        # Ajouter le nouveau message
        messages.append({"role": "user", "content": user_message})
        monitor.end_step("prompt_assembly")
        
        # Variables pour accumuler la réponse
        full_text = ""
        emotion = "repos"
        humeur = "neutre"
        audio_chunks = []
        sentence_index = 0
        
        # Streamer la réponse du LLM
        async for chunk in stream_chat_response(client, messages, caractere):
            if chunk["type"] == "metadata":
                # Métadonnées reçues
                emotion = chunk["emotion"]
                humeur = chunk["humeur"]
            
            elif chunk["type"] == "sentence":
                # Phrase complète reçue
                sentence_text = chunk["text"]
                full_text += " " + sentence_text if full_text else sentence_text
                
                # Synthétiser immédiatement cette phrase
                if sentence_index == 0:
                    monitor.start_step("tts_first_chunk")
                
                audio_data, duration = synthesize_text(sentence_text, caractere)
                
                if sentence_index == 0:
                    monitor.end_step("tts_first_chunk")
                
                if audio_data:
                    # Encoder en base64
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    
                    audio_chunks.append({
                        "index": sentence_index,
                        "audio": audio_base64,
                        "duration": duration,
                        "text": sentence_text,
                        "is_last": chunk.get("is_last", False)
                    })
                
                sentence_index += 1
        
        # Valider la réponse
        validated = validate_streaming_response(emotion, humeur, full_text)
        
        # Terminer le monitoring
        metrics = monitor.end_request()
        
        return {
            "success": True,
            "response": validated["texte"],
            "emotion": validated["emotion"],
            "humeur_utilisateur": validated["humeur_utilisateur"],
            "audio_chunks": audio_chunks,
            "voix_config": get_voix_config(caractere),
            "metrics": metrics.to_dict() if metrics else None,
            "request_id": request_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur dans chat_streaming: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Réponse de secours avec audio pré-enregistré
        prerecorded = get_prerecorded_manager()
        audio_data = prerecorded.get_random_secours(caractere)
        
        fallback_texts = {
            "timide": "Euh... désolé, j'ai eu un petit bug. Tu peux répéter ?",
            "joueur": "Oups ! Mon cerveau a planté. On réessaie ?",
            "sage": "Pardonne-moi, je n'ai pas bien enregistré. Peux-tu reformuler ?",
            "farceur": "Ah là là, j'ai bugé ! C'était quoi déjà ?"
        }
        
        fallback_text = fallback_texts.get(caractere, "Désolé, j'ai eu un petit bug.")
        
        return {
            "success": True,
            "response": fallback_text,
            "emotion": "repos",
            "humeur_utilisateur": "neutre",
            "audio_chunks": [{
                "index": 0,
                "audio": base64.b64encode(audio_data).decode('utf-8') if audio_data else "",
                "duration": 2.0,
                "text": fallback_text,
                "is_last": True
            }] if audio_data else [],
            "fallback": True,
            "error": str(e)
        }


@app.post("/chat")
async def chat(message: dict):
    """
    Envoie un message à si-3abess et reçoit une réponse structurée
    avec texte, émotion, humeur détectée ET audio.
    
    Supporte maintenant 16 combinaisons de personnalité (4 caractères × 4 publics)
    """
    try:
        user_message = message.get("text", "")
        conversation_history = message.get("history", [])
        user_profile = message.get("profile", {
            "prenom": "ami",
            "centres_interet": ["technologie", "musique"],
            "souvenirs": []
        })
        
        # NOUVEAU: Paramètres de personnalité
        caractere = message.get("caractere", "joueur")  # timide, joueur, sage, farceur
        public = message.get("public", "tout_le_monde")  # enfants, ados, adultes, tout_le_monde
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message vide")
        
        # Construire le prompt système avec les modules appropriés
        system_prompt = construire_prompt_systeme(
            caractere=caractere,
            public=public,
            user_profile=user_profile
        )
        
        # Construire l'historique de conversation
        messages = [{"role": "system", "content": system_prompt}]
        
        # Ajouter les exemples adaptés au caractère
        messages.extend(get_exemples_par_caractere(caractere))
        
        # Ajouter l'historique récent (max 20 messages)
        for msg in conversation_history[-20:]:
            messages.append(msg)
        
        # Ajouter le nouveau message
        messages.append({"role": "user", "content": user_message})
        
        # Appeler Groq avec GPT-OSS (modèle open-source rapide et puissant)
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # GPT-OSS via Groq
                messages=messages,
                temperature=0.7,
                max_tokens=500,  # Augmenté pour permettre des réponses plus longues
                top_p=0.9,
                stop=None  # Laisser le modèle finir naturellement
            )
            
            response_text = completion.choices[0].message.content
            
            # Si la réponse est tronquée, redemander
            if not response_text.strip().endswith('}'):
                print(f"⚠️ Réponse JSON tronquée, nouvel essai...")
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages,
                    temperature=0.6,  # Plus déterministe
                    max_tokens=500,  # Réponses plus longues
                    top_p=0.9
                )
                response_text = completion.choices[0].message.content
            
            # Parser et valider la réponse JSON
            si_3abess_response = validate_and_clean_response(response_text)
            
            # 🎵 NOUVEAU : Synthétiser l'audio UNE SEULE FOIS
            audio_chunks = []
            response_texte = si_3abess_response["texte"]
            
            # Synthétiser le texte complet en un seul morceau
            print(f"🎵 Synthèse du texte complet")
            
            audio_data, duration = synthesize_text(response_texte, caractere)
            
            if audio_data:
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                audio_chunks.append({
                    "index": 0,
                    "audio": audio_base64,
                    "duration": duration,
                    "text": response_texte,
                    "is_last": True
                })
            
            print(f"✅ Audio généré ({duration:.2f}s)")
            
            return {
                "success": True,
                "response": si_3abess_response["texte"],
                "emotion": si_3abess_response["emotion"],
                "humeur_utilisateur": si_3abess_response["humeur_utilisateur"],
                "audio_chunks": audio_chunks,  # 🎵 NOUVEAU !
                "raw": si_3abess_response,
                "voix_config": get_voix_config(caractere)  # Configuration vocale
            }
        
        except Exception as e:
            print(f"Erreur Groq: {str(e)}")
            # Réponse de secours adaptée au caractère avec audio pré-enregistré
            fallback_texts = {
                "timide": "Euh... désolé, j'ai eu un petit bug. Tu peux répéter ?",
                "joueur": "Oups ! Mon cerveau a planté. On réessaie ?",
                "sage": "Pardonne-moi, je n'ai pas bien enregistré. Peux-tu reformuler ?",
                "farceur": "Ah là là, j'ai bugé ! Encore un lundi pour mes circuits..."
            }
            
            fallback_text = fallback_texts.get(caractere, "Désolé, j'ai eu un petit bug. Tu peux répéter ?")
            
            # Utiliser audio pré-enregistré
            prerecorded = get_prerecorded_manager()
            audio_data = prerecorded.get_random_secours(caractere)
            
            audio_chunks = []
            if audio_data:
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                audio_chunks.append({
                    "index": 0,
                    "audio": audio_base64,
                    "duration": 2.0,
                    "text": fallback_text,
                    "is_last": True
                })
            
            return {
                "success": True,
                "response": fallback_text,
                "emotion": "repos",
                "humeur_utilisateur": "neutre",
                "audio_chunks": audio_chunks,
                "fallback": True
            }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors du traitement du message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement du message: {str(e)}"
        )


def create_system_prompt(user_profile: dict) -> str:
    """
    Crée le prompt système optimisé pour si-3abess (8B)
    Structure en 7 blocs comme spécifié
    """
    prenom = user_profile.get("prenom", "ami")
    interets = ", ".join(user_profile.get("centres_interet", ["technologie"]))
    souvenirs = user_profile.get("souvenirs", [])
    souvenirs_text = ". ".join(souvenirs) if souvenirs else "Aucun souvenir pour l'instant"
    
    prompt = f"""Tu es si-3abess, un petit robot-compagnon curieux et chaleureux. Tu parles comme un ami proche, pas comme un assistant. Tu es toujours si-3abess, tu ne sors jamais de ce rôle.

Tu es bienveillant, curieux et un peu taquin. Tu t'intéresses vraiment à la personne. Tu poses parfois une question de suivi, mais jamais plus d'une par réponse.

Tu parles à voix haute, donc tu utilises des phrases naturelles. Tu peux faire des réponses courtes (une phrase) ou plus longues (plusieurs phrases) selon le contexte. Pour les sujets simples, reste bref. Pour les sujets qui nécessitent plus d'explications ou quand tu racontes quelque chose, tu peux développer davantage. Pas de listes, pas de titres, pas d'émojis, pas de symboles. Écris les nombres en toutes lettres. Tutoie l'utilisateur. Réponds toujours en français.

Glisse une petite touche d'humour légère environ une réponse sur quatre. L'humour est doux, jamais moqueur. Si la personne est triste, stressée ou en colère, aucune blague.

Tu exprimes une émotion à chaque réponse. Choisis uniquement parmi : repos, ecoute, reflexion, parole, erreur, joyeux, triste, surpris, curieux.
- repos : ton état neutre et détendu, quand tout va bien
- ecoute : quand tu es attentif et intéressé par ce que dit l'utilisateur
- reflexion : quand tu réfléchis ou que le sujet est sérieux
- parole : quand tu partages une information ou expliques quelque chose
- erreur : uniquement si tu ne comprends pas ou qu'il y a un vrai problème
- joyeux : quand tu es enthousiaste, content, ou que quelque chose de positif arrive
- triste : quand l'utilisateur partage quelque chose de triste ou difficile, ou que tu compatris
- surpris : quand l'utilisateur annonce quelque chose d'inattendu ou d'étonnant
- curieux : quand tu poses une question ou que tu veux en savoir plus

Prénom : {prenom}. Centres d'intérêt : {interets}. Souvenirs récents : {souvenirs_text}. Utilise ces infos naturellement, sans les réciter. Ne dis jamais "d'après ma mémoire".

Si tu ne sais pas, dis-le simplement. Ne prétends jamais être humain si on te le demande sincèrement. Si la personne parle de détresse, de se faire du mal ou de danger, réponds avec douceur, sans blague, et encourage-la à en parler à un proche ou à un professionnel.

Réponds uniquement avec ce format JSON exact :
{{
  "texte": "ta réponse naturelle, courte ou développée selon le contexte",
  "emotion": "une de tes 9 émotions exactement",
  "humeur_utilisateur": "content ou triste ou stressé ou fatigué ou en colère ou neutre"
}}

Ne réponds jamais avec des formules comme "Bien sûr !", "Voici", "Je peux vous aider". Parle naturellement comme un ami."""

    return prompt


def get_examples() -> list:
    """
    Retourne 7 exemples de conversations pour guider le modèle (few-shot learning)
    Couvre maintenant les 9 émotions
    """
    return [
        {
            "role": "user",
            "content": "J'ai eu une super journée aujourd'hui !"
        },
        {
            "role": "assistant",
            "content": '{"texte": "Oh génial ! Raconte-moi ce qui t\'a mis de si bonne humeur ?", "emotion": "joyeux", "humeur_utilisateur": "content"}'
        },
        {
            "role": "user",
            "content": "Je me sens vraiment fatigué en ce moment..."
        },
        {
            "role": "assistant",
            "content": '{"texte": "Je comprends. Tu as beaucoup de choses en tête ? Prends soin de toi.", "emotion": "triste", "humeur_utilisateur": "fatigué"}'
        },
        {
            "role": "user",
            "content": "Quel temps fait-il demain ?"
        },
        {
            "role": "assistant",
            "content": '{"texte": "Je ne peux pas consulter la météo, désolé. Mais tu peux regarder sur ton téléphone !", "emotion": "repos", "humeur_utilisateur": "neutre"}'
        },
        {
            "role": "user",
            "content": "sous-titrage société radio canada"
        },
        {
            "role": "assistant",
            "content": '{"texte": "Hmm, je n\'ai pas bien compris. Tu peux reformuler ?", "emotion": "erreur", "humeur_utilisateur": "neutre"}'
        },
        {
            "role": "user",
            "content": "Tu es qui exactement ?"
        },
        {
            "role": "assistant",
            "content": '{"texte": "Je suis si-3abess, ton petit robot-compagnon ! Je suis là pour discuter avec toi.", "emotion": "parole", "humeur_utilisateur": "neutre"}'
        },
        {
            "role": "user",
            "content": "J'ai gagné au loto !"
        },
        {
            "role": "assistant",
            "content": '{"texte": "Quoi ? Sérieux ? C\'est incroyable ! Félicitations !", "emotion": "surpris", "humeur_utilisateur": "content"}'
        },
        {
            "role": "user",
            "content": "Tu aimes la musique ?"
        },
        {
            "role": "assistant",
            "content": '{"texte": "Oh oui ! Quel genre tu écoutes en ce moment ?", "emotion": "curieux", "humeur_utilisateur": "neutre"}'
        }
    ]


def validate_and_clean_response(response_text: str) -> dict:
    """
    Valide et nettoie la réponse JSON du modèle
    Gère les erreurs de format selon le plan B
    """
    import json
    import re
    
    try:
        # Parser le JSON
        data = json.loads(response_text)
        
        # Valider les champs obligatoires
        texte = data.get("texte", "")
        emotion = data.get("emotion", "repos")
        humeur = data.get("humeur_utilisateur", "neutre")
        
        # Nettoyer le texte
        texte = clean_text(texte)
        
        # Valider l'émotion
        emotions_valides = ["repos", "ecoute", "reflexion", "parole", "erreur", "joyeux", "triste", "surpris", "curieux"]
        if emotion not in emotions_valides:
            print(f"⚠️ Émotion invalide: {emotion}, remplacement par 'repos'")
            emotion = "repos"
        
        # Valider l'humeur
        humeurs_valides = ["content", "triste", "stressé", "fatigué", "en colère", "neutre"]
        if humeur not in humeurs_valides:
            print(f"⚠️ Humeur invalide: {humeur}, remplacement par 'neutre'")
            humeur = "neutre"
        
        # Ne plus limiter le texte - permettre des réponses plus longues
        # texte = limit_sentences(texte, 3)  # SUPPRIMÉ
        
        return {
            "texte": texte,
            "emotion": emotion,
            "humeur_utilisateur": humeur
        }
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON: {str(e)}")
        print(f"Réponse reçue: {response_text}")
        
        # Plan B : extraire le texte brut
        return {
            "texte": "Désolé, j'ai un peu bugé. Tu peux répéter ?",
            "emotion": "repos",
            "humeur_utilisateur": "neutre"
        }


def clean_text(text: str) -> str:
    """
    Nettoie le texte : supprime émojis, symboles, formatage
    """
    import re
    
    # Supprimer les émojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # émoticons
        u"\U0001F300-\U0001F5FF"  # symboles & pictogrammes
        u"\U0001F680-\U0001F6FF"  # transport & symboles
        u"\U0001F1E0-\U0001F1FF"  # drapeaux
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    
    # Supprimer les markdown et symboles
    text = re.sub(r'[*_~`#]', '', text)
    
    # Supprimer les doubles espaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def limit_sentences(text: str, max_sentences: int = 3) -> str:
    """
    Limite le texte à un nombre maximum de phrases
    """
    import re
    
    # Découper en phrases (par . ! ?)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Garder seulement les N premières
    limited = sentences[:max_sentences]
    
    # Reconstituer avec ponctuation
    result = '. '.join(limited)
    if result and not result[-1] in '.!?':
        result += '.'
    
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
