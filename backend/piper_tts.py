"""
Implémentation simple et fonctionnelle de Piper TTS pour si-3abess
"""

import io
import wave
import hashlib
from pathlib import Path
from typing import Tuple
import re

try:
    from piper import PiperVoice
    PIPER_AVAILABLE = True
except ImportError:
    print("⚠️ Piper non disponible")
    PIPER_AVAILABLE = False


# Configuration des voix par caractère - vitesses ajustées pour un débit naturel et lent
VOIX_CONFIG = {
    "timide": {"model": "fr_FR-siwis-medium", "speed": 0.75},  # Très lent et hésitant
    "joueur": {"model": "fr_FR-siwis-medium", "speed": 0.95},  # Légèrement plus lent pour rester naturel
    "sage": {"model": "fr_FR-siwis-medium", "speed": 0.7},     # Très lent et posé
    "farceur": {"model": "fr_FR-siwis-medium", "speed": 0.9}   # Modéré
}


class SimplePiperTTS:
    """TTS simple avec Piper"""
    
    def __init__(self):
        self.voices = {}
        self.models_path = Path(__file__).parent / "piper"
        self.cache_path = Path(__file__).parent / "tts_cache"
        self.cache_path.mkdir(exist_ok=True)
        
        if PIPER_AVAILABLE:
            self._load_voices()
    
    def _load_voices(self):
        """Charge les voix disponibles"""
        model_file = self.models_path / "fr_FR-siwis-medium.onnx"
        
        if model_file.exists():
            try:
                print(f"🎤 Chargement de fr_FR-siwis-medium...")
                self.voices["fr_FR-siwis-medium"] = PiperVoice.load(str(model_file))
                print(f"   ✅ Voix chargée")
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        else:
            print(f"   ⚠️  Modèle non trouvé: {model_file}")
    
    def synthesize(self, texte: str, caractere: str = "joueur") -> Tuple[bytes, float]:
        """
        Synthétise du texte en audio
        
        Args:
            texte: Texte à synthétiser
            caractere: timide, joueur, sage ou farceur
        
        Returns:
            (audio_wav_bytes, duration_seconds)
        """
        
        if not PIPER_AVAILABLE or not self.voices:
            print(f"🎤 [Mode silencieux] {texte}")
            return b'', len(texte) * 0.08
        
        # Nettoyer le texte
        texte = self._clean_text(texte)
        
        # Configuration
        config = VOIX_CONFIG.get(caractere, VOIX_CONFIG["joueur"])
        voice_name = config["model"]
        speed = config["speed"]
        
        # Vérifier cache
        cache_key = hashlib.md5(f"{texte}_{caractere}".encode()).hexdigest()
        cache_file = self.cache_path / f"{cache_key}.wav"
        
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                audio_data = f.read()
            duration = self._get_duration(audio_data)
            return audio_data, duration
        
        # Synthétiser
        try:
            voice = self.voices[voice_name]
            audio_buffer = io.BytesIO()
            
            # Créer la config de synthèse avec la vitesse ajustée
            from piper.config import SynthesisConfig
            syn_config = SynthesisConfig(
                length_scale=1.0/speed  # length_scale inverse: plus grand = plus lent
            )
            
            # Utiliser synthesize_wav qui gère le format automatiquement
            with wave.open(audio_buffer, 'wb') as wav_file:
                voice.synthesize_wav(texte, wav_file, syn_config=syn_config, set_wav_format=True)
            
            audio_data = audio_buffer.getvalue()
            duration = self._get_duration(audio_data)
            
            # Sauvegarder dans cache
            with open(cache_file, 'wb') as f:
                f.write(audio_data)
            
            print(f"✅ Synthèse: {texte[:50]}... ({duration:.2f}s)")
            return audio_data, duration
            
        except Exception as e:
            print(f"❌ Erreur synthèse: {e}")
            return b'', 0.0
    
    def _clean_text(self, texte: str) -> str:
        """Nettoie le texte pour TTS"""
        # Remplacements basiques
        replacements = {
            "si-3abess": "si-3abess",
            "M.": "Monsieur",
            "Mme": "Madame",
            "etc.": "et cetera"
        }
        
        for old, new in replacements.items():
            texte = texte.replace(old, new)
        
        # Supprimer émojis
        texte = re.sub(r'[😀-🙏🌀-🗿🚀-🛿]', '', texte)
        
        return texte.strip()
    
    def _get_duration(self, wav_data: bytes) -> float:
        """Calcule la durée d'un WAV"""
        try:
            with wave.open(io.BytesIO(wav_data), 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                return frames / float(rate)
        except:
            return 0.0


# Instance globale
tts = SimplePiperTTS()


def synthesize_text(texte: str, caractere: str = "joueur") -> Tuple[bytes, float]:
    """
    Fonction simple pour synthétiser du texte
    
    Usage:
        audio, duration = synthesize_text("Bonjour !", "timide")
    """
    return tts.synthesize(texte, caractere)
