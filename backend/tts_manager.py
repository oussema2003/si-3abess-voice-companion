"""
Gestionnaire TTS (Text-to-Speech) pour si-3abess avec Piper
Gère la synthèse vocale adaptée à chaque caractère
"""

import os
import re
import wave
import io
from pathlib import Path
from typing import List, Tuple, Dict, AsyncGenerator
import asyncio
import json
import tempfile
import hashlib

try:
    from piper import PiperVoice
    PIPER_AVAILABLE = True
except ImportError:
    print("⚠️ Piper non disponible. Installez avec: pip install piper-tts")
    PIPER_AVAILABLE = False


# ============================================================================
# CONFIGURATION DES VOIX PAR CARACTÈRE
# ============================================================================

VOIX_CONFIG = {
    "timide": {
        "voice_model": "fr_FR-siwis-medium",
        "speed": 0.9,
        "volume": 0.8,
        "pause_between_sentences": 0.3
    },
    "joueur": {
        "voice_model": "fr_FR-siwis-medium",  # Utiliser siwis en attendant upmc
        "speed": 1.2,
        "volume": 1.0,
        "pause_between_sentences": 0.2
    },
    "sage": {
        "voice_model": "fr_FR-siwis-medium",
        "speed": 0.85,
        "volume": 0.95,
        "pause_between_sentences": 0.4
    },
    "farceur": {
        "voice_model": "fr_FR-siwis-medium",  # Utiliser siwis en attendant upmc
        "speed": 1.1,
        "volume": 1.0,
        "pause_between_sentences": 0.25
    }
}


# ============================================================================
# DICTIONNAIRE DE PRONONCIATION
# ============================================================================

DICTIONNAIRE_PRONONCIATION = {
    # Noms et marques
    "si-3abess": "si-3abess",
    "Groq": "Grok",
    "Whisper": "Ouispeur",
    "ChatGPT": "Chat G P T",
    
    # Abréviations courantes
    "M.": "Monsieur",
    "Mme": "Madame",
    "Dr.": "Docteur",
    "etc.": "et cetera",
    "ex.": "exemple",
    "cf.": "confer",
    
    # Sigles
    "SMS": "S M S",
    "USA": "U S A",
    "PDF": "P D F",
    "HTML": "H T M L",
    "API": "A P I",
    
    # Nombres et unités
    "kg": "kilogrammes",
    "km": "kilomètres",
    "m²": "mètres carrés",
    "°C": "degrés Celsius"
}


# ============================================================================
# PHRASES PRÉ-ENREGISTRÉES
# ============================================================================

PHRASES_SECOURS = {
    "timide": [
        "Euh... désolé, j'ai eu un petit bug. Tu peux répéter ?",
        "Oh... je n'ai pas bien compris.",
        "Pardon, tu peux reformuler ?"
    ],
    "joueur": [
        "Oups ! Mon cerveau a planté. On réessaie ?",
        "Ah zut, j'ai bugé ! Encore ?",
        "Problème technique ! Tu peux répéter ?"
    ],
    "sage": [
        "Pardonne-moi, je n'ai pas bien enregistré. Peux-tu reformuler ?",
        "Je n'ai pas saisi. Peux-tu répéter calmement ?",
        "Excuse-moi, peux-tu redire cela ?"
    ],
    "farceur": [
        "Ah là là, j'ai bugé ! Encore un lundi pour mes circuits...",
        "Oups, court-circuit ! C'était quoi déjà ?",
        "Bug détecté ! Mais on va y arriver, redis-moi ça !"
    ]
}

MESSAGES_ACCUEIL = {
    "timide": "Euh... bonjour. Je suis si-3abess.",
    "joueur": "Salut ! Je suis si-3abess, ton robot-compagnon !",
    "sage": "Bonjour à toi. Je m'appelle si-3abess.",
    "farceur": "Hey ! Moi c'est si-3abess, prêt pour l'aventure ?"
}


# ============================================================================
# NETTOYAGE DU TEXTE
# ============================================================================

