# Baguette Publishing — guide pour Claude

Ce fichier est lu automatiquement par Claude (Claude Code, ou une session
claude.ai connectée à ce dépôt via un connecteur GitHub) avant d'agir sur
ce projet. Il s'adresse à Claude, pas à un lecteur humain — mais toute
personne qui l'ouvre y trouvera les mêmes règles.

## Ce que c'est

Copie statique (HTML/CSS/JS/images) du site WordPress
baguettepublishing.com, hébergée sur GitHub Pages, pendant la phase de
transition avant un hébergement définitif sur l'OVH du client. Le design
reproduit fidèlement l'original — toute modification doit préserver ce
rendu.

**Décision actée avec le client (à ne pas remettre en cause sans lui
reposer la question) : sortir complètement de WordPress.** Le site
définitif sur OVH sera un site statique/sur-mesure "from scratch", pas
un retour à WordPress. Ne pas proposer de réinstaller WordPress sur OVH.

## ⚠️ GitHub est temporaire — ne pas construire dessus comme si c'était définitif

**Ce dépôt GitHub ne sera plus l'hébergement du site au moment de la
remise au client.** Le site final vivra sur l'**OVH du client**. Ça a des
conséquences concrètes à garder en tête :

- Le mécanisme de publication actuel de l'outil admin (`admin/index.html`)
  repose entièrement sur l'**API GitHub Contents** (lecture/écriture de
  fichiers via un jeton, déclenchement de la GitHub Action). **Rien de
  ça ne fonctionnera sur OVH tel quel** — OVH n'a pas d'API GitHub. Ce
  mécanisme devra être reconstruit pour l'hébergement cible, en fonction
  de ce qu'OVH permet concrètement (accès FTP/SFTP seul ? exécution de
  PHP possible pour un petit backend ? — à vérifier avant de choisir
  l'architecture).
- Un "connecteur GitHub" côté claude.ai (pour que le client pilote Claude
  en autonomie) ne sera **plus le bon connecteur** une fois le site sur
  OVH — il faudra un accès équivalent adapté à cet hébergement (FTP/SFTP,
  ou une API si un backend PHP est construit).
- Ne pas coder en dur d'URL GitHub Pages (`romainpitot.github.io/...`)
  comme si elle allait perdurer — c'est une URL de travail, pas celle du
  site final.

**En résumé : tout ce qui est construit ici doit être vu comme un
prototype fonctionnel de la logique (contenu modulaire, historique,
confirmation avant publication) — la logique se transporte, le
mécanisme technique de publication devra être refait pour OVH.**

**Site en ligne :** https://romainpitot.github.io/baguettepublishing-wp-clone/
**Outil d'administration simple (formulaire) :** .../admin/

## Règle n°1 — ne jamais éditer `index.html` à la main

Ce fichier est **entièrement régénéré** à partir des données ci-dessous.
Toute modification faite directement dedans sera écrasée au prochain
push sur `data/*.json`. Éditer uniquement :

- **`data/artists_grid.json`** — liste des artistes (nom, genre, bio, photo,
  réseaux). Régénéré par `scripts/build_artists_floors.py`. Reproduit la
  logique originale par "étages" de 4 artistes max, fond blanc/noir en
  alternance, cartes toujours à taille normale (jamais étirées même si un
  étage est incomplet), alternance photo-en-haut/texte-en-haut en continu
  sur tous les artistes.
- **`data/site_content.json`** — diapositives du hero, section "Qui
  sommes-nous", section Contact. Régénéré par
  `scripts/build_site_content.py`.

Après modification d'un de ces fichiers, lancer le script correspondant
(ou les deux) puis commit + push : `.github/workflows/build-artists.yml`
le refait aussi automatiquement à chaque push sur l'un de ces fichiers.

## Règle n°2 — toujours passer par les scripts, jamais de HTML à la main

Si une nouvelle section doit devenir modulaire, suivre le même principe
que l'existant : un bloc de données JSON + un script Python qui régénère
le HTML entre des marqueurs (`<!-- ARTISTS:START -->`, `<!-- HERO:START -->`,
etc.) — jamais de section ajoutée en dur dans `index.html`.

## Règle n°3 — sécurité et confirmation

- Toute image remplacée doit voir son ancienne version supprimée
  (éviter les fichiers orphelins).
- Avant de publier un changement dont la formulation du client est
  ambiguë ou dont l'impact visuel n'est pas évident, **demander une
  confirmation explicite** plutôt que de pousser directement.
- Chaque changement doit être un commit **descriptif** (quoi, pourquoi).
  L'historique git est le filet de sécurité du projet — rien ne doit
  jamais être fait en force-push ou en réécrivant l'historique. Pour
  annuler un changement, ajouter un nouveau commit qui restaure l'état
  précédent (voir l'onglet "Historique" de l'outil admin, qui fait
  exactement ça).
- Le tag `avant-modularite` marque un état stable connu si besoin de
  comparer ou revenir loin en arrière.

## Règle n°4 — le formulaire de contact ne fonctionne pas

Contact Form 7 dépendait du backend PHP/WordPress, absent ici. Ne pas
essayer de le faire fonctionner sans en discuter avec le client d'abord
(nécessite un service tiers type Formspree).

## Avant de conclure une tâche

Toujours vérifier visuellement (capture d'écran ou lecture du DOM) que
la page rendue correspond à ce qui était demandé, avant de pousser sur
`master` — le site est public et se met à jour en ~1 minute.
