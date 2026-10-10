"""
Tests pour le système TTS de si-3abess
"""

from tts_manager import (
    nettoyer_texte_pour_tts,
    decouper_en_phrases,
    VOIX_CONFIG,
    get_phrases_secours,
    get_message_accueil
)
from colorama import init, Fore, Style

init()

print(f"\n{Fore.CYAN}{'='*70}")
print(f"🧪 TESTS DU SYSTÈME TTS")
print(f"{'='*70}{Style.RESET_ALL}\n")

# ============================================================================
# TEST 1 : Nettoyage du texte
# ============================================================================

print(f"{Fore.YELLOW}📝 TEST 1 : Nettoyage du texte{Style.RESET_ALL}\n")

tests_nettoyage = [
    ("si-3abess est super !", "si-3abess est super !"),
    ("M. Dupont va bien", "Monsieur Dupont va bien"),
    ("Il est 3 heures", "Il est trois heures"),
    ("USA et SMS", "U S A et S M S"),
    ("C'est SUPER cool", "C'est Super cool"),
    ("etc. voilà", "et cetera voilà")
]

reussis = 0
for input_text, expected in tests_nettoyage:
    result = nettoyer_texte_pour_tts(input_text)
    status = "✅" if expected.lower() in result.lower() else "❌"
    if status == "✅":
        reussis += 1
    print(f"{status} \"{input_text}\" → \"{result}\"")

print(f"\n{Fore.GREEN}Réussis: {reussis}/{len(tests_nettoyage)}{Style.RESET_ALL}\n")

# ============================================================================
# TEST 2 : Découpe en phrases
# ============================================================================

print(f"{Fore.YELLOW}📝 TEST 2 : Découpe en phrases{Style.RESET_ALL}\n")

tests_decoupe = [
    ("Salut ! Comment ça va ?", 2),
    ("Oh. Euh. Je vois.", 1),  # Devrait regrouper
    ("Bonjour M. Dupont.", 1),  # M. ne doit pas couper
    ("Phrase courte. Et une autre phrase.", 2),
]

reussis = 0
for texte, nb_attendu in tests_decoupe:
    phrases = decouper_en_phrases(texte)
    nb_obtenu = len(phrases)
    status = "✅" if nb_obtenu == nb_attendu else "❌"
    if status == "✅":
        reussis += 1
    
    print(f"{status} \"{texte}\"")
    print(f"   Attendu: {nb_attendu} phrase(s), Obtenu: {nb_obtenu}")
    for i, phrase in enumerate(phrases):
        print(f"   [{i+1}] \"{phrase}\"")
    print()

print(f"{Fore.GREEN}Réussis: {reussis}/{len(tests_decoupe)}{Style.RESET_ALL}\n")

# ============================================================================
# TEST 3 : Configuration des voix
# ============================================================================

print(f"{Fore.YELLOW}🎤 TEST 3 : Configuration des voix{Style.RESET_ALL}\n")

for caractere, config in VOIX_CONFIG.items():
    print(f"{Fore.MAGENTA}🎭 {caractere.upper()}{Style.RESET_ALL}")
    print(f"   Modèle: {config['voice_model']}")
    print(f"   Vitesse: {config['speed']}x")
    print(f"   Pitch: {config['pitch_shift']:+d}")
    print(f"   Volume: {config['volume']}")
    print(f"   Pause: {config['pause_between_sentences']}s")
    print()

# ============================================================================
# TEST 4 : Phrases de secours
# ============================================================================

print(f"{Fore.YELLOW}💬 TEST 4 : Phrases de secours{Style.RESET_ALL}\n")

for caractere in ["timide", "joueur", "sage", "farceur"]:
    phrases = get_phrases_secours(caractere)
    accueil = get_message_accueil(caractere)
    
    print(f"{Fore.MAGENTA}🎭 {caractere.upper()}{Style.RESET_ALL}")
    print(f"   Accueil: \"{accueil}\"")
    print(f"   Secours:")
    for i, phrase in enumerate(phrases):
        print(f"     {i+1}. \"{phrase}\"")
    print()

# ============================================================================
# TEST 5 : Phrases de test pour écoute
# ============================================================================

print(f"{Fore.YELLOW}👂 TEST 5 : Phrases pour test d'écoute{Style.RESET_ALL}\n")

phrases_test = [
    "Bonjour, je suis si-3abess, ton robot-compagnon.",
    "J'ai compris que tu es triste. Je suis là pour toi.",
    "Génial ! Tu as l'air content aujourd'hui !",
    "Trois cent vingt-cinq euros et cinquante centimes.",
    "Raconte-moi ce qui s'est passé.",
    "Oh là là, quel surprise !",
    "Euh... je ne suis pas sûr de comprendre.",
    "Tu veux jouer à un jeu avec moi ?",
    "Prends le temps de réfléchir calmement.",
    "Haha, c'est drôle ce que tu dis !"
]

print(f"{Fore.CYAN}📋 {len(phrases_test)} phrases à tester avec chaque voix :{Style.RESET_ALL}\n")

for i, phrase in enumerate(phrases_test, 1):
    print(f"   {i}. \"{phrase}\"")

print(f"\n{Fore.CYAN}💡 Pour tester manuellement :{Style.RESET_ALL}")
print(f"   echo \"Phrase de test\" | piper --model voix.onnx --output_file test.wav")

# ============================================================================
# TEST 6 : Caractéristiques distinctives
# ============================================================================

print(f"\n{Fore.YELLOW}🎭 TEST 6 : Caractéristiques distinctives{Style.RESET_ALL}\n")

phrase_meme = "J'ai eu une mauvaise note aujourd'hui"

print(f"{Fore.CYAN}Phrase identique pour les 4 caractères :{Style.RESET_ALL}")
print(f"   \"{phrase_meme}\"\n")

caracteristiques = {
    "timide": {
        "vitesse": "Lente (0.9x)",
        "ton": "Doux, hésitant",
        "attendu": "Voix posée, pauses naturelles"
    },
    "joueur": {
        "vitesse": "Rapide (1.2x)",
        "ton": "Énergique, aigu",
        "attendu": "Voix dynamique, rythme soutenu"
    },
    "sage": {
        "vitesse": "Très lente (0.85x)",
        "ton": "Grave, calme",
        "attendu": "Voix profonde, pauses longues"
    },
    "farceur": {
        "vitesse": "Moyenne (1.1x)",
        "ton": "Expressif, varié",
        "attendu": "Voix vivante, intonations marquées"
    }
}

for caractere, car in caracteristiques.items():
    print(f"{Fore.MAGENTA}🎭 {caractere.upper()}{Style.RESET_ALL}")
    print(f"   Vitesse: {car['vitesse']}")
    print(f"   Ton: {car['ton']}")
    print(f"   Attendu: {car['attendu']}")
    print()

print(f"{Fore.GREEN}{'='*70}")
print(f"✅ TESTS TERMINÉS")
print(f"{'='*70}{Style.RESET_ALL}\n")

print(f"{Fore.CYAN}📋 PROCHAINES ÉTAPES :{Style.RESET_ALL}")
print(f"   1. Installer Piper (voir INSTALLATION_PIPER.md)")
print(f"   2. Télécharger les voix fr_FR-siwis-medium et fr_FR-upmc-medium")
print(f"   3. Générer les fichiers audio de test")
print(f"   4. Faire écouter à 5 personnes")
print(f"   5. Noter les résultats d'écoute")
print()
