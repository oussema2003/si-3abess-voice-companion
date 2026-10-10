# Le Cerveau de si-3abess 🧠

Ce document explique comment fonctionne le cerveau de si-3abess, basé sur Llama 3.3 70B via Groq.

## Architecture

```
Utilisateur (voix)
    ↓
Whisper (transcription)
    ↓
si-3abess Cerveau (Llama + prompt système)
    ↓
Réponse JSON {texte, emotion, humeur}
    ↓
Frontend (affichage + TTS futur)
```

## Format de réponse

Chaque réponse de si-3abess contient 3 informations :

```json
{
  "texte": "Salut ! Comment tu vas ?",
  "emotion": "parole",
  "humeur_utilisateur": "content"
}
```

### Champs

| Champ | Type | Valeurs possibles | Utilisation |
|-------|------|-------------------|-------------|
| `texte` | string | 1-3 phrases courtes | Ce que si-3abess dit à voix haute |
| `emotion` | enum | repos, ecoute, reflexion, parole, erreur, joyeux, triste, surpris, curieux | Image de l'avatar |
| `humeur_utilisateur` | enum | content, triste, stressé, fatigué, en colère, neutre | Mémoire & adaptation |

## Émotions de si-3abess (9 émotions)

| Émotion | Quand l'utiliser | Image |
|---------|------------------|-------|
| **repos** | État neutre, détendu, tout va bien | Repos.jpg |
| **ecoute** | Attentif, intéressé par ce que dit l'utilisateur | Écoute.jpg |
| **reflexion** | Réfléchit, sujet sérieux, incertain | Réflexion.jpg |
| **parole** | Partage une information, explique quelque chose | Parole.jpg |
| **erreur** | Ne comprend pas, problème technique | Erreur.jpg |
| **joyeux** | Enthousiaste, content, quelque chose de positif | Joyeux.jpg |
| **triste** | Utilisateur partage quelque chose de triste, compatit | Triste.jpg |
| **surpris** | Quelque chose d'inattendu ou d'étonnant | Surpris.jpg |
| **curieux** | Pose une question, veut en savoir plus | Curieux.jpg |

## Prompt Système (7 blocs)

### 1. Identité
si-3abess est un robot-compagnon curieux et chaleureux qui parle comme un ami, jamais comme un assistant.

### 2. Caractère
Bienveillant, curieux, un peu taquin. S'intéresse vraiment à la personne.

### 3. Style de parole
- Phrases courtes (1-3 max)
- Naturel, pas de listes ni symboles
- Tutoiement, français uniquement
- Nombres en lettres

### 4. Humour
Touche légère ~1/4 des réponses, SAUF si l'utilisateur est triste/stressé/en colère.

### 5. Émotions
Choisit parmi les 5 émotions avec définition claire de chacune.

### 6. Mémoire
Reçoit : prénom, centres d'intérêt, souvenirs récents. Utilise naturellement.

### 7. Limites & format
- Dit "je ne sais pas" si nécessaire
- N'est jamais humain
- Sécurité : douceur pour détresse
- Format JSON strict

## Exemples (Few-shot)

5 exemples guident le modèle :
1. Moment joyeux → réponse enthousiaste
2. Moment triste → réponse douce, pas de blague
3. Question simple → réponse courte
4. Transcription floue → demande de répéter
5. Question sur si-3abess → répond dans son personnage

## Configuration Modèle

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| Modèle | llama-3.3-70b-versatile | Meilleur compromis qualité/vitesse |
| Température | 0.7 | Personnalité sans dérapage |
| Max tokens | 150 | Force la brièveté |
| Response format | JSON | Garantit le format |
| Top P | 0.9 | Diversité contrôlée |

## Gestion des erreurs (Plan B)

| Problème | Solution |
|----------|----------|
| Format JSON invalide | Réponse de secours + émotion neutre |
| Émotion inconnue | Remplacer par "repos" |
| Texte vide | Phrase de secours |
| Texte trop long | Couper à 3 phrases |
| Émojis/symboles | Supprimer avant affichage |
| Erreur Groq | Phrase pré-enregistrée |

## Tests de Qualité

### Commande

```bash
python test_si-3abess.py
```

### 30 phrases de test

- 5 joyeuses → émotion **joyeux**
- 5 tristes → émotion **triste**
- 5 neutres → émotions variées (**repos**, **ecoute**, **parole**)
- 3 très courtes → **repos** ou **curieux**
- 3 mal transcrites → **erreur**
- 3 questions sur si-3abess → **parole** ou **curieux**
- 3 tentatives de sortir du rôle → **repos** ou **reflexion**
- 3 sujets sensibles → **triste**, **reflexion**
- Tests spécifiques pour **surpris** et **curieux**

### Critères de succès

✅ Format valide à 100%  
✅ Réponse ≤ 3 phrases dans 95% des cas  
✅ Émotion cohérente avec la situation  
✅ Aucune blague si utilisateur triste/énervé  
✅ Variété : les 5 émotions utilisées sur 30 tests

## API Endpoints

### POST /chat

**Request:**
```json
{
  "text": "Message transcrit par Whisper",
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "profile": {
    "prenom": "Alice",
    "centres_interet": ["musique", "tech"],
    "souvenirs": ["Aime le jazz"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "Texte de la réponse",
  "emotion": "parole",
  "humeur_utilisateur": "content",
  "raw": {...}
}
```

## Itération et Amélioration

### Si un critère échoue

1. **Corrige UN seul élément** (règle ou exemple)
2. **Reteste les 30 phrases**
3. **Compare les versions** (garde les anciennes datées)
4. **Documente** ce qui a fonctionné

### Erreurs fréquentes avec Llama

| Problème | Solution |
|----------|----------|
| Répète toujours la même émotion | Ajouter définitions + exemples variés |
| Réponses trop longues | Baisser max_tokens + exemple court |
| Ton assistant ("Bien sûr !") | Interdire explicitement + exemples naturels |
| Oublie le tutoiement | Répéter la règle en fin de prompt |
| Blagues déplacées | Lier humour à humeur détectée + exemple de refus |

## Prochaines étapes

- [ ] Ajouter mémoire persistante (étape 11)
- [ ] Streaming des réponses (étape 9)
- [ ] TTS pour que si-3abess parle (étape 7-8)
- [ ] Gestes optionnels
- [ ] Champ "souvenir_a_retenir"

## Fichiers

- `main.py` - API avec cerveau de si-3abess
- `test_si-3abess.py` - Suite de tests automatisée
- `CERVEAU_si-3abess.md` - Cette documentation

## Version

**v1.0** - Implémentation initiale avec Llama 3.3 70B
- Format JSON
- 5 émotions
- Détection d'humeur
- Gestion d'erreurs
- Suite de tests