def nettoyer_texte_pour_tts(texte: str) -> str:
    """
    Nettoie le texte avant la synthèse vocale
    - Remplace les abréviations
    - Convertit les nombres
    - Supprime les symboles problématiques
    """
    
    # Appliquer le dictionnaire de prononciation
    for mot, remplacement in DICTIONNAIRE_PRONONCIATION.items():
        # Utiliser des limites de mots pour éviter les remplacements partiels
        texte = re.sub(r'\b' + re.escape(mot) + r'\b', remplacement, texte, flags=re.IGNORECASE)
    
    # Convertir les nombres (basique, peut être amélioré)
    # Exemple: "3" -> "trois"
    nombres = {
        "0": "zéro", "1": "un", "2": "deux", "3": "trois", "4": "quatre",
        "5": "cinq", "6": "six", "7": "sept", "8": "huit", "9": "neuf",
        "10": "dix", "11": "onze", "12": "douze", "13": "treize", "14": "quatorze",
        "15": "quinze", "16": "seize", "17": "dix-sept", "18": "dix-huit", "19": "dix-neuf",
        "20": "vingt", "30": "trente", "40": "quarante", "50": "cinquante",
        "60": "soixante", "70": "soixante-dix", "80": "quatre-vingts", "90": "quatre-vingt-dix",
        "100": "cent", "1000": "mille"
    }
    
    # Remplacer les nombres simples
    for num, mot in nombres.items():
        texte = re.sub(r'\b' + num + r'\b', mot, texte)
    
    # Supprimer les émojis (déjà fait normalement)
    texte = re.sub(r'[😀-🙏🌀-🗿🚀-🛿]', '', texte)
    
    # Gérer les majuscules complètes (éviter l'épellation)
    # Garder la première lettre en majuscule
    def lower_all_caps(match):
        word = match.group(0)
        if len(word) > 2:  # Seulement pour les mots de plus de 2 lettres
            return word.capitalize()
        return word
    
    texte = re.sub(r'\b[A-Z]{2,}\b', lower_all_caps, texte)
    
    # Simplifier la ponctuation
    texte = re.sub(r'\.{3,}', '...', texte)  # Limiter les points de suspension
    texte = re.sub(r'["""«»]', '"', texte)  # Normaliser les guillemets
    texte = re.sub(r'[\[\](){}]', '', texte)  # Supprimer les parenthèses
    
    # Nettoyer les espaces multiples
    texte = re.sub(r'\s+', ' ', texte)
    
    return texte.strip()


# ============================================================================
# DÉCOUPE EN PHRASES
# ============================================================================

def decouper_en_phrases(texte: str) -> List[str]:
    """
    Découpe le texte en phrases pour la synthèse progressive
    - Sépare sur . ! ?
    - Regroupe les phrases très courtes
    - Gère les cas spéciaux (M., etc.)
    """
    
    # Protéger les abréviations courantes
    texte = texte.replace("M.", "M§")
    texte = texte.replace("Mme", "Mme§")
    texte = texte.replace("Dr.", "Dr§")
    texte = texte.replace("etc.", "etc§")
    
    # Découper sur les ponctuations fortes
    phrases = re.split(r'([.!?]+)', texte)
    
    # Reconstituer les phrases avec leur ponctuation
    phrases_finales = []
    i = 0
    while i < len(phrases):
        if phrases[i].strip():
            phrase = phrases[i]
            # Ajouter la ponctuation si elle existe
            if i + 1 < len(phrases) and phrases[i + 1].strip():
                phrase += phrases[i + 1]
                i += 2
            else:
                i += 1
            
            # Restaurer les abréviations
            phrase = phrase.replace("§", ".")
            phrase = phrase.strip()
            
            if phrase:
                phrases_finales.append(phrase)
        else:
            i += 1
    
    # Regrouper les phrases très courtes (moins de 10 caractères)
    phrases_regroupees = []
    phrase_courante = ""
    
    for phrase in phrases_finales:
        if len(phrase) < 10 and phrase_courante:
            phrase_courante += " " + phrase
        else:
            if phrase_courante:
                phrases_regroupees.append(phrase_courante)
            phrase_courante = phrase
    
    if phrase_courante:
        phrases_regroupees.append(phrase_courante)
    
    # Couper les phrases très longues sur les virgules
    phrases_finales_2 = []
    for phrase in phrases_regroupees:
        if len(phrase) > 150 and ',' in phrase:
            sous_phrases = phrase.split(',')
            partie = ""
            for i, sp in enumerate(sous_phrases):
                if partie:
                    partie += ","
                partie += sp
                if len(partie) > 80 or i == len(sous_phrases) - 1:
                    phrases_finales_2.append(partie.strip())
                    partie = ""
        else:
            phrases_finales_2.append(phrase)
    
    return [p for p in phrases_finales_2 if p.strip()]


# ============================================================================
# SYNTHÈSE AVEC PIPER
# ============================================================================

