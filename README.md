# SnikyTheGame

Prototype **pré-alpha web** de SnikyTheGame orienté **runner**.

## Analyse du repository actuel

Historique Git disponible dans ce repo local:

- `faee0c1` : commit initial du projet.
- `85bd688` : première pré-alpha web runner (UI + logique de base).

Cette version améliore la pré-alpha en intégrant un rendu **sprite-like**,
plusieurs obstacles, et une boucle de jeu plus lisible pour les tests gameplay.

## Lancer le projet

```bash
python3 -m http.server 4173
```

Puis ouvrir: `http://localhost:4173`

## Fonctionnalités de la pré-alpha

- Runner 2D jouable au clavier (saut, pause, reset).
- Sprites du joueur (run frame A/B + jump) et obstacles (rocher, pics, drone).
- Obstacles variés (sol + aérien), collisions, game over.
- Défilement avec parallax simple pour perception de vitesse.
- Score + distance + vitesse + combo d’esquive.
- Sauvegarde locale du meilleur score via `localStorage`.

## Contrôles

- `Espace` / `Flèche haut` / `Z` / `W` : sauter.
- `P` : pause.
- Boutons UI: démarrer / pause / recommencer.

## Prochaines étapes suggérées

- Ajouter des animations plus fluides (sprite-sheet / interpolation).
- Ajouter des bonus temporaires (shield, dash) et patterns d’obstacles.
- Intégrer son/SFX (jump, hit, dodge combo).
- Ajouter écran titre + menu difficulté + best times.
