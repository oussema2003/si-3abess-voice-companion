"""
🧪 Test du streaming et mesure de performance
"""

import requests
import time
import json
from statistics import mean, median

API_URL = "http://localhost:3000"

# Phrases de test
TEST_PHRASES = [
    "Bonjour !",
    "Comment vas-tu ?",
    "Raconte-moi une blague.",
    "Quel temps fait-il aujourd'hui ?",
    "J'ai passé une super journée !",
    "Je suis un peu fatigué.",
    "Tu peux m'aider avec mes devoirs ?",
    "Qu'est-ce que tu aimes faire ?",
    "Parle-moi de toi.",
    "C'est quoi ton caractère préféré ?"
]


def test_endpoint(endpoint: str, phrase: str, caractere: str = "joueur"):
    """Teste un endpoint et mesure la performance"""
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/{endpoint}",
            json={
                "text": phrase,
                "caractere": caractere,
                "public": "tout_le_monde",
                "history": [],
                "profile": {"prenom": "Test"}
            },
            timeout=30
        )
        
        total_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Extraire les métriques
            metrics = data.get("metrics", {})
            audio_chunks = data.get("audio_chunks", [])
            
            return {
                "success": True,
                "total_time": total_time,
                "server_metrics": metrics,
                "num_chunks": len(audio_chunks),
                "response_text": data.get("response", "")
            }
        else:
            return {
                "success": False,
                "error": response.text,
                "total_time": total_time
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "total_time": time.time() - start_time
        }


def run_benchmark():
    """Lance les benchmarks"""
    
    print("\n" + "="*80)
    print("🔬 BENCHMARK DE PERFORMANCE - STREAMING vs STANDARD")
    print("="*80 + "\n")
    
    # Vérifier que le serveur est disponible
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Serveur non disponible. Lancez : python main.py")
            return
    except:
        print("❌ Serveur non disponible. Lancez : python main.py")
        return
    
    print("✅ Serveur disponible\n")
    
    # Tests sur l'endpoint streaming
    print("📊 Test de l'endpoint /chat_streaming\n")
    
    streaming_times = []
    streaming_first_chunk = []
    
    for i, phrase in enumerate(TEST_PHRASES[:5], 1):
        print(f"   Test {i}/5: \"{phrase}\"")
        result = test_endpoint("chat_streaming", phrase)
        
        if result["success"]:
            total = result["total_time"]
            streaming_times.append(total)
            
            # Extraire le temps du premier chunk
            metrics = result.get("server_metrics", {})
            if metrics and "steps" in metrics:
                first_chunk = metrics["steps"].get("tts_first_chunk")
                if first_chunk:
                    streaming_first_chunk.append(first_chunk)
            
            print(f"      ✅ {total:.2f}s - {result['num_chunks']} phrases")
            print(f"      💬 Réponse: {result['response_text'][:60]}...")
        else:
            print(f"      ❌ Erreur: {result.get('error', 'Unknown')}")
        
        print()
        time.sleep(1)  # Pause entre les requêtes
    
    # Statistiques
    if streaming_times:
        print("\n" + "="*80)
        print("📈 STATISTIQUES")
        print("="*80 + "\n")
        
        print(f"🚀 Endpoint /chat_streaming:")
        print(f"   Moyenne : {mean(streaming_times):.2f}s")
        print(f"   Médiane : {median(streaming_times):.2f}s")
        print(f"   Min     : {min(streaming_times):.2f}s")
        print(f"   Max     : {max(streaming_times):.2f}s")
        
        if streaming_first_chunk:
            print(f"\n⚡ Temps jusqu'au premier chunk audio:")
            print(f"   Moyenne : {mean(streaming_first_chunk):.3f}s")
            print(f"   Médiane : {median(streaming_first_chunk):.3f}s")
        
        print("\n" + "="*80)
        print("🎯 OBJECTIFS")
        print("="*80 + "\n")
        
        med = median(streaming_times)
        if med < 2.0:
            print(f"   ✅ Médiane < 2s : {med:.2f}s")
        else:
            print(f"   ❌ Médiane > 2s : {med:.2f}s (objectif: < 2s)")
        
        p95 = sorted(streaming_times)[int(len(streaming_times) * 0.95)]
        if p95 < 3.5:
            print(f"   ✅ 95e centile < 3.5s : {p95:.2f}s")
        else:
            print(f"   ❌ 95e centile > 3.5s : {p95:.2f}s (objectif: < 3.5s)")
        
        if streaming_first_chunk:
            first = median(streaming_first_chunk)
            if first < 1.0:
                print(f"   ✅ Premier son < 1s : {first:.3f}s")
            else:
                print(f"   ⚠️  Premier son > 1s : {first:.3f}s (objectif: < 1s)")
        
        print()


def test_single_request():
    """Test d'une seule requête avec détails"""
    
    print("\n" + "="*80)
    print("🔍 TEST DÉTAILLÉ D'UNE REQUÊTE")
    print("="*80 + "\n")
    
    phrase = "Bonjour ! Comment vas-tu aujourd'hui ?"
    print(f"📝 Phrase: \"{phrase}\"\n")
    
    result = test_endpoint("chat_streaming", phrase)
    
    if result["success"]:
        print(f"✅ Succès en {result['total_time']:.2f}s\n")
        
        # Détails des métriques
        metrics = result.get("server_metrics", {})
        if metrics and "steps" in metrics:
            steps = metrics["steps"]
            print("⏱️  Détail des étapes:")
            
            if steps.get("transcription"):
                print(f"   Transcription      : {steps['transcription']:.3f}s")
            if steps.get("prompt_assembly"):
                print(f"   Assemblage prompt  : {steps['prompt_assembly']:.3f}s")
            if steps.get("llm_first_token"):
                print(f"   LLM premier token  : {steps['llm_first_token']:.3f}s")
            if steps.get("llm_first_sentence"):
                print(f"   LLM première phrase: {steps['llm_first_sentence']:.3f}s")
            if steps.get("tts_first_chunk"):
                print(f"   TTS premier chunk  : {steps['tts_first_chunk']:.3f}s")
            
            print()
        
        # Détails des chunks audio
        chunks = result.get("num_chunks", 0)
        print(f"🎵 {chunks} phrase(s) générée(s)\n")
        print(f"💬 Réponse: {result['response_text']}\n")
    
    else:
        print(f"❌ Erreur: {result.get('error')}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        test_single_request()
    else:
        run_benchmark()
    
    print("✅ Tests terminés !\n")
