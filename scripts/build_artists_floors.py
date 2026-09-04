#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Régénère toute la section "Nos artistes" de index.html à partir de
data/artists_grid.json, en reproduisant exactement la logique du site
d'origine :

- Les artistes sont groupés par "étage" de 4 maximum.
- Chaque étage alterne fond blanc/liseré noir puis fond noir/liseré rose,
  puis blanc à nouveau, etc. (comme sur le site d'origine : le 1er étage,
  Jackie/ALMAGABRIEL/Herson/Mandarina, est blanc à liseré noir ; le 2e,
  Santoré/Pete Byrd/Verlatour, est noir à liseré rose).
- Dans un étage, les colonnes se partagent la largeur également selon le
  nombre d'artistes qu'il contient (1 → pleine largeur, 2 → 50/50,
  3 → 33/33/33, 4 → 25/25/25/25) et restent centrées.
- La disposition alterne en continu sur TOUS les artistes (pas juste au
  sein d'un étage) : photo en haut/texte en bas, puis texte en haut/photo
  en bas, etc. (Jackie=photo, ALMAGABRIEL=texte, Herson=photo, ...).

Usage :
    python scripts/build_artists_floors.py

Modifie uniquement ce qui se trouve entre les marqueurs
<!-- ARTISTS:START --> et <!-- ARTISTS:END --> de index.html. Pour ajouter
un artiste, ajoutez simplement une entrée à la fin de
data/artists_grid.json puis relancez ce script.
"""
import html
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "artists_grid.json")
INDEX_FILE = os.path.join(ROOT, "index.html")

START_MARKER = "<!-- ARTISTS:START -->"
END_MARKER = "<!-- ARTISTS:END -->"

ICON_CLASSES = {
    "spotify": "fa fa-spotify",
    "instagram": "fa fa-instagram",
    "facebook": "fa fa-facebook",
    "youtube": "fa fa-youtube",
    "tiktok": "fa fa-tiktok",
    "soundcloud": "fa fa-soundcloud",
    "web": "fa fa-globe",
}

COL_WIDTH_CLASS = {1: "elementor-col-100", 2: "elementor-col-50", 3: "elementor-col-33", 4: "elementor-col-25"}

# Les deux jeux de couleurs déjà utilisés sur le site d'origine.
FLOOR_STYLES = [
    {"bg": "#FFFFFF", "zigzag": "#030303", "text_white": False},  # étage blanc, liseré noir
    {"bg": "#0a0a0a", "zigzag": "#E91E63", "text_white": True},   # étage noir, liseré rose
]


def esc(s):
    return html.escape(s or "", quote=False)


def rand_id():
    return "".join(random.choice("0123456789abcdef") for _ in range(7))


def divider_svg_style(color):
    return (
        "--divider-border-style:zigzag_tribal;--divider-color:" + color + ";"
        "--divider-pattern-height:20px;"
        "--divider-pattern-url: url(&quot;data:image/svg+xml,%3Csvg xmlns=&#039;http://www.w3.org/2000/svg&#039; "
        "preserveAspectRatio=&#039;xMidYMid meet&#039; overflow=&#039;visible&#039; height=&#039;100%&#039; "
        "viewBox=&#039;0 0 120 26&#039; fill=&#039;black&#039; stroke=&#039;none&#039;%3E%3Cpolygon points=&#039;0,14.4 0,21 "
        "11.5,12.4 21.3,20 30.4,11.1 40.3,20 51,12.4 60.6,20 69.6,11.1 79.3,20 90.1,12.4 99.6,20 109.7,11.1 120,21 "
        "120,14.4 109.7,5 99.6,13 90.1,5 79.3,14.5 71,5.7 60.6,12.4 51,5 40.3,14.5 31.1,5 21.3,13 11.5,5 "
        "\t&#039;/%3E%3C/svg%3E&quot;);"
    )


def build_card(a):
    icons = "".join(
        f'''
															<li>
																<a href="{esc(s["url"])}" target="_blank">									<i class="{ICON_CLASSES.get(s["icon"], "fa fa-globe")}"></i>
																</a>
															</li>
'''
        for s in a.get("socials", [])
    )
    card_id = rand_id()
    return f'''<div class="elementor-element elementor-element-{card_id} elementor-widget elementor-widget-anggita-team" data-id="{card_id}" data-element_type="widget" data-widget_type="anggita-team.default">
				<div class="elementor-widget-container">
							<div class="clearfix">
			<div class="port-inner team-innerbox">
				<div class="port-box"></div>
				<div class="port-img width-img img-bg" style="background-image:url('{esc(a["card_image"])}');"></div>
				<div class="img-mask"></div>
				<div class="port-dbox">
					<div class="dbox-relative">
						<h3 >{esc(a["name"])}</h3>
						<p >{esc(a["genre"])}</p>
						<ul class="team-sicon">
{icons}
						</ul>
					</div>
				</div>
			</div>
		</div>
				</div>
				</div>'''


def build_bio(a, zigzag_color, text_white):
    con_id, div_id, txt_id = (rand_id() for _ in range(3))
    bio_text = esc(a["bio"])
    p_open = '<p><span style="color: #ffffff;">' if text_white else "<p>"
    p_close = "</span></p>" if text_white else "</p>"
    return f'''<div class="elementor-element elementor-element-{con_id} e-transform e-flex e-con-boxed e-con e-parent" data-id="{con_id}" data-element_type="container" data-settings="{{&quot;_transform_translateX_effect&quot;:{{&quot;unit&quot;:&quot;px&quot;,&quot;size&quot;:&quot;&quot;,&quot;sizes&quot;:[]}},&quot;_transform_translateX_effect_tablet&quot;:{{&quot;unit&quot;:&quot;px&quot;,&quot;size&quot;:&quot;&quot;,&quot;sizes&quot;:[]}},&quot;_transform_translateX_effect_mobile&quot;:{{&quot;unit&quot;:&quot;px&quot;,&quot;size&quot;:&quot;&quot;,&quot;sizes&quot;:[]}},&quot;_transform_translateY_effect&quot;:{{&quot;unit&quot;:&quot;px&quot;,&quot;size&quot;:&quot;&quot;,&quot;sizes&quot;:[]}},&quot;_transform_translateY_effect_tablet&quot;:{{&quot;unit&quot;:&quot;px&quot;,&quot;size&quot;:&quot;&quot;,&quot;sizes&quot;:[]}},&quot;_transform_translateY_effect_mobile&quot;:{{&quot;unit&quot;:&quot;px&quot;,&quot;size&quot;:&quot;&quot;,&quot;sizes&quot;:[]}}}}">
						<div class="e-con-inner">
					<div class="elementor-element elementor-element-{div_id} elementor-widget-divider--separator-type-pattern elementor-widget-divider--no-spacing elementor-widget-divider--view-line elementor-widget elementor-widget-divider" data-id="{div_id}" data-element_type="widget" data-widget_type="divider.default">
							<div class="elementor-divider" style="{divider_svg_style(zigzag_color)}">
			<span class="elementor-divider-separator">
						</span>
		</div>
							</div>
				<div class="elementor-element elementor-element-{txt_id} elementor-widget elementor-widget-text-editor" data-id="{txt_id}" data-element_type="widget" data-settings="{{&quot;_animation&quot;:&quot;none&quot;}}" data-widget_type="text-editor.default">
									{p_open}{bio_text}{p_close}								</div>
					</div>
				</div>'''


def build_column(a, bio_first, col_width_class, zigzag_color, text_white):
    col_id = rand_id()
    card = build_card(a)
    bio = build_bio(a, zigzag_color, text_white)
    inner = f"{bio}\n\t\t{card}" if bio_first else f"{card}\n\t\t{bio}"
    return f'''
				<div class="elementor-column {col_width_class} elementor-top-column elementor-element elementor-element-{col_id}" data-id="{col_id}" data-element_type="column" data-settings="{{&quot;background_background&quot;:&quot;classic&quot;}}">
			<div class="elementor-widget-wrap elementor-element-populated">
						{inner}
					</div>
		</div>'''


def build_floor(artists_in_floor, floor_index, start_position):
    style = FLOOR_STYLES[floor_index % len(FLOOR_STYLES)]
    col_class = COL_WIDTH_CLASS[len(artists_in_floor)]
    section_id = rand_id()
    columns = []
    for i, a in enumerate(artists_in_floor):
        bio_first = (start_position + i) % 2 == 1
        columns.append(build_column(a, bio_first, col_class, style["zigzag"], style["text_white"]))
    id_attr = ' id="artistes"' if floor_index == 0 else ""
    return f'''
				<section class="elementor-section elementor-top-section elementor-element elementor-element-{section_id} elementor-section-content-middle elementor-section-height-min-height elementor-section-boxed elementor-section-height-default elementor-section-items-middle" data-id="{section_id}" data-element_type="section"{id_attr} data-settings="{{&quot;background_background&quot;:&quot;classic&quot;}}" style="background-color:{style["bg"]};">
						<div class="elementor-container elementor-column-gap-extended" style="min-height:400px;">{"".join(columns)}
					</div>
		</section>'''


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        artists = json.load(f)

    if not artists:
        sys.exit("data/artists_grid.json est vide.")

    floors_html = []
    for floor_index in range(0, len(artists), 4):
        chunk = artists[floor_index:floor_index + 4]
        floors_html.append(build_floor(chunk, floor_index // 4, floor_index))

    grid_html = "".join(floors_html) + "\n"

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        page = f.read()

    if START_MARKER not in page or END_MARKER not in page:
        sys.exit("Marqueurs ARTISTS:START / ARTISTS:END introuvables dans index.html.")

    start = page.index(START_MARKER) + len(START_MARKER)
    end = page.index(END_MARKER)
    page = page[:start] + grid_html + page[end:]

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(page)

    n_floors = (len(artists) + 3) // 4
    print(f"OK : {len(artists)} artiste(s) répartis sur {n_floors} étage(s).")


if __name__ == "__main__":
    main()
