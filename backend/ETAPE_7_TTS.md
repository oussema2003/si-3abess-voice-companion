# Étape 7 : Synthèse Vocale avec Piper 🎤

Cette étape transforme le texte de si-3abess en audio avec une voix adaptée à chaque caractère.

## Trajet du texte vers l'audio

```
┌─────────────────┐
│ Texte validé    │ (Étape 6)
│ de Llama        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Nettoyage du    │ - Abréviations
│ texte           │ - Nombres en lettres
└────────┬────────┘ - Symboles
         │
         ▼
┌─────────────────┐
│ Découpe en      │ - Sur . ! ?
│ phrases         │ - Regroupe courtes
└────────┬────────┘ - Coupe longues
         │
         ▼
┌─────────────────┐
│ Synthèse Piper  │ - Voix par caractère
│ phrase par      │ - Vitesse adaptée
│ phrase          │ - Pitch ajusté
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Streaming vers  │ - Première phrase
│ navigateur      │   immédiate
└────────┬────────┘ - Puis suivantes
         │
         ▼
┌─────────────────┐
│ Lecture +       │ - Bouche animée
│ Animation       │ - Selon volume
└─────────────────┘
```

## Voix sélectionnées

### Pour si-3abess, 2 voix principales :

#### 1. **fr_FR-siwis-medium** 
- **Caractères** : Timide, Sage
- **Qualité** : ⭐⭐⭐⭐ (4/5)
- **Naturel** : Doux, posé
- **Clarté** : Excellente
- **Défauts** : Légère monotonie
- **License** : CC BY-SA 4.0

#### 2. **fr_FR-upmc-medium**
- **Caractères** : Joueur, Farceur
- **Qualité** : ⭐⭐⭐⭐ (4/5)
- **Naturel** : Vif, expressif
- **Clarté** : Très bonne
- **Défauts** : Parfois trop mécanique sur nombres
- **License** : CC BY-SA 4.0

## Configuration par caractère

| Caractère | Voix | Vitesse | Pitch | Volume | Pause |
|-----------|------|---------|-------|--------|-------|
| **Timide** | siwis | 0.9 | 0 | 0.8 | 0.3s |
| **Joueur** | upmc | 1.2 | +2 | 1.0 | 0.2s |
| **Sage** | siwis | 0.85 | -2 | 0.95 | 0.4s |
| **Farceur** | upmc | 1.1 | +1 | 1.0 | 0.25s |

## Nettoyage du texte

### Règles appliquées

| Problème | Solution | Exemple |
|----------|----------|---------|
| Nombres | En lettres | "2026" → "deux mille vingt-six" |
| Abréviations | Développer | "M." → "Monsieur" |
| Sigles | Épeler | "SMS" → "S M S" |
| Émojis | Supprimer | "😊" → "" |
| Points... | Limiter | "....." → "..." |
| MAJUSCULES | Capitaliser | "SUPER" → "Super" |
| Mots étrangers | Dictionnaire | "si-3abess" → "si-3abess" |

### Dictionnaire de prononciation

```python
DICTIONNAIRE_PRONONCIATION = {
    "si-3abess": "si-3abess",
    "Groq": "Grok",
    "M.": "Monsieur",
    "etc.": "et cetera",
    "SMS": "S M S",
    # ... À enrichir avec les tests
}
```

## Découpe en phrases

### Règles

1. **Séparer** sur `.` `!` `?`
2. **Protéger** `M.` `etc.` `Dr.`
3. **Regrouper** les phrases < 10 caractères
4. **Couper** les phrases > 150 caractères sur `,`

### Exemples

```python
Input: "Salut ! Comment ça va ?"
Output: ["Salut !", "Comment ça va ?"]

Input: "Oh. Euh. Je vois."
Output: ["Oh. Euh. Je vois."]  # Regroupé

Input: "Bonjour M. Dupont, comment allez-vous ?"
Output: ["Bonjour M. Dupont, comment allez-vous ?"]  # M. protégé
```

## Streaming phrase par phrase

### Pourquoi ?

- **Objectif** : Première parole en < 700ms
- **Sans streaming** : Attendre toute la synthèse (~2-3s)
- **Avec streaming** : Commence dès la première phrase prête

### Fonctionnement

```python
async for chunk in synthesize_streaming(texte, caractere):
    # chunk = {
    #   "index": 0,
    #   "audio": bytes,
    #   "duration": 1.2,
    #   "phrase": "Salut !",
    #   "is_last": False
    # }
    yield chunk
```

## Phrases pré-enregistrées

### Messages de secours (par caractère)

| Caractère | Phrase | Fichier |
|-----------|--------|---------|
| Timide | "Euh... désolé, j'ai bugé" | `cache/timide_secours_1.wav` |
| Joueur | "Oups ! On réessaie ?" | `cache/joueur_secours_1.wav` |
| Sage | "Pardonne-moi..." | `cache/sage_secours_1.wav` |
| Farceur | "Ah là là, bug !" | `cache/farceur_secours_1.wav` |

### Messages d'accueil

| Caractère | Message |
|-----------|---------|
| Timide | "Euh... bonjour. Je suis si-3abess." |
| Joueur | "Salut ! Je suis si-3abess !" |
| Sage | "Bonjour à toi. Je m'appelle si-3abess." |
| Farceur | "Hey ! Moi c'est si-3abess !" |

