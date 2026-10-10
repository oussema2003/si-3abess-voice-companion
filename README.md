# 🤖 si-3abess - Robot Compagnon Intelligent

<div align="center">

![si-3abess Robot](backend/robo%20émotions/Joyeux.jpg)

**Un assistant vocal intelligent avec personnalité, émotions et voix naturelle**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-API-orange.svg)](https://groq.com/)
[![Piper TTS](https://img.shields.io/badge/Piper-TTS-purple.svg)](https://github.com/rhasspy/piper)

</div>

---

## 📋 Table des Matières

- [Présentation](#-présentation)
- [Caractéristiques](#-caractéristiques)
- [Les 9 Émotions de si-3abess](#-les-9-émotions-de-si-3abess)
- [Les 4 Personnalités](#-les-4-personnalités)
- [Les 4 Publics Cibles](#-les-4-publics-cibles)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Endpoints](#-api-endpoints)
- [Exemples de Conversations](#-exemples-de-conversations)
- [Développement](#-développement)
- [Dépannage](#-dépannage)
- [Contribuer](#-contribuer)
- [Licence](#-licence)

---

## 🎯 Présentation

**si-3abess** est un robot compagnon vocal intelligent qui combine :
- 🧠 **Intelligence artificielle** (Llama 3.1 8B via Groq)
- 🎤 **Reconnaissance vocale** (Whisper)
- 🔊 **Synthèse vocale naturelle** (Piper TTS)
- 😊 **9 expressions émotionnelles**
- 🎭 **4 personnalités distinctes**
- 👥 **4 modes adaptés aux différents publics**

si-3abess peut avoir des **conversations longues et naturelles**, s'adapter à votre humeur, et répondre avec des émotions visuelles et vocales cohérentes.

---

## ✨ Caractéristiques

### 🎭 Système de Personnalité Modulaire
- **4 caractères** : Timide, Joueur, Sage, Farceur
- **4 publics** : Jeunes, Adultes, Seniors, Tout le monde
- **16 combinaisons possibles** pour s'adapter à chaque utilisateur

### 😊 Système d'Émotions
- **9 émotions visuelles** avec images associées
- **Détection de l'humeur** de l'utilisateur
- **Adaptation émotionnelle** en temps réel

### 🎙️ Traitement Vocal Avancé
- **Transcription** : Groq Whisper (large-v3)
- **Synthèse vocale** : Piper TTS en français
- **Débit adaptatif** : Chaque personnalité a sa vitesse de parole
- **Cache audio** : Réponses rapides pour les phrases fréquentes

### 🚀 Performance Optimisée
- **Latence réduite** : < 2 secondes pour la première réponse
- **Streaming** : Réponses progressives phrase par phrase
- **Audios pré-enregistrés** : Messages d'accueil et de secours

### 💾 Mémoire Contextuelle
- **Historique de conversation** : Jusqu'à 20 messages récents
- **Profil utilisateur** : Prénom, centres d'intérêt, souvenirs
- **Continuité** : si-3abess se souvient de vos échanges

---

## 😊 Les 9 Émotions de si-3abess

si-3abess exprime 9 émotions différentes avec des visages animés et des expressions vocales adaptées.

### 1. 😌 Repos
<img src="backend/robo émotions/Repos.jpg" width="150" alt="Repos">

**Quand ?** État neutre et détendu, quand tout va bien  
**Utilisation** : Réponses neutres, état par défaut  
**Exemple** : _"Je suis là si tu as besoin de parler."_

---

### 2. 👂 Écoute
<img src="backend/robo émotions/Écoute.jpg" width="150" alt="Écoute">

**Quand ?** Attentif et intéressé par ce que dit l'utilisateur  
**Utilisation** : Quand l'utilisateur partage quelque chose d'important  
**Exemple** : _"Je t'écoute, raconte-moi."_

---

### 3. 🤔 Réflexion
<img src="backend/robo émotions/Réflexion.jpg" width="150" alt="Réflexion">

**Quand ?** En train de réfléchir ou sujet sérieux  
**Utilisation** : Questions complexes, sujets profonds  
**Exemple** : _"Laisse-moi réfléchir à ça..."_

---

### 4. 💬 Parole
<img src="backend/robo émotions/Parole.jpg" width="150" alt="Parole">

**Quand ?** Partage une information ou explique quelque chose  
**Utilisation** : Explications, partage de connaissances  
**Exemple** : _"Je vais t'expliquer comment ça fonctionne."_

---

### 5. ❌ Erreur
<img src="backend/robo émotions/Erreur.jpg" width="150" alt="Erreur">

**Quand ?** Ne comprend pas ou problème technique  
**Utilisation** : Incompréhension, bugs, erreurs  
**Exemple** : _"Oups, je n'ai pas bien compris. Tu peux répéter ?"_

---

### 6. 😄 Joyeux
<img src="backend/robo émotions/Joyeux.jpg" width="150" alt="Joyeux">

**Quand ?** Enthousiaste, content, quelque chose de positif  
**Utilisation** : Bonnes nouvelles, moments joyeux  
**Exemple** : _"Génial ! Je suis trop content pour toi !"_

---

### 7. 😢 Triste
<img src="backend/robo émotions/Triste.jpg" width="150" alt="Triste">

**Quand ?** L'utilisateur partage quelque chose de triste  
**Utilisation** : Compassion, empathie, soutien  
**Exemple** : _"Je comprends, c'est difficile. Je suis là pour toi."_

---

### 8. 😲 Surpris
<img src="backend/robo émotions/Surpris.jpg" width="150" alt="Surpris">

**Quand ?** Quelque chose d'inattendu ou d'étonnant  
**Utilisation** : Révélations, nouvelles surprenantes  
**Exemple** : _"Quoi ? Vraiment ? C'est incroyable !"_

---

### 9. 🤨 Curieux
<img src="backend/robo émotions/Curieux.jpg" width="150" alt="Curieux">

**Quand ?** Pose une question ou veut en savoir plus  
**Utilisation** : Questions de suivi, curiosité  
**Exemple** : _"Dis-moi en plus, ça m'intéresse !"_

---

## 🎭 Les 4 Personnalités

si-3abess peut adopter 4 caractères différents pour s'adapter à vos préférences.

### 1. 😊 Timide

<table>
<tr>
<td width="30%"><img src="backend/robo émotions/Repos.jpg" width="150"></td>
<td width="70%">

**Caractéristiques :**
- 🗣️ **Ton** : Doux, hésitant, attentif
- 💬 **Style** : Utilise "euh...", "je crois que...", s'excuse facilement
- 😄 **Humour** : Rare et très discret
- 🎤 **Voix** : Très lente (vitesse 0.75) et douce (volume 0.8)
- 😊 **Émotions fréquentes** : repos, curieux, surpris

**Exemple de réponse :**
> _"Euh... bonjour. Je suis content de te parler. Tu vas bien ?"_

</td>
</tr>
</table>

---

### 2. 🎮 Joueur

<table>
<tr>
<td width="30%"><img src="backend/robo émotions/Joyeux.jpg" width="150"></td>
<td width="70%">

**Caractéristiques :**
- 🗣️ **Ton** : Énergique, enthousiaste
- 💬 **Style** : Propose des jeux, devinettes, défis
- 😄 **Humour** : Fréquent (~1/3 des réponses)
- 🎤 **Voix** : Légèrement rapide (vitesse 0.95), volume normal
- 😊 **Émotions fréquentes** : joyeux, curieux, parole

**Exemple de réponse :**
> _"Salut ! Je suis si-3abess, ton robot-compagnon ! Tu veux qu'on fasse un jeu ?"_

</td>
</tr>
</table>

---

### 3. 🧘 Sage

<table>
<tr>
<td width="30%"><img src="backend/robo émotions/Réflexion.jpg" width="150"></td>
<td width="70%">

**Caractéristiques :**
- 🗣️ **Ton** : Calme, posé, bienveillant
- 💬 **Style** : Images simples, aide à réfléchir, petites histoires
- 😄 **Humour** : Fin et rare
- 🎤 **Voix** : Très lente (vitesse 0.7), grave et posée
- 😊 **Émotions fréquentes** : repos, reflexion, curieux

**Exemple de réponse :**
> _"Bonjour à toi. Je m'appelle si-3abess. Comment te sens-tu aujourd'hui ?"_

</td>
</tr>
</table>

---

### 4. 😄 Farceur

<table>
<tr>
<td width="30%"><img src="backend/robo émotions/Surpris.jpg" width="150"></td>
<td width="70%">

**Caractéristiques :**
- 🗣️ **Ton** : Taquin, blagues gentilles
- 💬 **Style** : Jeux de mots, taquineries (~1/2 des réponses)
- 😄 **Humour** : Très fréquent SAUF si personne triste/stressée
- 🎤 **Voix** : Modérée (vitesse 0.9), expressive
- 😊 **Émotions fréquentes** : joyeux, surpris, parole

**Exemple de réponse :**
> _"Hey ! Moi c'est si-3abess, prêt pour l'aventure ? Attention, mes blagues sont pourries !"_

**⚠️ Note importante** : Le Farceur ne fait JAMAIS de blague si l'utilisateur est triste, stressé ou en colère.

</td>
</tr>
</table>

---

## 👥 Les 4 Publics Cibles

si-3abess adapte son langage et son comportement selon le public.

### 1. 👶 Jeunes (10-18 ans)

**Caractéristiques :**
- 📚 **Vocabulaire** : Simple et clair
- 📝 **Phrases** : Courtes (1-3 phrases maximum)
- 🎨 **Ton** : Doux, encourageant, patient
- 🔒 **Sécurité renforcée** :
  - ❌ Aucun sujet effrayant/violent/adulte
  - ❌ Ne demande JAMAIS d'infos privées (nom complet, adresse, école)
  - ⚠️ Si danger → encourage à parler à un adulte de confiance

**Exemple :**
> _"Oh, tu as l'air triste. Tu veux me raconter ce qui s'est passé ? Si c'est grave, tu peux en parler à tes parents."_

---

### 2. 🎒 Adultes (18-65 ans)

**Caractéristiques :**
- 📚 **Vocabulaire** : Naturel et décontracté
- 💬 **Ton** : Cool, sans jugement, sans morale
- 🤝 **Respect** : Ne pas infantiliser
- 🔒 **Sécurité** :
  - ⚠️ Vigilance sur détresse, harcèlement, danger
  - 💬 Encourage à parler à un adulte de confiance si besoin

**Exemple :**
> _"Ah, je comprends. C'est pas facile parfois. Tu veux en parler ou tu préfères qu'on change de sujet ?"_

---

### 3. 👔 Seniors (65+ ans)

**Caractéristiques :**
- 📚 **Vocabulaire** : Mature et varié
- 💬 **Sujets** : Tous types, avec nuances
- ⚠️ **Limites** : Pas de conseils médicaux/juridiques/financiers professionnels
- 🤝 **Ton** : Égal à égal, respectueux

**Exemple :**
> _"Je comprends votre situation. C'est complexe et il n'y a pas de réponse simple. Qu'est-ce qui vous préoccupe le plus ?"_

---

### 4. 🌍 Tout le monde (10-100 ans)

**Caractéristiques :**
- ⚙️ **Mode universel** : Pour tous les âges de 10 à 100 ans
- 📚 **Vocabulaire** : Clair, simple, universel
- 📝 **Contenu** : Adapté à un adolescent (niveau de sécurité)
- ❌ **Pas de** : Sujets adultes, violents ou sensibles

**Exemple :**
> _"Bonjour ! Je suis si-3abess, ton compagnon robot. Comment puis-je t'aider aujourd'hui ?"_

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend (Interface)               │
│         (Web / Mobile / Application)            │
└────────────┬────────────────────────────────────┘
             │
             │ HTTP/REST API
             │
┌────────────▼────────────────────────────────────┐
│           Backend FastAPI                       │
│  ┌──────────────────────────────────────┐      │
│  │  main.py - API principale            │      │
│  │  • /transcribe - Audio → Texte       │      │
│  │  • /chat - Conversation complète     │      │
│  │  • /chat_streaming - Streaming       │      │
│  │  • /synthesize - TTS direct          │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │  si_3abess_personality.py                 │      │
│  │  • Système modulaire de personnalité │      │
│  │  • 16 combinaisons (4×4)             │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │  piper_tts.py                        │      │
│  │  • Synthèse vocale française         │      │
│  │  • Cache audio                       │      │
│  │  • Voix adaptées par caractère       │      │
│  └──────────────────────────────────────┘      │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │  prerecorded_audio.py                │      │
│  │  • Audios pré-enregistrés            │      │
│  │  • Messages d'accueil et secours     │      │
│  └──────────────────────────────────────┘      │
└──────────┬───────────────────┬───────────────────┘
           │                   │
           │                   │
┌──────────▼─────────┐  ┌──────▼────────────┐
│   Groq API         │  │   Piper TTS       │
│  • Whisper (STT)   │  │  • fr_FR-siwis    │
│  • Llama 3.1 8B    │  │  • Synthèse local │
└────────────────────┘  └───────────────────┘
```

### Flux de Conversation Typique

```
1. 🎤 Utilisateur parle
   └─> Enregistrement audio (WebM/WAV)

2. 📝 Transcription
   └─> Groq Whisper → Texte

3. 🧠 Traitement
   ├─> Analyse du contexte
   ├─> Détection de l'humeur
   ├─> Application de la personnalité
   └─> Génération de la réponse (Groq LLM)

4. 😊 Émotion
   └─> Sélection de l'émotion appropriée

5. 🔊 Synthèse vocale
   └─> Piper TTS → Audio WAV

6. 📱 Retour utilisateur
   ├─> Texte de la réponse
   ├─> Image de l'émotion
   └─> Audio de la voix
```

---

## 🚀 Installation

### Prérequis

- **Python 3.8+**
- **Pip** (gestionnaire de paquets Python)
- **Compte Groq** avec clé API (gratuit)
- **Windows, Linux ou macOS**

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/[VOTRE_USERNAME]/si-3abess-robot.git
cd si-3abess-robot
```

### Étape 2 : Créer un environnement virtuel

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Windows :
venv\Scripts\activate

# Linux/Mac :
source venv/bin/activate
```

### Étape 3 : Installer les dépendances

```bash
cd backend
pip install -r requirements.txt
```

### Étape 4 : Installer Piper TTS

**Option 1 : Via pip**
```bash
pip install piper-tts
```

**Option 2 : Installation manuelle**  
Suivez le guide : [INSTALLATION_PIPER.md](backend/INSTALLATION_PIPER.md)

### Étape 5 : Télécharger le modèle vocal français

```bash
# Le modèle est déjà inclus dans backend/piper/
# Si besoin de le retélécharger :
cd backend/piper
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json
```

---

## ⚙️ Configuration

### 1. Créer le fichier `.env`

À la racine du projet, créez un fichier `.env` :

```bash
cp .env.example .env
```

### 2. Configurer la clé API Groq

Éditez le fichier `.env` :

```env
# Clé API Groq (obligatoire)
GROQ_API_KEY=gsk_votre_cle_api_ici

# Configuration optionnelle
PIPER_MODEL_PATH=backend/piper/fr_FR-siwis-medium.onnx
AUDIO_CACHE_DIR=backend/tts_cache
PRERECORDED_AUDIO_DIR=backend/audio_prerecorded
```

### 3. Obtenir une clé API Groq (gratuit)

1. Allez sur [https://console.groq.com](https://console.groq.com)
2. Créez un compte (gratuit)
3. Allez dans "API Keys"
4. Créez une nouvelle clé
5. Copiez-la dans votre fichier `.env`

---

## 🎮 Utilisation

### Démarrer le serveur

```bash
cd backend
python main.py
```

Le serveur démarre sur **http://localhost:3000**

### Vérifier que tout fonctionne

```bash
# Test de santé
curl http://localhost:3000/health

# Réponse attendue :
# {"status": "healthy", "groq_configured": true}
```

### Mode développement (auto-reload)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

---

## 📡 API Endpoints

### 1. 🏠 GET `/` - Page d'accueil

Informations sur l'API.

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

### 2. ❤️ GET `/health` - Santé du serveur

Vérifier l'état du serveur.

**Réponse :**
```json
{
  "status": "healthy",
  "groq_configured": true
}
```

---

### 3. 🎙️ POST `/transcribe` - Transcription audio

Convertir un fichier audio en texte.

**Requête :**
```bash
curl -X POST http://localhost:3000/transcribe \
  -F "audio=@monAudio.webm"
```

**Réponse :**
```json
{
  "success": true,
  "text": "Bonjour si-3abess, comment ça va ?",
  "language": "fr",
  "model": "whisper-large-v3"
}
```

---

### 4. 💬 POST `/chat` - Conversation complète

Envoyer un message et recevoir une réponse complète avec audio.

**Requête :**
```json
{
  "text": "Bonjour si-3abess !",
  "caractere": "joueur",
  "public": "tout_le_monde",
  "history": [],
  "profile": {
    "prenom": "Thomas",
    "centres_interet": ["technologie", "musique"],
    "souvenirs": []
  }
}
```

**Réponse :**
```json
{
  "success": true,
  "response": "Salut Thomas ! Je suis trop content de te parler ! Tu vas bien ?",
  "emotion": "joyeux",
  "humeur_utilisateur": "content",
  "audio_chunks": [
    {
      "index": 0,
      "audio": "base64_encoded_audio...",
      "duration": 3.2,
      "text": "Salut Thomas ! Je suis trop content de te parler ! Tu vas bien ?",
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

### 5. 🚀 POST `/chat_streaming` - Conversation en streaming

Version optimisée avec streaming pour latence réduite.

**Requête :** Identique à `/chat`

**Réponse :** Identique à `/chat` mais avec métriques de performance

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

### 6. 🔊 POST `/synthesize` - Synthèse vocale directe

Convertir du texte en audio (TTS).

**Requête :**
```json
{
  "text": "Bonjour, je suis si-3abess !",
  "caractere": "sage"
}
```

**Réponse :** Fichier audio WAV

---

### 7. 📋 GET `/personnalites` - Liste des personnalités

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

## 💬 Exemples de Conversations

### Exemple 1 : Timide + Jeunes

**Utilisateur :** "Bonjour si-3abess !"  
**si-3abess :** 😊 _"Euh... bonjour. Je suis content de te voir."_  
**Émotion :** `repos`

**Utilisateur :** "Tu veux jouer avec moi ?"  
**si-3abess :** 🤨 _"Oh... oui, je veux bien. À quoi tu veux jouer ?"_  
**Émotion :** `curieux`

---

### Exemple 2 : Joueur + Adultes

**Utilisateur :** "Salut, t'es qui ?"  
**si-3abess :** 😄 _"Salut ! Moi c'est si-3abess, ton pote robot ! Prêt pour une super discussion ?"_  
**Émotion :** `joyeux`

**Utilisateur :** "J'ai eu une mauvaise note en maths..."  
**si-3abess :** 😢 _"Aïe, c'est pas cool ça. Tu veux en parler ou tu préfères qu'on se change les idées ?"_  
**Émotion :** `triste`

---

### Exemple 3 : Sage + Seniors

**Utilisateur :** "Comment fonctionnent les robots comme toi ?"  
**si-3abess :** 💬 _"Les robots comme moi fonctionnent grâce à des circuits électroniques et des programmes informatiques. C'est un peu comme un cerveau, mais en version numérique. On peut apprendre, se souvenir de choses, et analyser les situations. Mon intelligence vient de modèles d'apprentissage qui ont été entraînés sur d'énormes quantités de données. C'est fascinant, vous ne trouvez pas ?"_  
**Émotion :** `parole`

---

### Exemple 4 : Farceur + Tout le monde

**Utilisateur :** "Tu connais des blagues ?"  
**si-3abess :** 😄 _"Oh que oui ! Pourquoi les robots n'ont jamais peur ? Parce qu'ils ont des nerfs d'acier ! Ha ha !"_  
**Émotion :** `joyeux`

**Utilisateur :** "Je suis triste aujourd'hui..."  
**si-3abess :** 😢 _"Oh... je suis désolé. Qu'est-ce qui ne va pas ? Je suis là pour t'écouter."_  
**Émotion :** `triste`  
**Note :** Pas de blague car l'utilisateur est triste

---

## 🛠️ Développement

### Structure du projet

```
si-3abess-robot/
├── backend/
│   ├── audio_prerecorded/      # Audios pré-enregistrés
│   │   ├── farceur_accueil_0.wav
│   │   ├── joueur_secours_1.wav
│   │   └── ...
│   ├── piper/                   # Modèles Piper TTS
│   │   ├── fr_FR-siwis-medium.onnx
│   │   └── fr_FR-siwis-medium.onnx.json
│   ├── robo émotions/          # Images des émotions
│   │   ├── Repos.jpg
│   │   ├── Joyeux.jpg
│   │   ├── Triste.jpg
│   │   └── ... (9 émotions)
│   ├── tts_cache/              # Cache audio (généré)
│   ├── main.py                 # API principale
│   ├── si_3abess_personality.py     # Système de personnalité
│   ├── piper_tts.py           # Synthèse vocale
│   ├── prerecorded_audio.py   # Gestion audios pré-enregistrés
│   ├── streaming_chat.py       # Chat avec streaming
│   ├── performance_monitor.py  # Monitoring performance
│   ├── requirements.txt        # Dépendances Python
│   └── README.md              # Documentation backend
├── .env                        # Configuration (non versionné)
├── .env.example               # Exemple de configuration
├── .gitignore                 # Fichiers ignorés par Git
└── README.md                  # Ce fichier
```

### Tests

```bash
# Tester les 4 personnalités
python backend/test_personnalites.py

# Tester la synthèse vocale
python backend/test_tts.py

# Tester Piper directement
python backend/test_piper_direct.py

# Tester les audios pré-enregistrés
python backend/prerecorded_audio.py
```

### Créer de nouveaux audios pré-enregistrés

1. Modifier le fichier `backend/demo_voix.py`
2. Lancer la génération :
```bash
python backend/demo_voix.py
```
3. Les audios seront générés dans `backend/audio_prerecorded/`

### Ajouter une nouvelle émotion

1. Ajouter l'image dans `backend/robo émotions/NouvelleEmotion.jpg`
2. Mettre à jour la liste des émotions dans `main.py` :
```python
emotions_valides = ["repos", "ecoute", "reflexion", "parole", 
                   "erreur", "joyeux", "triste", "surpris", 
                   "curieux", "nouvelle_emotion"]
```
3. Mettre à jour le prompt système pour expliquer quand utiliser cette émotion

---

## 🐛 Dépannage

### Problème : "GROQ_API_KEY n'est pas définie"

**Solution :**
1. Vérifiez que le fichier `.env` existe à la racine
2. Vérifiez que la clé est bien définie : `GROQ_API_KEY=gsk_...`
3. Redémarrez le serveur

---

### Problème : "Piper non disponible"

**Solution :**
```bash
pip install piper-tts
```

Si ça ne fonctionne pas, consultez [INSTALLATION_PIPER.md](backend/INSTALLATION_PIPER.md)

---

### Problème : Audio silencieux ou pas d'audio

**Causes possibles :**
1. Piper TTS non installé → Mode silencieux activé
2. Modèle vocal manquant → Retélécharger le modèle
3. Cache corrompu → Supprimer `backend/tts_cache/`

**Solution :**
```bash
# Vérifier Piper
python backend/test_piper_simple.py

# Supprimer le cache
rm -rf backend/tts_cache/*
```

---

### Problème : Le robot parle deux fois

**Solution :** Ce problème a été corrigé. Assurez-vous d'utiliser la dernière version :
```bash
git pull origin main
```

Voir [CORRECTION_DISCOURS.md](backend/CORRECTION_DISCOURS.md) pour plus de détails.

---

### Problème : Réponses trop courtes

**Solution :** Les réponses sont maintenant adaptatives. Si vous voulez forcer des réponses plus longues :
1. Posez des questions qui nécessitent des explications
2. Demandez "Explique-moi en détail..."
3. Utilisez la personnalité "Sage" qui tend à développer davantage

---

### Problème : Latence élevée (> 5 secondes)

**Solutions :**
1. Utilisez `/chat_streaming` au lieu de `/chat`
2. Vérifiez votre connexion Internet (Groq API)
3. Activez le cache audio (déjà activé par défaut)
4. Utilisez les audios pré-enregistrés pour les messages courants

---

## 🤝 Contribuer

Les contributions sont les bienvenues !

### Comment contribuer

1. **Fork** le projet
2. Créez une **branche** pour votre fonctionnalité
```bash
git checkout -b feature/nouvelle-fonctionnalite
```
3. **Committez** vos changements
```bash
git commit -m "Ajout d'une nouvelle fonctionnalité"
```
4. **Push** vers votre branche
```bash
git push origin feature/nouvelle-fonctionnalite
```
5. Ouvrez une **Pull Request**

### Guidelines

- ✅ Code clair et commenté
- ✅ Tests pour les nouvelles fonctionnalités
- ✅ Documentation à jour
- ✅ Respect de la structure existante

---

## 📄 Licence

Ce projet est un projet personnel. Pour toute utilisation, veuillez contacter l'auteur.

---

## 🙏 Remerciements

- **Groq** pour leur API LLM rapide et gratuite (Llama 3.1 8B)
- **Rhasspy Piper** pour la synthèse vocale française de qualité
- **FastAPI** pour le framework web moderne
- **OpenAI Whisper** (via Groq) pour la transcription vocale

---

## 📞 Contact & Support

Pour toute question ou assistance, vous pouvez :
- 🐛 Ouvrir une issue : [GitHub Issues](https://github.com/[VOTRE_USERNAME]/si-3abess-robot/issues)
- 📖 Consulter la documentation complète dans le dépôt

---

<div align="center">

**Fait avec ❤️ pour créer des interactions humain-robot naturelles**

⭐ Si vous aimez ce projet, donnez-lui une étoile sur GitHub !

</div>
