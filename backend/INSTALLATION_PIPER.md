# Installation de Piper TTS 🎤

Guide complet pour installer et configurer Piper pour si-3abess.

## Option 1 : Installation avec pip (Recommandé)

```bash
pip install piper-tts
```

**Note** : Cette version peut ne pas inclure les modèles de voix. Vous devrez les télécharger séparément.

## Option 2 : Installation manuelle (Plus de contrôle)

### Windows

1. Téléchargez la dernière version depuis GitHub :
   https://github.com/rhasspy/piper/releases

2. Téléchargez `piper_windows_amd64.zip`

3. Extrayez dans `backend/piper/`

4. Votre structure devrait être :
   ```
   backend/
   ├── piper/
   │   ├── piper.exe
   │   ├── espeak-ng-data/
   │   └── ...
   ```

### Linux / Mac

```bash
# Télécharger Piper
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz

# Extraire
tar -xzf piper_linux_x86_64.tar.gz -C backend/piper/

# Rendre exécutable
chmod +x backend/piper/piper
```

## Téléchargement des voix françaises

### Voix recommandées pour si-3abess

#### 1. fr_FR-siwis-medium (Douce, claire)
- **Utilisation** : Timide, Sage
- **Qualité** : ⭐⭐⭐⭐
- **Taille** : ~63 MB

```bash
# Télécharger le modèle
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx

# Télécharger le fichier de configuration
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json
```

#### 2. fr_FR-upmc-medium (Vive, expressive)
- **Utilisation** : Joueur, Farceur
- **Qualité** : ⭐⭐⭐⭐
- **Taille** : ~63 MB

```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx.json
```

#### 3. fr_FR-mls-medium (Alternative, multi-locuteurs)
- **Avantage** : Plusieurs voix dans un modèle
- **Qualité** : ⭐⭐⭐
- **Taille** : ~63 MB

```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/mls/medium/fr_FR-mls-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/mls/medium/fr_FR-mls-medium.onnx.json
```

### Structure des fichiers

```
backend/
├── piper/
│   ├── piper.exe  (ou piper sur Linux/Mac)
│   └── voices/
│       ├── fr_FR-siwis-medium.onnx
│       ├── fr_FR-siwis-medium.onnx.json
│       ├── fr_FR-upmc-medium.onnx
│       └── fr_FR-upmc-medium.onnx.json
```

## Vérification de l'installation

```bash
# Tester Piper
piper --version

# Tester une voix
echo "Bonjour, je suis si-3abess" | piper \
  --model backend/piper/voices/fr_FR-siwis-medium.onnx \
  --output_file test.wav

# Écouter le résultat
# Windows : start test.wav
# Linux : aplay test.wav
# Mac : afplay test.wav
```

## Licences des voix

| Voix | License | Usage commercial |
|------|---------|------------------|
| siwis | CC BY-SA 4.0 | ✅ Oui (avec attribution) |
| upmc | CC BY-SA 4.0 | ✅ Oui (avec attribution) |
| mls | CC BY-SA 4.0 | ✅ Oui (avec attribution) |

**Attribution requise** :
```
Voix française générée par Piper TTS
Modèle : fr_FR-siwis-medium
Source : https://github.com/rhasspy/piper
Licence : CC BY-SA 4.0
```

## Test des voix

Script Python pour tester toutes les voix :

```python
import subprocess
import os

voix = [
    "fr_FR-siwis-medium",
    "fr_FR-upmc-medium",
    "fr_FR-mls-medium"
]

phrases_test = [
    "Bonjour, je suis si-3abess, ton robot-compagnon.",
    "J'ai compris que tu es triste. Je suis là pour toi.",
    "Génial ! Tu as l'air content aujourd'hui !",
    "Trois cent vingt-cinq euros et cinquante centimes.",
    "Raconte-moi ce qui s'est passé."
]

for voix_nom in voix:
    print(f"\n🎤 Test de {voix_nom}")
    for i, phrase in enumerate(phrases_test):
        output = f"test_{voix_nom}_{i}.wav"
        cmd = [
            "piper",
            "--model", f"backend/piper/voices/{voix_nom}.onnx",
            "--output_file", output
        ]
        
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        process.communicate(input=phrase.encode('utf-8'))
        print(f"   Généré: {output}")
```

## Dépannage

### "piper: command not found"

**Solution** : Ajoutez Piper au PATH ou utilisez le chemin complet.

```bash
# Windows
set PATH=%PATH%;D:\projet\Nouveau dossier\backend\piper

# Linux/Mac
export PATH=$PATH:/chemin/vers/backend/piper
```

### "Model file not found"

**Solution** : Vérifiez que les fichiers `.onnx` et `.onnx.json` sont téléchargés.

### Voix robotique ou hachée

**Solutions** :
- Utilisez `medium` au lieu de `low` pour plus de qualité
- Ajustez la vitesse (speed) dans la configuration
- Vérifiez que le CPU n'est pas surchargé

### Temps de synthèse trop long

**Solutions** :
- Pré-chargez les modèles en mémoire au démarrage
- Utilisez `low` pour plus de rapidité
- Mettez en cache les phrases courantes
- Ajoutez plus de CPU ou utilisez plusieurs processus

## Optimisation des performances

### Pré-chargement des modèles

```python
# Au démarrage du serveur
from piper import PiperVoice

voices = {}
for caractere, config in VOIX_CONFIG.items():
    model_path = f"backend/piper/voices/{config['voice_model']}.onnx"
    voices[caractere] = PiperVoice.load(model_path)
```

### Cache des phrases fréquentes

```python
import hashlib

def get_cache_key(texte: str, caractere: str) -> str:
    return hashlib.md5(f"{texte}_{caractere}".encode()).hexdigest()

# Vérifier le cache avant la synthèse
cache_key = get_cache_key(phrase, caractere)
if cache_key in audio_cache:
    return audio_cache[cache_key]
```

## Alternatives à Piper

Si Piper ne fonctionne pas bien :

1. **gTTS** (Google Text-to-Speech) : Simple mais nécessite internet
2. **Coqui TTS** : Open-source, très naturel mais plus lourd
3. **Edge-TTS** : Microsoft Edge TTS, gratuit, très naturel
4. **ElevenLabs** : Payant mais qualité exceptionnelle

## Prochaines étapes

Après installation :
1. ✅ Testez les 3 voix avec les phrases de test
2. ✅ Choisissez les 2 meilleures voix
3. ✅ Pré-enregistrez les phrases de secours
4. ✅ Configurez `tts_manager.py` avec les chemins corrects
5. ✅ Lancez les tests d'écoute

## Ressources

- [Piper GitHub](https://github.com/rhasspy/piper)
- [Liste des voix](https://rhasspy.github.io/piper-samples/)
- [Documentation Piper](https://github.com/rhasspy/piper/blob/master/README.md)
- [Hugging Face - Modèles](https://huggingface.co/rhasspy/piper-voices)
