"""
Test direct de l'API Piper pour comprendre son fonctionnement
"""

from piper import PiperVoice
import wave

print("\n🔍 Test direct de Piper\n")

# Charger la voix
model_file = "piper/fr_FR-siwis-medium.onnx"
print(f"📂 Chargement de {model_file}...")
voice = PiperVoice.load(model_file)
print(f"✅ Voix chargée")
print(f"   Sample rate: {voice.config.sample_rate} Hz")
print(f"   Num speakers: {voice.config.num_speakers if hasattr(voice.config, 'num_speakers') else 'N/A'}")

# Tester la synthèse
texte = "Bonjour, je suis si-3abess."
print(f"\n📝 Synthèse de: \"{texte}\"\n")

# Méthode 1: Essayer avec un fichier WAV
print("📌 Méthode 1: Fichier WAV direct")
try:
    with wave.open("test_method1.wav", "wb") as wav_file:
        voice.synthesize(texte, wav_file)
    print("   ✅ Succès")
    
    with wave.open("test_method1.wav", "rb") as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        print(f"   📊 {frames} frames, {rate} Hz, {duration:.2f}s")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Méthode 2: Essayer avec synthesize_stream_raw
print("\n📌 Méthode 2: Stream raw")
try:
    samples = []
    for chunk in voice.synthesize_stream_raw(texte):
        samples.extend(chunk)
    
    print(f"   ✅ {len(samples)} échantillons générés")
    
    # Sauvegarder en WAV
    import array
    with wave.open("test_method2.wav", "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(voice.config.sample_rate)
        audio_bytes = array.array('h', samples).tobytes()
        wav_file.writeframes(audio_bytes)
    
    duration = len(samples) / voice.config.sample_rate
    print(f"   📊 Durée: {duration:.2f}s")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print("\n✅ Test terminé\n")
