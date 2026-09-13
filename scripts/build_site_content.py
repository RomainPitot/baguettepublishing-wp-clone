#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Régénère les sections "Hero", "Qui sommes-nous" et "Contact" de index.html
à partir de data/site_content.json — même principe que
scripts/build_artists_floors.py pour la grille d'artistes.

Modifie uniquement ce qui se trouve entre les marqueurs :
  <!-- HERO:START --> ... <!-- HERO:END -->
  <!-- ABOUT:START --> ... <!-- ABOUT:END -->
  <!-- CONTACT:START --> ... <!-- CONTACT:END -->
Le reste de la page n'est jamais touché.

Usage :
    python scripts/build_site_content.py
"""
import html
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "site_content.json")
INDEX_FILE = os.path.join(ROOT, "index.html")

SOCIAL_ICON_CLASS = {
    "linkedin": "fa fa-linkedin",
    "instagram": "fa fa-instagram",
    "facebook": "fa fa-facebook",
    "youtube": "fa fa-youtube",
    "spotify": "fa fa-spotify",
    "tiktok": "fa fa-tiktok",
}


def esc(s):
    return html.escape(s or "", quote=False)


def rand_id():
    return "".join(random.choice("0123456789abcdef") for _ in range(7))


def build_hero(slides):
    parts = []
    for s in slides:
        parts.append(f'''
			<div class="item slide clearfix">
				<div class="slider-img-bg" data-animation="puffIn" data-delay="0.2s" data-animation-duration="0.7s"
					style="background-image:url('{esc(s["image"])}');"></div>
				<div class="slider-mask" data-animation="slideUpReturn" data-delay="0.1s"></div>
				<div class="caption-box clearfix">
					<div class="slider-box container-fluid">
						<div class="slider-content">
							<p class="slider-subtitle" data-animation="fadeIn" data-delay="1.5s">
								{esc(s["name"])}							</p>
							<div class="clearfix"></div>
							<div class="slider-hidden">
								<h3 class="slider-title" data-animation="fadeInUp" data-delay="0.8s">
									{esc(s["word"])}</h3>
							</div>
							<!--/.slider-hidden-->
							<div class="slider-line" data-animation="swashIn" data-delay="0.5s"></div>
							<p class="slider-text" data-animation="fadeInDown" data-delay="1s">
								{esc(s["text"])}							</p>
							<div class="btn-relative" data-animation="swashIn" data-delay="1.8s" data-animation-duration="1s">
								<a class="slider-btn" href="#artistes">
								More View								</a>
							</div>
							<!--/.btn-relative-->
						</div>
						<!--/.slider-content-->
					</div>
					<!--/.slider-box-->
				</div>
				<!--/.caption-box-->
			</div>
			<!--/.slide-->
''')
    return f'''
		<div class="slider home-slider  ani-slider  clearfix"
			data-slick='{{"autoplaySpeed": 5000}}'>
{"".join(parts)}
					</div>
'''


def build_about(about):
    paras = "".join(f"<p>{p}</p>" for p in about["paragraphs"])
    eyebrow_id, body_id, img_id, title_id = (rand_id() for _ in range(4))
    return f'''
				<section class="elementor-section elementor-top-section elementor-element elementor-element-{rand_id()} elementor-section-boxed elementor-section-height-default elementor-section-height-default" data-element_type="section" id="about" data-settings="{{&quot;background_background&quot;:&quot;classic&quot;}}">
							<div class="elementor-background-overlay"></div>
							<div class="elementor-container elementor-column-gap-extended">
					<div class="elementor-column elementor-col-50 elementor-top-column elementor-element elementor-element-{rand_id()}" data-element_type="column">
			<div class="elementor-widget-wrap elementor-element-populated">
						<div class="elementor-element elementor-element-{title_id} elementor-widget elementor-widget-anggita-title" data-element_type="widget" data-widget_type="anggita-title.default">
				<div class="elementor-widget-container">
					<h2 class="content-title">{esc(about["title"])}</h2>				</div>
				</div>
				<div class="elementor-element elementor-element-{eyebrow_id} animated-fast elementor-invisible elementor-widget elementor-widget-text-editor" data-element_type="widget" data-settings="{{&quot;_animation&quot;:&quot;fadeInUp&quot;,&quot;_animation_delay&quot;:100}}" data-widget_type="text-editor.default">
									<p>{esc(about["eyebrow"])}</p>								</div>
				<div class="elementor-element elementor-element-{body_id} elementor-widget elementor-widget-text-editor" data-element_type="widget" data-widget_type="text-editor.default">
									{paras}								</div>
					</div>
		</div>
				<div class="elementor-column elementor-col-50 elementor-top-column elementor-element elementor-element-{rand_id()}" data-element_type="column">
			<div class="elementor-widget-wrap elementor-element-populated">
						<div class="elementor-element elementor-element-{img_id} elementor-widget elementor-widget-image" data-element_type="widget" data-widget_type="image.default">
															<img fetchpriority="high" decoding="async" src="{esc(about["image"])}" class="attachment-full size-full" alt="" />															</div>
					</div>
		</div>
					</div>
		</section>
'''


def build_contact(contact):
    socials_html = "".join(
        f'''
					<span class="elementor-grid-item">
						<a class="elementor-icon elementor-social-icon elementor-social-icon-{s["icon"]} elementor-animation-shrink" href="{esc(s["url"])}" target="_blank">
							<span class="elementor-screen-only">{s["icon"].capitalize()}</span>
							<i class="{SOCIAL_ICON_CLASS.get(s["icon"], "fa fa-globe")}"></i>
						</a>
					</span>'''
        for s in contact.get("socials", [])
    )
    return f'''
				<div class="elementor-column elementor-col-33 elementor-top-column elementor-element elementor-element-{rand_id()}" data-element_type="column" id="contact">
			<div class="elementor-widget-wrap elementor-element-populated">
						<div class="elementor-element elementor-element-{rand_id()} elementor-widget elementor-widget-heading" data-element_type="widget" data-widget_type="heading.default">
					<h2 class="elementor-heading-title elementor-size-default">Contact</h2>				</div>
				<div class="elementor-element elementor-element-{rand_id()} elementor-tablet-align-center elementor-align-right elementor-icon-list--layout-traditional elementor-list-item-link-full_width elementor-widget elementor-widget-icon-list" data-element_type="widget" data-widget_type="icon-list.default">
							<ul class="elementor-icon-list-items">
							<li class="elementor-icon-list-item">
											<span class="elementor-icon-list-icon"><i class="fa fa-building"></i></span>
										<span class="elementor-icon-list-text">{esc(contact["city"])}</span>
									</li>
								<li class="elementor-icon-list-item">
											<a href="mailto:{esc(contact["email"])}">
												<span class="elementor-icon-list-icon"><i class="fa fa-envelope"></i></span>
										<span class="elementor-icon-list-text">{esc(contact["email"])}</span>
											</a>
									</li>
						</ul>
						</div>
					</div>
		</div>
				<div class="elementor-column elementor-col-33 elementor-top-column elementor-element elementor-element-{rand_id()}" data-element_type="column" data-settings="{{&quot;background_background&quot;:&quot;classic&quot;}}">
			<div class="elementor-widget-wrap elementor-element-populated">
						<div class="elementor-element elementor-element-{rand_id()} elementor-widget elementor-widget-image" data-element_type="widget" data-widget_type="image.default">
															<img decoding="async" src="{esc(contact["logo"])}" class="attachment-thumbnail size-thumbnail" alt="" />															</div>
					</div>
		</div>
				<div class="elementor-column elementor-col-33 elementor-top-column elementor-element elementor-element-{rand_id()}" data-element_type="column">
			<div class="elementor-widget-wrap elementor-element-populated">
						<div class="elementor-element elementor-element-{rand_id()} elementor-widget elementor-widget-text-editor" data-element_type="widget" data-widget_type="text-editor.default">
									<p><em>{esc(contact["quote"])}</em></p>								</div>
				<div class="elementor-element elementor-element-{rand_id()} e-grid-align-left e-grid-align-tablet-center e-grid-align-mobile-center elementor-shape-rounded elementor-grid-0 elementor-widget elementor-widget-social-icons" data-element_type="widget" data-widget_type="social-icons.default">
							<div class="elementor-social-icons-wrapper elementor-grid">{socials_html}
							</div>
						</div>
					</div>
		</div>
'''


def replace_between(page, start_marker, end_marker, content):
    if start_marker not in page or end_marker not in page:
        sys.exit(f"Marqueurs introuvables : {start_marker} / {end_marker}")
    start = page.index(start_marker) + len(start_marker)
    end = page.index(end_marker)
    return page[:start] + content + page[end:]


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        page = f.read()

    page = replace_between(page, "<!-- HERO:START -->", "<!-- HERO:END -->", build_hero(data["hero_slides"]))
    page = replace_between(page, "<!-- ABOUT:START -->", "<!-- ABOUT:END -->", build_about(data["about"]))
    page = replace_between(page, "<!-- CONTACT:START -->", "<!-- CONTACT:END -->", build_contact(data["contact"]))

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"OK : {len(data['hero_slides'])} slide(s) hero, à propos et contact régénérés.")


if __name__ == "__main__":
    main()