### Petits sons

- "hmm" (réflexion)
- "oh" (surprise)
- "ah" (compréhension)
- "euh" (hésitation)

**Avantages** :
- ⚡ Réponse instantanée
- 🛡️ Fonctionne même si Piper plante
- 💰 Aucun coût de calcul

## Animation de la bouche

### Méthode simple (v1)

1. **Analyser** le volume de l'audio en temps réel
2. **Seuil** : Si volume > 30% → bouche ouverte
3. **Délai** : Maintenir 80ms pour éviter clignotement
4. **Images** : Alterner `Parole.jpg` et `Parole_bouche_ouverte.jpg`

### Algorithme

```javascript
let bouche_ouverte = false;
let dernier_changement = 0;

function analyzeAudio(volume) {
    const now = Date.now();
    
    if (volume > 0.3 && !bouche_ouverte) {
        if (now - dernier_changement > 80) {
            setBoucheOuverte(true);
            dernier_changement = now;
        }
    } else if (volume < 0.2 && bouche_ouverte) {
        if (now - dernier_changement > 80) {
            setBoucheFermee(true);
            dernier_changement = now;
        }
    }
}
```

## Interruption

Quand l'utilisateur parle pendant que si-3abess parle :

1. **Navigateur** : Vider la file d'attente audio
2. **Serveur** : Arrêter les synthèses en cours
3. **Avatar** : Passer en état "Écoute"
4. **ID** : Ignorer les chunks audio de l'ancienne réponse

```python
# Chaque réponse a un ID unique
response_id = str(uuid.uuid4())

# Le navigateur envoie l'ID actuel
if incoming_chunk.response_id != current_response_id:
    return  # Ignorer
```

## Performances

### Objectifs

- ✅ Premier son en < 700ms
- ✅ Synthèse temps réel : phrase de 3s générée en < 1s
- ✅ Enchaînement sans coupure
- ✅ Support 5 utilisateurs simultanés

### Optimisations

1. **Pré-charger** les modèles au démarrage
2. **Cache** pour phrases fréquentes
3. **File d'attente** pour multi-utilisateurs
4. **Compression** audio pour transfert mobile

### Mesures

```python
import time

start = time.time()
audio = await synthesize_phrase(phrase, caractere)
elapsed = time.time() - start

# Facteur temps réel (RTF)
rtf = elapsed / duration
print(f"RTF: {rtf:.2f}x")  # < 1.0 = plus rapide que temps réel
```

## Tests de l'étape 7

### 1. Test de voix (à l'oreille)

**10 phrases par caractère** :
- [x] Naturel
- [x] Prononciation correcte
- [x] Rythme adapté

**5 phrases avec nombres** :
- "J'ai vingt-trois ans"
- "Il est trois heures quarante-cinq"
- "Ça coûte cent cinquante euros"
- "L'année deux mille vingt-six"
- "Trois virgule quatorze"

**10 prénoms** :
- si-3abess, Marie, Thomas, Amélie, Lucas
- Chloé, Alexandre, Sarah, Nicolas, Emma

**Support** :
- [ ] Téléphone
- [ ] Casque
- [ ] Haut-parleur

### 2. Test technique

- [ ] Temps premier son < 700ms
- [ ] Enchaînement 3 phrases sans coupure
- [ ] Interruption fonctionne
- [ ] 5 utilisateurs simultanés
- [ ] Safari iPhone démarre bien

### 3. Critères de réussite

✅ Premier son en < 700ms  
✅ Aucun mot mal prononcé (30 phrases)  
✅ 4 caractères distinguables à l'oreille  
✅ Bouche suit la parole sans décalage  
✅ Phrases de secours instantanées

## Ce que vous devez avoir

- [x] 2-3 voix françaises retenues + licences
- [x] Profil de réglage par caractère
- [x] Dictionnaire de prononciation
- [x] Règles de nettoyage du texte
- [x] Règles de découpe en phrases
- [ ] Phrases secours pré-enregistrées
- [ ] Images bouche ouverte pour émotions
- [ ] Résultats tests écoute et rapidité

## Fichiers créés

```
backend/
├── tts_manager.py              # Gestionnaire TTS
├── INSTALLATION_PIPER.md       # Guide installation
├── ETAPE_7_TTS.md             # Cette doc
├── test_tts.py                # Tests TTS
└── piper/                     # Dossier Piper
    ├── piper.exe              # Exécutable
    └── voices/                # Modèles voix
        ├── fr_FR-siwis-medium.onnx
        └── fr_FR-upmc-medium.onnx

frontend/
└── public/assets/             # Images émotions
    ├── Parole.jpg            # Bouche fermée
    ├── Parole_open.jpg       # Bouche ouverte (à créer)
    └── ...
```

## Commandes

```bash
# Installer Piper
pip install piper-tts

# Télécharger une voix
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx

# Tester
python test_tts.py

# Pré-enregistrer phrases
python prerecord_phrases.py
```

## Prochaine étape

**Étape 8** : Optimisation de la latence
- Streaming du LLM
- Début de synthèse avant la fin du texte
- Prédiction des prochains mots

## Version

**v2.1.0** - Synthèse vocale avec Piper
- Configuration par caractère
- Nettoyage et découpe intelligente
- Streaming phrase par phrase
- Phrases pré-enregistrées
- Animation bouche
