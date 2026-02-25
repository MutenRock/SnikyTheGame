# SnikyTheGame

Prototype **pré-alpha web** de SnikyTheGame orienté **runner**.

## Analyse des versions existantes du dépôt

Historique disponible actuellement:

- `faee0c1` : commit initial avec README minimal.
- `2237b57` : première web pré-alpha livrée en gameplay Snake.

Cette itération corrige la direction produit: **SnikyTheGame est un runner**, donc le gameplay web est aligné sur un endless runner.

## Lancer le projet

```bash
python3 -m http.server 4173
```

Puis ouvrir: `http://localhost:4173`

## Fonctionnalités actuelles (pré-alpha runner)

- Runner 2D jouable au clavier (saut, pause, reset).
- Défilement, obstacles aléatoires, collisions et game over.
- Score + distance + vitesse dynamique.
- Sauvegarde locale du meilleur score via `localStorage`.

## Contrôles

- `Espace` / `Flèche haut` / `Z` : sauter.
- `P` : pause.
- Boutons UI: démarrer / pause / recommencer.

## Prochaines étapes suggérées

- Ajouter animation sprite du personnage.
- Ajouter plusieurs types d’obstacles.
- Intégrer sons et feedback hit/jump.
- Ajouter écran titre + sélection difficulté.
