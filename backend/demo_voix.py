"""
🎤 DÉMO DES VOIX DE si-3abess
Génère un exemple audio pour chaque caractère
"""

from piper_tts import synthesize_text
import os

print("\n" + "="*60)
print("🎤 DÉMONSTRATION DES VOIX DE si-3abess")
print("="*60 + "\n")

# Créer un dossier pour les démos
os.makedirs("demo_audio", exist_ok=True)

# Phrases de démonstration pour chaque caractère
demos = {
    "timide": {
        "phrase": "Euh... bonjour. Je suis un peu timide mais... content de te rencontrer.",
        "description": "Doux, hésitant, pauses"
    },
    "joueur": {
        "phrase": "Salut ! Je suis super content de te voir ! On va bien s'amuser ensemble !",
        "description": "Énergique, rapide, enthousiaste"
    },
    "sage": {
        "phrase": "Bonjour à toi. Je suis là pour t'écouter et réfléchir avec toi, calmement.",
        "description": "Posé, lent, apaisant"
    },
    "farceur": {
        "phrase": "Hey ! Moi c'est si-3abess. Attention, je suis un petit malin... On va rire !",
        "description": "Taquin, dynamique, expressif"
    }
}

print("🎭 Génération des 4 voix de si-3abess...\n")

for caractere, config in demos.items():
    print(f"📝 {caractere.upper()}")
    print(f"   Description : {config['description']}")
    print(f"   Phrase : \"{config['phrase']}\"")
    
    # Synthétiser
    audio, duration = synthesize_text(config['phrase'], caractere)
    
    if audio:
        # Sauvegarder
        filename = f"demo_audio/{caractere}.wav"
        with open(filename, "wb") as f:
            f.write(audio)
        
        print(f"   ✅ Généré : {filename}")
        print(f"   ⏱️  Durée : {duration:.2f}s")
    else:
        print(f"   ❌ Erreur lors de la génération")
    
    print()

print("="*60)
print("✅ DÉMO TERMINÉE !")
print("="*60)
print()
print("📂 Fichiers générés dans : demo_audio/")
print("   • timide.wav")
print("   • joueur.wav")
print("   • sage.wav")
print("   • farceur.wav")
print()
print("🎧 Écoutez ces fichiers pour comparer les 4 voix !")
print()
