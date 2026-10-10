"""
🚀 Chat avec streaming et découpe en phrases pour réduction de latence
"""

import json
import re
from typing import AsyncGenerator, Dict, List, Optional
from groq import Groq
from performance_monitor import get_monitor


def split_into_sentences(text: str) -> List[str]:
    """
    Découpe le texte en phrases
    Retourne une liste de phrases complètes
    """
    # Protéger les abréviations
    text = text.replace("M.", "M§")
    text = text.replace("Mme", "Mme§")
    text = text.replace("Dr.", "Dr§")
    text = text.replace("etc.", "etc§")
    
    # Découper sur les ponctuations fortes
    sentences = re.split(r'([.!?]+\s+)', text)
    
    # Reconstituer les phrases avec leur ponctuation
    phrases = []
    i = 0
    while i < len(sentences):
        if sentences[i].strip():
            phrase = sentences[i]
            # Ajouter la ponctuation si elle existe
            if i + 1 < len(sentences):
                phrase += sentences[i + 1]
                i += 2
            else:
                i += 1
            
            # Restaurer les abréviations
            phrase = phrase.replace("§", ".")
            phrase = phrase.strip()
            
            if phrase:
                phrases.append(phrase)
        else:
            i += 1
    
    return phrases


def parse_streaming_response(text: str) -> Optional[Dict]:
    """
    Parse la réponse streaming du LLM
    Format attendu :
    EMOTION: joyeux | HUMEUR: content
    Texte de la réponse ici.
    """
    lines = text.strip().split('\n', 1)
    
    # Par défaut
    emotion = "repos"
    humeur = "neutre"
    texte = text.strip()
    
    # Vérifier si la première ligne contient les métadonnées
    if lines and ('EMOTION:' in lines[0] or 'HUMEUR:' in lines[0]):
        header = lines[0]
        texte = lines[1] if len(lines) > 1 else ""
        
        # Extraire émotion
        emotion_match = re.search(r'EMOTION:\s*(\w+)', header)
        if emotion_match:
            emotion = emotion_match.group(1).lower()
        
        # Extraire humeur
        humeur_match = re.search(r'HUMEUR:\s*([\w\s]+?)(?:\||$)', header)
        if humeur_match:
            humeur = humeur_match.group(1).strip().lower()
    
    return {
        "texte": texte.strip(),
        "emotion": emotion,
        "humeur_utilisateur": humeur
    }


async def stream_chat_response(
    client: Groq,
    messages: List[Dict],
    caractere: str = "joueur"
) -> AsyncGenerator[Dict, None]:
    """
    Streame la réponse du chat phrase par phrase
    
    Yields:
        dict avec:
        - type: "metadata" | "sentence"
        - emotion: str (pour metadata)
        - humeur: str (pour metadata)
        - text: str (pour sentence)
        - is_last: bool
    """
    
    monitor = get_monitor()
    monitor.start_step("llm_first_token")
    
    accumulated = ""
    first_token_received = False
    metadata_sent = False
    sentence_buffer = ""
    
    try:
        # Streaming du LLM
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=500,  # Augmenté pour permettre des discours plus longs
            stream=True
        )
        
        for chunk in stream:
            if not chunk.choices:
                continue
            
            delta = chunk.choices[0].delta
            
            if not delta.content:
                continue
            
            content = delta.content
            accumulated += content
            
            # Premier token reçu
            if not first_token_received:
                first_token_received = True
                monitor.end_step("llm_first_token")
                monitor.start_step("llm_first_sentence")
            
            # Ajouter au buffer de phrase
            sentence_buffer += content
            
            # Vérifier si on a les métadonnées (première ligne)
            if not metadata_sent and '\n' in accumulated:
                first_line = accumulated.split('\n')[0]
                if 'EMOTION:' in first_line or 'HUMEUR:' in first_line:
                    # Parser les métadonnées
                    parsed = parse_streaming_response(accumulated)
                    yield {
                        "type": "metadata",
                        "emotion": parsed["emotion"],
                        "humeur": parsed["humeur_utilisateur"]
                    }
                    metadata_sent = True
                    # Réinitialiser le buffer de phrase
                    sentence_buffer = parsed["texte"]
                    accumulated = first_line + "\n" + parsed["texte"]
            
            # Détecter la fin d'une phrase
            if re.search(r'[.!?]\s*$', sentence_buffer.strip()):
                # Phrase complète !
                sentence = sentence_buffer.strip()
                
                if sentence:
                    yield {
                        "type": "sentence",
                        "text": sentence,
                        "is_last": False
                    }
                    
                    # Mesure de la première phrase
                    if monitor.current_metrics and not monitor.current_metrics.llm_first_sentence:
                        monitor.end_step("llm_first_sentence")
                
                # Réinitialiser le buffer
                sentence_buffer = ""
        
        # Envoyer la dernière phrase si elle existe
        if sentence_buffer.strip():
            yield {
                "type": "sentence",
                "text": sentence_buffer.strip(),
                "is_last": True
            }
        
        # Si pas de métadonnées envoyées, parser la réponse complète
        if not metadata_sent:
            parsed = parse_streaming_response(accumulated)
            yield {
                "type": "metadata",
                "emotion": parsed["emotion"],
                "humeur": parsed["humeur_utilisateur"]
            }
    
    except Exception as e:
        print(f"❌ Erreur streaming: {e}")
        # Envoyer une réponse de secours
        yield {
            "type": "metadata",
            "emotion": "repos",
            "humeur": "neutre"
        }
        yield {
            "type": "sentence",
            "text": "Désolé, j'ai eu un petit bug.",
            "is_last": True
        }


