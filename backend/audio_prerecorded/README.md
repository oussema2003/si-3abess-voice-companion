# 🎙️ Audios pré-enregistrés

Ce dossier contient les audios générés automatiquement au démarrage du serveur.

## 📦 Contenu

**28 fichiers WAV** (4 caractères × 7 audios) :

### Par caractère

#### Timide
- `timide_accueil_0.wav` - Message d'accueil
- `timide_secours_0.wav` - Phrase de secours 1
- `timide_secours_1.wav` - Phrase de secours 2
- `timide_secours_2.wav` - Phrase de secours 3
- `timide_attente_0.wav` - Son d'attente 1 ("Euh...")
- `timide_attente_1.wav` - Son d'attente 2 ("Hmm...")
- `timide_attente_2.wav` - Son d'attente 3 ("Oh...")

#### Joueur
- `joueur_accueil_0.wav` - Message d'accueil
- `joueur_secours_0.wav` - Phrase de secours 1
- `joueur_secours_1.wav` - Phrase de secours 2
- `joueur_secours_2.wav` - Phrase de secours 3
- `joueur_attente_0.wav` - Son d'attente 1 ("Hmm !")
- `joueur_attente_1.wav` - Son d'attente 2 ("Ah !")
- `joueur_attente_2.wav` - Son d'attente 3 ("Oh oh !")

#### Sage
- `sage_accueil_0.wav` - Message d'accueil
- `sage_secours_0.wav` - Phrase de secours 1
- `sage_secours_1.wav` - Phrase de secours 2
- `sage_secours_2.wav` - Phrase de secours 3
- `sage_attente_0.wav` - Son d'attente 1 ("Hmm...")
- `sage_attente_1.wav` - Son d'attente 2 ("Je vois...")
- `sage_attente_2.wav` - Son d'attente 3 ("Intéressant...")

#### Farceur
- `farceur_accueil_0.wav` - Message d'accueil
- `farceur_secours_0.wav` - Phrase de secours 1
- `farceur_secours_1.wav` - Phrase de secours 2
- `farceur_secours_2.wav` - Phrase de secours 3
- `farceur_attente_0.wav` - Son d'attente 1 ("Haha !")
- `farceur_attente_1.wav` - Son d'attente 2 ("Oh là là...")
- `farceur_attente_2.wav` - Son d'attente 3 ("Hmm hmm...")

## 🔄 Génération

Les fichiers sont générés automatiquement :
- **Au démarrage du serveur** : `python main.py`
- **Manuellement** : `python prerecorded_audio.py`

Si un fichier existe déjà, il est réutilisé (pas de régénération).

## 🎯 Utilisation

Ces audios sont utilisés pour :

1. **Masquer la latence** : Jouer un son instantanément pendant que le LLM génère la réponse
2. **Feedback immédiat** : L'utilisateur sait que si-3abess a entendu
3. **Fallback** : En cas d'erreur du TTS ou du LLM
4. **Variété** : 3 variations de chaque type pour éviter la répétition

## 📊 Tailles

| Type | Durée typique | Taille typique |
|------|---------------|----------------|
| Accueil | 2-3s | ~100-120 KB |
| Secours | 1.5-4s | ~60-180 KB |
| Attente | 0.5-1s | ~20-40 KB |

**Total** : ~2-3 MB pour les 28 fichiers

## 🧹 Maintenance

### Régénérer tous les audios

```bash
# Supprimer le cache
Remove-Item *.wav -Force

# Relancer le serveur
python main.py
```

### Vérifier les audios

```bash
python prerecorded_audio.py
```

## ⚠️ Important

- **Ne pas commiter** les fichiers WAV dans Git (trop gros)
- Ajouté à `.gitignore` : `audio_prerecorded/*.wav`
- Chaque développeur doit générer ses propres audios
- Les fichiers sont créés automatiquement au premier démarrage
