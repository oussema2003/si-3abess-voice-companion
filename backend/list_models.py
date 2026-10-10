from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

client = Groq(api_key=os.getenv("GROQ_API_KEY").strip().strip('"').strip("'"))

print("\n=== Modèles disponibles sur Groq ===\n")

try:
    models = client.models.list()
    for model in models.data:
        print(f"✅ {model.id}")
        if hasattr(model, 'description'):
            print(f"   {model.description}")
except Exception as e:
    print(f"Erreur: {e}")
