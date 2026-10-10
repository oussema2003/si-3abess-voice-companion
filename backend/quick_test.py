import requests
import json

response = requests.post(
    "http://localhost:3000/chat",
    json={"text": "Salut si-3abess !"}
)

print("\n=== Réponse ===")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
