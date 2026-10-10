"""
🎙️ Phrases et sons pré-enregistrés pour masquer la latence
"""

import os
from pathlib import Path
from piper_tts import synthesize_text
from typing import Dict, List


# Phrases de secours par caractère
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

# Sons d'attente par caractère (pour masquer la réflexion)
SONS_ATTENTE = {
    "timide": ["Euh...", "Hmm...", "Oh..."],
    "joueur": ["Hmm !", "Ah !", "Oh oh !"],
    "sage": ["Hmm...", "Je vois...", "Intéressant..."],
    "farceur": ["Haha !", "Oh là là...", "Hmm hmm..."]
}

# Messages d'accueil
MESSAGES_ACCUEIL = {
    "timide": "Euh... bonjour. Je suis si-3abess.",
    "joueur": "Salut ! Je suis si-3abess, ton robot-compagnon !",
    "sage": "Bonjour à toi. Je m'appelle si-3abess.",
    "farceur": "Hey ! Moi c'est si-3abess, prêt pour l'aventure ?"
}


class PrerecordedAudioManager:
    """Gestionnaire des audios pré-enregistrés"""
    
    def __init__(self, cache_dir: str = "audio_prerecorded"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache: Dict[str, bytes] = {}
        self.initialized = False
    
    def get_cache_path(self, caractere: str, phrase_type: str, index: int = 0) -> Path:
        """Génère le chemin du fichier cache"""
        filename = f"{caractere}_{phrase_type}_{index}.wav"
        return self.cache_dir / filename
    
    def prerecord_all(self):
        """Pré-enregistre toutes les phrases et sons"""
        print("\n🎙️ Pré-enregistrement des phrases et sons...\n")
        
        total = 0
        
        for caractere in ["timide", "joueur", "sage", "farceur"]:
            print(f"📝 {caractere.upper()}")
            
            # Messages d'accueil
            self._prerecord_phrase(
                caractere, 
                MESSAGES_ACCUEIL[caractere],
                "accueil",
                0
            )
            total += 1
            
            # Phrases de secours
            for i, phrase in enumerate(PHRASES_SECOURS[caractere]):
                self._prerecord_phrase(caractere, phrase, "secours", i)
                total += 1
            
            # Sons d'attente
            for i, son in enumerate(SONS_ATTENTE[caractere]):
                self._prerecord_phrase(caractere, son, "attente", i)
                total += 1
            
            print()
        
        self.initialized = True
        print(f"✅ {total} audios pré-enregistrés !\n")
    
    def _prerecord_phrase(self, caractere: str, phrase: str, phrase_type: str, index: int):
        """Pré-enregistre une phrase"""
        cache_path = self.get_cache_path(caractere, phrase_type, index)
        cache_key = f"{caractere}_{phrase_type}_{index}"
        
        # Vérifier si déjà en cache
        if cache_path.exists():
            with open(cache_path, 'rb') as f:
                audio_data = f.read()
            self.cache[cache_key] = audio_data
            print(f"   ✓ {phrase_type}[{index}] (cache)")
            return
        
        # Synthétiser
        audio_data, duration = synthesize_text(phrase, caractere)
        
        if audio_data:
            # Sauvegarder
            with open(cache_path, 'wb') as f:
                f.write(audio_data)
            
            # Mettre en cache mémoire
            self.cache[cache_key] = audio_data
            
            print(f"   ✅ {phrase_type}[{index}]: {duration:.2f}s")
        else:
            print(f"   ❌ {phrase_type}[{index}]: Erreur")
    
    def get_accueil(self, caractere: str) -> bytes:
        """Récupère le message d'accueil"""
        cache_key = f"{caractere}_accueil_0"
        return self.cache.get(cache_key, b'')
    
    def get_secours(self, caractere: str, index: int = 0) -> bytes:
        """Récupère une phrase de secours"""
        cache_key = f"{caractere}_secours_{index}"
        return self.cache.get(cache_key, b'')
    
    def get_attente(self, caractere: str, index: int = 0) -> bytes:
        """Récupère un son d'attente"""
        cache_key = f"{caractere}_attente_{index}"
        return self.cache.get(cache_key, b'')
    
    def get_random_secours(self, caractere: str) -> bytes:
        """Récupère une phrase de secours aléatoire"""
        import random
        index = random.randint(0, len(PHRASES_SECOURS[caractere]) - 1)
        return self.get_secours(caractere, index)
    
    def get_random_attente(self, caractere: str) -> bytes:
        """Récupère un son d'attente aléatoire"""
        import random
        index = random.randint(0, len(SONS_ATTENTE[caractere]) - 1)
        return self.get_attente(caractere, index)


# Instance globale
_prerecorded_manager = None


def get_prerecorded_manager() -> PrerecordedAudioManager:
    """Récupère le gestionnaire (lazy loading)"""
    global _prerecorded_manager
    if _prerecorded_manager is None:
        _prerecorded_manager = PrerecordedAudioManager()
    return _prerecorded_manager


def init_prerecorded_audio():
    """Initialise les audios pré-enregistrés (à appeler au démarrage)"""
    manager = get_prerecorded_manager()
    if not manager.initialized:
        manager.prerecord_all()
    return manager


# Pour tester
if __name__ == "__main__":
    print("\n🧪 TEST DES AUDIOS PRÉ-ENREGISTRÉS\n")
    
    manager = PrerecordedAudioManager()
    manager.prerecord_all()
    
    # Tester la récupération
    print("\n🔍 Test de récupération :")
    for caractere in ["timide", "joueur", "sage", "farceur"]:
        accueil = manager.get_accueil(caractere)
        secours = manager.get_secours(caractere, 0)
        attente = manager.get_attente(caractere, 0)
        
        print(f"   {caractere}: accueil={len(accueil)} bytes, "
              f"secours={len(secours)} bytes, "
              f"attente={len(attente)} bytes")
    
    print("\n✅ Tests terminés !\n")
