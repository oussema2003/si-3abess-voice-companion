# 🤖 si-3abess Backend - FastAPI

API FastAPI pour si-3abess avec transcription vocale (Groq Whisper), génération de réponses (GPT-OSS), et synthèse vocale (Piper TTS).

---

## 📋 Table des Matières

- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement](#lancement)
- [API Endpoints](#api-endpoints)
- [Fichiers Principaux](#fichiers-principaux)
- [Tests](#tests)
- [Cache et Performance](#cache-et-performance)
- [Dépannage](#dépannage)

---

## 🏗️ Architecture

### Composants Principaux

```
Backend/
├── main.py                    # API FastAPI principale
├── si_3abess_personality.py        # Système de personnalité modulaire
├── piper_tts.py              # Synthèse vocale avec Piper
├── prerecorded_audio.py      # Gestion des audios pré-enregistrés
├── streaming_chat.py         # Chat avec streaming optimisé
├── performance_monitor.py    # Monitoring des performances
├── requirements.txt          # Dépendances Python
└── [fichiers de test]        # Tests unitaires et d'intégration
```

### Technologies Utilisées

| Technologie | Usage | Version |
|------------|-------|---------|
| **FastAPI** | Framework API REST | 0.104+ |
| **Groq API** | LLM (GPT-OSS) + Whisper | Latest |
| **Piper TTS** | Synthèse vocale française | Latest |
| **Python** | Langage principal | 3.8+ |
| **Uvicorn** | Serveur ASGI | Latest |

---

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)
- Clé API Groq (gratuite)

### Étape 1 : Environnement virtuel

```bash
# Créer l'environnement
python -m venv venv

# Activer (Windows)
venv\Scripts\activate

# Activer (Linux/Mac)
source venv/bin/activate
```

### Étape 2 : Installer les dépendances

```bash
cd backend
pip install -r requirements.txt
```

### Étape 3 : Installer Piper TTS

```bash
pip install piper-tts
```

Pour plus de détails : [INSTALLATION_PIPER.md](INSTALLATION_PIPER.md)

---

## ⚙️ Configuration

### Fichier `.env`

Créez un fichier `.env` à la **racine du projet** (pas dans backend/) :

```env
# Clé API Groq (OBLIGATOIRE)
GROQ_API_KEY=gsk_votre_cle_api_ici

# Chemins optionnels
PIPER_MODEL_PATH=backend/piper/fr_FR-siwis-medium.onnx
AUDIO_CACHE_DIR=backend/tts_cache
PRERECORDED_AUDIO_DIR=backend/audio_prerecorded
```

### Obtenir une clé Groq

1. Allez sur [console.groq.com](https://console.groq.com)
2. Créez un compte (gratuit)
3. Allez dans "API Keys"
4. Créez une nouvelle clé
5. Copiez-la dans votre `.env`

---

## 🎮 Lancement

### Mode Production

```bash
python main.py
```

Le serveur démarre sur **http://localhost:3000**

### Mode Développement (avec auto-reload)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### Vérifier que tout fonctionne

```bash
# Test de santé
curl http://localhost:3000/health

# Réponse attendue :
# {"status": "healthy", "groq_configured": true}
```

---

## 📡 API Endpoints

### 1. GET `/` - Informations

Retourne les informations sur l'API.

**Réponse :**
```json
{
  "message": "si-3abess Voice Assistant API is running!",
  "status": "online",
  "version": "2.0.0",
  "features": {
    "caracteres": ["timide", "joueur", "sage", "farceur"],
    "publics": ["jeunes", "adultes", "seniors", "tout_le_monde"],
    "combinations": 16
  }
}
```

---

### 2. GET `/health` - Santé

Vérifie l'état du serveur et de Groq.

**Réponse :**
```json
{
  "status": "healthy",
  "groq_configured": true
}
```

---

### 3. GET `/personnalites` - Liste des personnalités

Liste toutes les combinaisons disponibles.

**Réponse :**
```json
{
  "caracteres": {
    "timide": "Doux, hésitant, attentif",
    "joueur": "Énergique, enthousiaste, propose des jeux",
    "sage": "Calme, posé, bienveillant",
    "farceur": "Taquin, blagues gentilles"
  },
  "publics": {
    "jeunes": "Vocabulaire simple, ton encourageant (10-18 ans)",
    "adultes": "Naturel, décontracté (18-65 ans)",
    "seniors": "Langage mature, sujets variés (65+ ans)",
    "tout_le_monde": "Adapté à tous les âges (10-100 ans)"
  }
}
```

---

### 4. POST `/transcribe` - Transcription audio → texte

Convertit un fichier audio en texte via Groq Whisper.

**Paramètres :**
- `audio` (file) : Fichier audio (webm, mp3, wav, etc.)

**Exemple cURL :**
```bash
curl -X POST http://localhost:3000/transcribe \
  -F "audio=@monAudio.webm"
```

**Réponse :**
```json
{
  "success": true,
  "text": "Bonjour si-3abess, comment vas-tu ?",
  "language": "fr",
  "model": "whisper-large-v3"
}
```

---

### 5. POST `/chat` - Conversation complète

Envoie un message et reçoit une réponse avec texte, émotion et audio.

**Paramètres JSON :**
```json
{
  "text": "Bonjour si-3abess !",
  "caractere": "joueur",
  "public": "tout_le_monde",
  "history": [],
  "profile": {
    "prenom": "Marie",
    "centres_interet": ["science", "animaux"],
    "souvenirs": []
  }
}
```

**Réponse :**
```json
{
  "success": true,
  "response": "Salut Marie ! Trop cool de te parler ! Tu vas bien ?",
  "emotion": "joyeux",
  "humeur_utilisateur": "content",
  "audio_chunks": [
    {
      "index": 0,
      "audio": "base64_encoded_audio_data...",
      "duration": 2.5,
      "text": "Salut Marie ! Trop cool de te parler ! Tu vas bien ?",
      "is_last": true
    }
  ],
  "voix_config": {
    "speed": 0.95,
    "volume": 1.0
  }
}
```

---

### 6. POST `/chat_streaming` - Conversation optimisée

Version avec streaming pour latence réduite (< 2 secondes).

**Paramètres :** Identiques à `/chat`

**Réponse :** Identique à `/chat` + métriques de performance

```json
{
  "success": true,
  "response": "...",
  "emotion": "joyeux",
  "humeur_utilisateur": "content",
  "audio_chunks": [...],
  "metrics": {
    "transcription": 0.3,
    "llm_first_token": 0.2,
    "tts_first_chunk": 0.4,
    "total_time": 1.8
  },
  "request_id": "abc12345"
}
```

---

### 7. POST `/synthesize` - Synthèse vocale directe

Convertit du texte en audio WAV.

**Paramètres JSON :**
```json
{
  "text": "Bonjour, je suis si-3abess !",
  "caractere": "sage"
}
```

**Réponse :** Fichier audio WAV (Content-Type: audio/wav)

**Exemple cURL :**
```bash
curl -X POST http://localhost:3000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour !", "caractere": "joueur"}' \
  -o output.wav
```

---

## 📁 Fichiers Principaux

### `main.py` - API Principale

Contient tous les endpoints FastAPI :
- Gestion des requêtes HTTP
- Orchestration des différents modules
- Gestion des erreurs et fallbacks

**Points clés :**
- Initialisation du client Groq
- Chargement des audios pré-enregistrés au démarrage
- Gestion de l'historique de conversation (max 20 messages)
- Validation des réponses JSON

---

### `si_3abess_personality.py` - Système de Personnalité

Système modulaire avec 7 blocs de prompt :

1. **Identité de base** (fixe)
2. **Module caractère** (4 choix : timide, joueur, sage, farceur)
3. **Module public** (4 choix : jeunes, adultes, seniors, tout_le_monde)
4. **Style de parole** (fixe)
5. **Émotions** (fixe, 9 émotions)
6. **Mémoire utilisateur** (dynamique)
7. **Sécurité et format** (fixe, prioritaire)

**Fonctions principales :**
- `construire_prompt_systeme()` : Assemble le prompt final
- `get_exemples_par_caractere()` : Retourne les exemples de conversation
- `get_voix_config()` : Configuration vocale par caractère

---

### `piper_tts.py` - Synthèse Vocale

Gère la synthèse vocale avec Piper TTS.

**Fonctionnalités :**
- Chargement du modèle français (fr_FR-siwis-medium)
- Cache audio (évite de re-synthétiser les mêmes phrases)
- Configuration adaptative selon le caractère (vitesse, volume)
- Nettoyage du texte (émojis, abréviations, etc.)

**Configuration vocale :**

| Caractère | Vitesse | Description |
|-----------|---------|-------------|
| Timide | 0.75 | Très lent, hésitant |
| Joueur | 0.95 | Légèrement rapide, naturel |
| Sage | 0.7 | Très lent, posé |
| Farceur | 0.9 | Modéré |

---

### `prerecorded_audio.py` - Audios Pré-enregistrés

Gère les audios pré-générés pour :
- Messages d'accueil
- Messages d'attente
- Messages de secours (en cas d'erreur)

**Organisation :**
```
audio_prerecorded/
├── timide_accueil_0.wav
├── timide_attente_0.wav
├── timide_secours_0.wav
├── joueur_accueil_0.wav
└── ... (28 fichiers au total)
```

**Avantages :**
- ⚡ Latence quasi nulle
- 🔊 Qualité constante
- 💾 Pas besoin de Piper pour ces messages

---

### `streaming_chat.py` - Chat Optimisé

Version streaming pour réduire la latence.

**Fonctionnalités :**
- Streaming des tokens du LLM
- Découpage en phrases en temps réel
- Synthèse vocale phrase par phrase
- Métriques de performance détaillées

**Format de prompt spécial :**
```
EMOTION: joyeux | HUMEUR: content
Texte de la réponse ici
```

---

### `performance_monitor.py` - Monitoring

Mesure les performances de chaque requête :

**Métriques collectées :**
- `transcription` : Temps de transcription audio
- `llm_first_token` : Temps avant le premier token du LLM
- `llm_first_sentence` : Temps avant la première phrase complète
- `tts_first_chunk` : Temps avant le premier audio généré
- `total_time` : Temps total de la requête

---

## 🧪 Tests

### Test de santé

```bash
curl http://localhost:3000/health
```

---

### Test de transcription

```bash
# Créer un audio de test (enregistrez-vous dire "Bonjour si-3abess")
# Puis :
curl -X POST http://localhost:3000/transcribe \
  -F "audio=@test.webm"
```

---

### Test de conversation

```bash
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bonjour !",
    "caractere": "joueur",
    "public": "tout_le_monde"
  }'
```

---

### Test des 4 personnalités

```bash
python test_personnalites.py
```

Ce script teste les 4 caractères avec différentes phrases.

---

### Test de la synthèse vocale

```bash
# Test simple
python test_tts.py

# Test Piper direct
python test_piper_direct.py

# Test via API
python test_tts_api.py
```

---

### Test des audios pré-enregistrés

```bash
python prerecorded_audio.py
```

Affiche tous les audios disponibles et les joue.

---

## 🚀 Cache et Performance

### Cache Audio (`tts_cache/`)

Toutes les synthèses vocales sont mises en cache :
- **Clé** : Hash MD5 du texte + caractère
- **Format** : Fichiers WAV
- **Avantage** : Réponse instantanée pour les phrases déjà synthétisées

**Nettoyer le cache :**
```bash
# Windows
del /s /q tts_cache\*

# Linux/Mac
rm -rf tts_cache/*
```

---

### Stratégie de Performance

1. **Première fois** : Synthèse complète (~1-2 secondes)
2. **Fois suivantes** : Cache utilisé (~0.1 seconde)
3. **Messages fréquents** : Audios pré-enregistrés (~0.05 seconde)

**Objectif de latence :**
- Première réponse : < 2 secondes
- Réponses en cache : < 0.5 seconde
- Mode streaming : < 1.5 seconde pour le premier audio

---

## 🐛 Dépannage

### Erreur : "GROQ_API_KEY n'est pas définie"

**Cause :** Fichier `.env` manquant ou mal configuré

**Solution :**
1. Vérifiez que `.env` existe à la **racine** (pas dans backend/)
2. Vérifiez la syntaxe : `GROQ_API_KEY=gsk_...` (pas de guillemets)
3. Redémarrez le serveur

---

### Erreur : "Piper non disponible"

**Cause :** Piper TTS n'est pas installé

**Solution :**
```bash
pip install piper-tts
```

Si problème, consultez [INSTALLATION_PIPER.md](INSTALLATION_PIPER.md)

---

### Erreur : "Modèle fr_FR-siwis-medium non trouvé"

**Cause :** Modèle vocal manquant

**Solution :**
```bash
cd piper
# Télécharger le modèle
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json
```

---

### Problème : Audio silencieux

**Cause :** Mode silencieux activé (Piper non disponible)

**Vérification :**
```bash
python test_piper_simple.py
```

**Solution :**
1. Installer Piper correctement
2. Vérifier que le modèle existe
3. Redémarrer le serveur

---

### Problème : Réponses JSON invalides

**Cause :** Le modèle LLM génère parfois du texte non-JSON

**Solution :** Déjà gérée dans le code :
- Validation automatique
- Réessai avec température réduite
- Fallback vers message de secours

---

### Problème : Latence élevée

**Causes possibles :**
1. Connexion Internet lente (appels API Groq)
2. Première synthèse (pas en cache)
3. Modèle LLM surchargé

**Solutions :**
- Utiliser `/chat_streaming` au lieu de `/chat`
- Augmenter la taille du cache
- Utiliser les audios pré-enregistrés pour les messages fréquents

---

## 📊 Statistiques du Projet

- **Lignes de code** : ~2500 lignes Python
- **Endpoints API** : 7
- **Personnalités** : 16 combinaisons (4×4)
- **Émotions** : 9
- **Audios pré-enregistrés** : 28 fichiers
- **Modèle LLM** : Llama 3.1 8B(Groq)
- **Modèle STT** : Whisper Large V3 (Groq)
- **Modèle TTS** : Piper fr_FR-siwis-medium

---

## 📚 Documentation Complémentaire

- [PERSONNALITES.md](PERSONNALITES.md) - Détails sur le système de personnalité
- [INSTALLATION_PIPER.md](INSTALLATION_PIPER.md) - Guide d'installation de Piper
- [ETAPE_7_TTS.md](ETAPE_7_TTS.md) - Intégration du TTS
- [ETAPE_9_LATENCE.md](ETAPE_9_LATENCE.md) - Optimisation de la latence
- [CORRECTION_DISCOURS.md](CORRECTION_DISCOURS.md) - Corrections récentes

---

## 🔄 Mises à Jour Récentes

### Version 2.0.1 (Actuelle)

✅ **Correction** : Le robot ne parle plus deux fois  
✅ **Amélioration** : Réponses de longueur variable (courtes ou longues selon contexte)  
✅ **Amélioration** : Débit de parole plus lent et naturel  
✅ **Amélioration** : max_tokens augmenté (200 → 500)

Voir [CORRECTION_DISCOURS.md](CORRECTION_DISCOURS.md) pour plus de détails.

---

<div align="center">

**Backend si-3abess - Fait avec ❤️ en Python**

[⬆ Retour en haut](#-si-3abess-backend---fastapi)

</div>
