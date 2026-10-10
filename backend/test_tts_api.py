"""
Test de l'API TTS sans démarrer le serveur complet
"""

from piper_tts import synthesize_text

print("\n🧪 TEST DE L'API TTS\n")

# Test 1: Synthèse simple
print("📝 Test 1: Synthèse basique")
audio, duration = synthesize_text("Bonjour ! Je suis si-3abess, ton robot-compagnon.", "joueur")

if audio:
    print(f"   ✅ Audio généré: {len(audio)} bytes, {duration:.2f}s")
    with open("test_api_joueur.wav", "wb") as f:
        f.write(audio)
    print(f"   💾 Fichier sauvé: test_api_joueur.wav")
else:
    print(f"   ⚠️  Pas d'audio (mode silencieux)")

# Test 2: Phrase avec caractères spéciaux
print("\n📝 Test 2: Phrase avec caractères spéciaux")
audio, duration = synthesize_text("J'ai compris ! Tu veux qu'on discute de M. Robot ?", "sage")

if audio:
    print(f"   ✅ Audio généré: {len(audio)} bytes, {duration:.2f}s")
    with open("test_api_sage.wav", "wb") as f:
        f.write(audio)
else:
    print(f"   ⚠️  Pas d'audio")

# Test 3: Cache fonctionne
print("\n📝 Test 3: Test du cache (même phrase)")
audio2, duration2 = synthesize_text("J'ai compris ! Tu veux qu'on discute de M. Robot ?", "sage")

if audio2 == audio:
    print(f"   ✅ Cache fonctionne ! Audio identique")
else:
    print(f"   ⚠️  Cache ne fonctionne pas")

# Test 4: Phrase courte
print("\n📝 Test 4: Phrase très courte")
audio, duration = synthesize_text("Oh !", "surpris")
print(f"   ✅ {len(audio)} bytes, {duration:.2f}s")

# Test 5: Phrase longue
print("\n📝 Test 5: Phrase longue")
audio, duration = synthesize_text(
    "Je suis content que tu sois là aujourd'hui. On peut parler de ce que tu veux.",
    "timide"
)
print(f"   ✅ {len(audio)} bytes, {duration:.2f}s")

print("\n✅ Tous les tests terminés !\n")
