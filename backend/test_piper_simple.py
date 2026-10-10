"""
Test simple de Piper TTS
"""

from piper_tts import synthesize_text
import wave

print("\n🧪 TEST DE PIPER TTS\n")

# Test 1: Synthèse simple
print("📝 Test 1: Synthèse basique")
audio, duration = synthesize_text("Bonjour, je suis si-3abess.", "joueur")

if audio:
    print(f"   ✅ Audio généré: {len(audio)} bytes, {duration:.2f}s")
    
    # Sauvegarder pour écouter
    with open("test_si_3abess.wav", "wb") as f:
        f.write(audio)
    print(f"   💾 Fichier sauvé: test_si_3abess.wav")
else:
    print(f"   ⚠️  Pas d'audio (mode silencieux)")

# Test 2: Les 4 caractères
print("\n📝 Test 2: Les 4 caractères")
phrase = "J'ai compris."

for caractere in ["timide", "joueur", "sage", "farceur"]:
    audio, duration = synthesize_text(phrase, caractere)
    print(f"   🎭 {caractere}: {duration:.2f}s")
    
    if audio:
        with open(f"test_{caractere}.wav", "wb") as f:
            f.write(audio)

print("\n✅ Tests terminés !")
print("Écoutez les fichiers .wav générés\n")
