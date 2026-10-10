"""
Test des 4 caractères avec la même phrase
"""
import requests
import json
from colorama import init, Fore, Style

init()

API_URL = "http://localhost:3000"

# Test de la même phrase avec les 4 caractères
phrase_test = "J'ai eu une mauvaise note aujourd'hui"

caracteres = ["timide", "joueur", "sage", "farceur"]

print(f"\n{Fore.CYAN}{'='*70}")
print(f"🎭 TEST DES 4 CARACTÈRES")
print(f"{'='*70}{Style.RESET_ALL}\n")
print(f"{Fore.YELLOW}Phrase de test:{Style.RESET_ALL} \"{phrase_test}\"\n")

for caractere in caracteres:
    print(f"{Fore.MAGENTA}🎭 Caractère: {caractere.upper()}{Style.RESET_ALL}")
    
    response = requests.post(
        f"{API_URL}/chat",
        json={
            "text": phrase_test,
            "caractere": caractere,
            "public": "tout_le_monde"
        },
        timeout=30
    )
    
    data = response.json()
    
    if data.get("success"):
        print(f"   💬 Réponse: {Fore.GREEN}{data.get('response', '')}{Style.RESET_ALL}")
        print(f"   😊 Émotion: {data.get('emotion', 'N/A')}")
        print(f"   🎯 Humeur: {data.get('humeur_utilisateur', 'N/A')}\n")
    else:
        print(f"   {Fore.RED}❌ Erreur{Style.RESET_ALL}\n")

print(f"{Fore.GREEN}✅ Test terminé !{Style.RESET_ALL}\n")
print(f"{Fore.CYAN}Observez les différences de ton et de style !{Style.RESET_ALL}\n")