class PiperTTS:
    """Gestionnaire de synthèse vocale avec Piper"""
    
    def __init__(self):
        self.piper_path = self._find_piper()
        self.models_cache = {}
        self.pre_recorded_cache = {}
    
    def _find_piper(self) -> str:
        """Trouve l'exécutable Piper"""
        # Chercher dans le PATH
        if os.name == 'nt':  # Windows
            piper_exe = 'piper.exe'
        else:
            piper_exe = 'piper'
        
        # Vérifier si piper est dans le PATH
        try:
            result = subprocess.run([piper_exe, '--version'], 
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return piper_exe
        except:
            pass
        
        # Chercher dans le dossier local
        local_piper = Path(__file__).parent / 'piper' / piper_exe
        if local_piper.exists():
            return str(local_piper)
        
        raise FileNotFoundError(
            "Piper n'est pas installé. "
            "Installez-le avec: pip install piper-tts "
            "ou téléchargez-le depuis: https://github.com/rhasspy/piper"
        )
    
    async def synthesize_phrase(
        self,
        texte: str,
        caractere: str = "joueur",
        phrase_index: int = 0
    ) -> Tuple[bytes, float]:
        """
        Synthétise une phrase en audio
        
        Returns:
            (audio_bytes, duration_seconds)
        """
        
        # Nettoyer le texte
        texte_propre = nettoyer_texte_pour_tts(texte)
        
        # Configuration pour ce caractère
        config = VOIX_CONFIG.get(caractere, VOIX_CONFIG["joueur"])
        
        # Créer un fichier temporaire pour l'audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            temp_path = temp_audio.name
        
        try:
            # Commande Piper (version simplifiée pour le prototype)
            # Dans la vraie version, utiliser l'API Python de Piper
            # Pour l'instant, cette fonction retourne un placeholder
            
            # TODO: Implémenter l'appel réel à Piper
            # cmd = [
            #     self.piper_path,
            #     '--model', config['voice_model'],
            #     '--output_file', temp_path
            # ]
            
            # Pour le prototype, retourner un placeholder
            print(f"🎤 Synthèse: [{caractere}] \"{texte_propre}\"")
            
            # Simuler une durée basée sur la longueur du texte
            duration = len(texte_propre) * 0.08 / config['speed']
            
            # Retourner des données vides pour l'instant
            return b'', duration
            
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    async def synthesize_streaming(
        self,
        texte: str,
        caractere: str = "joueur"
    ):
        """
        Génère l'audio phrase par phrase (streaming)
        
        Yields:
            dict avec {index, audio, duration, is_last}
        """
        # Nettoyer et découper
        phrases = decouper_en_phrases(texte)
        
        print(f"📝 Découpage en {len(phrases)} phrase(s)")
        
        for i, phrase in enumerate(phrases):
            audio, duration = await self.synthesize_phrase(
                phrase,
                caractere=caractere,
                phrase_index=i
            )
            
            yield {
                "index": i,
                "audio": audio,
                "duration": duration,
                "phrase": phrase,
                "is_last": (i == len(phrases) - 1)
            }


# Instance globale (créée seulement si nécessaire)
piper_tts = None

def get_piper_tts():
    """Récupère l'instance TTS (lazy loading)"""
    global piper_tts
    if piper_tts is None:
        piper_tts = PiperTTS()
    return piper_tts


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def get_phrases_secours(caractere: str) -> List[str]:
    """Retourne les phrases de secours pour un caractère"""
    return PHRASES_SECOURS.get(caractere, PHRASES_SECOURS["joueur"])


def get_message_accueil(caractere: str) -> str:
    """Retourne le message d'accueil pour un caractère"""
    return MESSAGES_ACCUEIL.get(caractere, MESSAGES_ACCUEIL["joueur"])


async def pre_enregistrer_phrases(caractere: str):
    """
    Pré-enregistre toutes les phrases courantes pour ce caractère
    À exécuter au démarrage du serveur
    """
    phrases_a_enregistrer = []
    
    # Messages de secours
    phrases_a_enregistrer.extend(get_phrases_secours(caractere))
    
    # Message d'accueil
    phrases_a_enregistrer.append(get_message_accueil(caractere))
    
    # Petits sons
    phrases_a_enregistrer.extend(["hmm", "oh", "ah", "euh"])
    
    print(f"🎙️ Pré-enregistrement de {len(phrases_a_enregistrer)} phrases pour {caractere}...")
    
    # TODO: Synthétiser et sauvegarder chaque phrase
    # Pour l'instant, juste simuler
    for phrase in phrases_a_enregistrer:
        print(f"   - \"{phrase}\"")