def get_streaming_prompt(caractere: str, public: str, user_profile: Dict) -> str:
    """
    Crée le prompt système pour le mode streaming
    Format : EMOTION: xxx | HUMEUR: xxx
    Puis le texte
    """
    
    # Descriptions des caractères
    caractere_desc = {
        "timide": "doux, hésitant et attentif",
        "joueur": "énergique, enthousiaste et propose des activités",
        "sage": "calme, posé et bienveillant",
        "farceur": "taquin avec des blagues gentilles"
    }
    
    # Descriptions des publics
    public_desc = {
        "enfants": "Utilise un vocabulaire simple et un ton encourageant.",
        "ados": "Parle naturellement, de façon décontractée.",
        "adultes": "Utilise un langage mature et aborde des sujets variés.",
        "tout_le_monde": "Adapte-toi à tous les âges."
    }
    
    prenom = user_profile.get("prenom", "ami")
    
    prompt = f"""Tu es si-3abess, un robot-compagnon {caractere_desc.get(caractere, "amical")}. {public_desc.get(public, "")}

IMPORTANT : Ta réponse doit commencer par une ligne de métadonnées, puis le texte.

Format exact :
EMOTION: [une émotion] | HUMEUR: [humeur détectée]
[Ton texte ici - peut être court ou développé selon le contexte]

Émotions possibles : repos, ecoute, reflexion, parole, erreur, joyeux, triste, surpris, curieux
Humeurs possibles : content, triste, stressé, fatigué, en colère, neutre

Règles :
- Parle naturellement comme un ami
- Pour les questions simples : réponds brièvement (1-2 phrases)
- Pour les sujets qui nécessitent des explications ou quand tu racontes quelque chose : développe davantage (plusieurs phrases)
- Utilise un débit de parole lent et naturel
- Pas de listes, titres, émojis
- Tutoie l'utilisateur
- Prénom : {prenom}

Exemple réponse courte :
EMOTION: joyeux | HUMEUR: content
Oh super ! Raconte-moi tout !

Exemple réponse développée :
EMOTION: parole | HUMEUR: neutre
Les robots comme moi fonctionnent grâce à des circuits électroniques et des programmes. C'est un peu comme un cerveau, mais en version digitale. On peut apprendre, se souvenir de choses, et discuter avec toi. C'est fascinant, tu ne trouves pas ?"""
    
    return prompt


def validate_streaming_response(emotion: str, humeur: str, texte: str) -> Dict:
    """Valide et nettoie la réponse streaming"""
    
    # Émotions valides
    emotions_valides = ["repos", "ecoute", "reflexion", "parole", "erreur", 
                        "joyeux", "triste", "surpris", "curieux"]
    if emotion not in emotions_valides:
        emotion = "repos"
    
    # Humeurs valides
    humeurs_valides = ["content", "triste", "stressé", "fatigué", "en colère", "neutre"]
    if humeur not in humeurs_valides:
        humeur = "neutre"
    
    # Nettoyer le texte
    import re
    # Supprimer émojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    texte = emoji_pattern.sub('', texte)
    
    # Supprimer markdown
    texte = re.sub(r'[*_~`#]', '', texte)
    texte = re.sub(r'\s+', ' ', texte).strip()
    
    return {
        "texte": texte,
        "emotion": emotion,
        "humeur_utilisateur": humeur
    }
