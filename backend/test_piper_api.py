"""
Explorer l'API de Piper pour trouver les bonnes méthodes
"""

from piper import PiperVoice
import inspect

print("\n🔍 Exploration de l'API Piper\n")

# Charger la voix
model_file = "piper/fr_FR-siwis-medium.onnx"
print(f"📂 Chargement de {model_file}...")
voice = PiperVoice.load(model_file)
print(f"✅ Voix chargée\n")

# Lister toutes les méthodes disponibles
print("📋 Méthodes disponibles:")
for name in dir(voice):
    if not name.startswith('_'):
        attr = getattr(voice, name)
        if callable(attr):
            try:
                sig = inspect.signature(attr)
                print(f"   • {name}{sig}")
            except:
                print(f"   • {name}()")

# Lister les attributs
print("\n📋 Attributs disponibles:")
for name in dir(voice):
    if not name.startswith('_') and not callable(getattr(voice, name)):
        print(f"   • {name}: {type(getattr(voice, name))}")

# Explorer la config
print("\n📋 Configuration de la voix:")
for name in dir(voice.config):
    if not name.startswith('_'):
        print(f"   • {name}: {getattr(voice.config, name)}")
