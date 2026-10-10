import requests
import json
from colorama import init, Fore, Style

init()

API_URL = "http://localhost:3000"

# Tests spécifiques pour les nouvelles émotions
test_phrases = [
    ("J'ai gagné au loto !", "surpris"),
    ("Tu aimes la musique ?", "curieux"),
    ("Je suis super content aujourd'hui !", "joyeux"),
    ("Mon chien est mort...", "triste"),
    ("Comment ça va ?", None),  # Peut varier
]

print(f"\n{Fore.CYAN}{'='*70}")
print(f"🧪 TEST DES NOUVELLES ÉMOTIONS")
print(f"{'='*70}{Style.RESET_ALL}\n")

for phrase, emotion_attendue in test_phrases:
    print(f"{Fore.YELLOW}📝 Test:{Style.RESET_ALL} {phrase}")
    
    response = requests.post(
        f"{API_URL}/chat",
        json={"text": phrase},
        timeout=30
    )
    
    data = response.json()
    
    if data.get("success"):
        emotion = data.get("emotion", "N/A")
        texte = data.get("response", "")
        humeur = data.get("humeur_utilisateur", "N/A")
        
        # Vérifier l'émotion attendue
        if emotion_attendue:
            if emotion == emotion_attendue:
                print(f"{Fore.GREEN}   ✅ Émotion correcte: {emotion}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}   ❌ Émotion incorrecte: {emotion} (attendu: {emotion_attendue}){Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}   ℹ️  Émotion: {emotion}{Style.RESET_ALL}")
        
        print(f"   💬 Réponse: {texte}")
        print(f"   😊 Humeur détectée: {humeur}\n")
    else:
        print(f"{Fore.RED}   ❌ Erreur: {data.get('error', 'Unknown')}{Style.RESET_ALL}\n")

print(f"\n{Fore.GREEN}✅ Tests terminés !{Style.RESET_ALL}")
print(f"{Fore.CYAN}Ouvrez http://localhost:5173 pour tester visuellement les émotions !{Style.RESET_ALL}\n")
