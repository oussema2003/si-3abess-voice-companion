# Assets si-3abess - Images des émotions

Ce dossier contient les images représentant les différents états émotionnels de si-3abess.

## Images disponibles

| Fichier | État | Utilisation |
|---------|------|-------------|
| `Repos.jpg` | **idle** | si-3abess en attente, état par défaut |
| `Écoute.jpg` | **listening** | si-3abess écoute l'utilisateur (microphone actif) |
| `Réflexion.jpg` | **thinking** | si-3abess réfléchit (traitement en cours) |
| `Parole.jpg` | **speaking** | si-3abess parle (donne une réponse) |
| `Erreur.jpg` | **error** | Erreur de connexion ou problème technique |

## Format

- **Format** : JPG
- **Dimensions recommandées** : 250x250 pixels ou plus
- **Ratio** : Carré ou proche du carré pour un rendu optimal

## Modification

Pour changer les images de si-3abess :
1. Remplacez les fichiers JPG dans ce dossier
2. Gardez les mêmes noms de fichiers
3. Le frontend se rechargera automatiquement

## Correspondance avec le code

Les images sont définies dans `main.js` :

```javascript
const avatarImages = {
    idle: 'assets/Repos.jpg',
    listening: 'assets/Écoute.jpg',
    thinking: 'assets/Réflexion.jpg',
    speaking: 'assets/Parole.jpg',
    error: 'assets/Erreur.jpg'
};
```
