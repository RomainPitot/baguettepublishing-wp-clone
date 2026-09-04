# Baguette Publishing — Clone statique (temporaire)

Copie statique HTML/CSS/JS/images de https://www.baguettepublishing.com/, aspirée depuis le site WordPress en ligne pour servir de base de travail hors WordPress.

**Aperçu en ligne :** https://romainpitot.github.io/baguettepublishing-wp-clone/ (mis à jour automatiquement à chaque `push`)

## Structure

- `index.html` : page d'accueil (page unique avec ancres : Qui sommes-nous, Nos artistes, Notre catalogue, Contact)
- `wp-content/`, `wp-includes/` : assets d'origine (CSS, JS, polices, images), chemins réécrits en relatif
- `data/artists_grid.json` : **la liste des artistes** de la section "Nos artistes" — c'est le seul fichier à modifier pour ajouter/modifier un artiste
- `scripts/build_artists_floors.py` : régénère toute la section "Nos artistes" à partir de `data/artists_grid.json`

⚠️ Le formulaire de contact (Contact Form 7) ne fonctionne pas ici : il dépendait du backend PHP/WordPress, absent de cette copie statique.

## Logique de la section "Nos artistes"

Le site d'origine organise les artistes par **étages de 4 maximum**, avec un fond qui alterne :
- Étage 1 (positions 1-4) : fond **blanc**, liseré **noir**
- Étage 2 (positions 5-8) : fond **noir**, liseré **rose**
- Étage 3 (positions 9-12) : fond blanc à nouveau, etc.

Dans chaque étage, les colonnes se partagent la largeur également selon le nombre d'artistes qu'il contient (1 → pleine largeur, 2 → 50/50, 3 → 33/33/33, 4 → 25/25/25/25), toujours centrées. La disposition de chaque carte (photo en haut/texte en bas, ou l'inverse) alterne en continu sur l'ensemble des artistes, pas seulement au sein d'un étage.

`scripts/build_artists_floors.py` reproduit exactement cette logique : il régénère l'intégralité de la section entre les marqueurs `<!-- ARTISTS:START -->` / `<!-- ARTISTS:END -->` de `index.html` à partir de la liste ordonnée dans `data/artists_grid.json`. Rien d'autre sur la page n'est modifié.

## Ajouter un artiste

1. Ajouter une entrée à la fin de `data/artists_grid.json` (copier un bloc existant comme modèle) avec :
   - `name` : nom de l'artiste
   - `genre` : tag court (ex. "Pop Solaire")
   - `bio` : paragraphe de présentation
   - `card_image` : chemin vers la photo (carrée/portrait de préférence)
   - `socials` : liste `{"icon": "spotify"|"instagram"|"facebook"|"youtube"|"tiktok"|"soundcloud", "url": "..."}`
2. Déposer la photo dans `wp-content/uploads/2025/09/` (ou un dossier de son choix) et faire correspondre le chemin dans le JSON.
3. Lancer :
   ```
   python scripts/build_artists_floors.py
   ```
4. Vérifier le rendu, puis commit + push (mise à jour automatique de la page GitHub Pages).

En pratique : donnez simplement le texte, les liens et l'image à Claude, qui s'occupe de l'étape JSON + script + commit/push.

Dépôt temporaire de travail — usage interne, avant transfert vers la plateforme cible.
