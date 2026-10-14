#!/usr/bin/env python3
"""Genera las plantillas JSON de Elementor para Julia Wisteria.

Uso:  python3 generate_templates.py
Produce los archivos en ./templates/ listos para importar desde
Elementor > Plantillas > Plantillas guardadas > Importar plantillas.

Todos los elementos usan widgets nativos de Elementor / Elementor Pro
(heading, text-editor, button, icon-box, icon-list, testimonial, counter,
star-rating, form, price-table, woocommerce-products, wc-categories,
nav-menu, search-form, woocommerce-menu-cart, social-icons).
"""
import itertools
import json
import os

_counter = itertools.count(1)


def nid():
    return "jw{:05x}".format(next(_counter))


# ── Sistema de diseño ──────────────────────────────────────────────
C = {
    "cream": "#F9F2EB", "creamd": "#F0E6D9", "brown": "#5A4642",
    "brownl": "#7A6460", "rose": "#B88889", "rosel": "#D4B4B5",
    "sage": "#C1C099", "muted": "#8B7B78", "white": "#FFFFFF",
}
SERIF = "Cormorant Garamond"
SCRIPT = "Sacramento"
SANS = "Jost"


def px(size):
    return {"unit": "px", "size": size, "sizes": []}


def typo(prefix, family=None, size=None, weight=None, transform=None,
         spacing=None, height=None, style=None, size_t=None, size_m=None):
    s = {prefix + "_typography": "custom"}
    if family:
        s[prefix + "_font_family"] = family
    if size:
        s[prefix + "_font_size"] = px(size)
        # Escalado responsive automático para textos grandes
        if size_t is None and size >= 18:
            size_t = round(size * (0.82 if size >= 40 else 0.9))
        if size_m is None and size >= 16:
            size_m = round(size * (0.58 if size >= 40 else 0.75))
        if size_t:
            s[prefix + "_font_size_tablet"] = px(size_t)
        if size_m:
            s[prefix + "_font_size_mobile"] = px(size_m)
    if weight:
        s[prefix + "_font_weight"] = str(weight)
    if transform:
        s[prefix + "_text_transform"] = transform
    if spacing is not None:
        s[prefix + "_letter_spacing"] = px(spacing)
    if height:
        s[prefix + "_line_height"] = {"unit": "em", "size": height, "sizes": []}
    if style:
        s[prefix + "_font_style"] = style
    return s


def el(el_type, settings, elements=None, widget=None, inner=False):
    d = {"id": nid(), "elType": el_type, "settings": settings,
         "elements": elements or [], "isInner": inner}
    if widget:
        d["widgetType"] = widget
    return d


def container(settings, children, inner=False):
    s = {"content_width": "boxed", "flex_direction": "column"}
    s.update(settings)
    return el("container", s, children, inner=inner)


def row(children, settings=None, inner=True, stack="column"):
    """stack: 'column' apila en móvil · 'wrap' envuelve en tablet/móvil ·
    None no cambia nada."""
    s = {"content_width": "full", "flex_direction": "row",
         "flex_gap": {"unit": "px", "size": 28, "column": "28", "row": "28"}}
    if stack == "column":
        s["flex_direction_mobile"] = "column"
    elif stack == "wrap":
        s["flex_wrap_tablet"] = "wrap"
        s["flex_wrap_mobile"] = "wrap"
    s.update(settings or {})
    return container(s, children, inner=inner)


def col(children, width=50, settings=None, tablet=None, mobile=100):
    s = {"content_width": "full", "flex_direction": "column",
         "width": {"unit": "%", "size": width, "sizes": []}}
    if tablet:
        s["width_tablet"] = {"unit": "%", "size": tablet, "sizes": []}
    if mobile:
        s["width_mobile"] = {"unit": "%", "size": mobile, "sizes": []}
    s.update(settings or {})
    return container(s, children, inner=True)


def pad(top, right, bottom, left):
    d = {"padding": {"unit": "px", "top": str(top), "right": str(right),
                     "bottom": str(bottom), "left": str(left),
                     "isLinked": False}}
    if max(top, right, bottom, left) > 24:
        d["padding_tablet"] = {
            "unit": "px", "top": str(round(top * 0.75)),
            "right": str(min(right, 36)), "bottom": str(round(bottom * 0.75)),
            "left": str(min(left, 36)), "isLinked": False}
        d["padding_mobile"] = {
            "unit": "px", "top": str(round(top * 0.6)),
            "right": str(min(right, 20)), "bottom": str(round(bottom * 0.6)),
            "left": str(min(left, 20)), "isLinked": False}
    return d


# ── Widgets ────────────────────────────────────────────────────────
def heading(text, tag="h2", color=C["brown"], align="left", **t):
    s = {"title": text, "header_size": tag, "title_color": color,
         "align": align}
    s.update(typo("typography", **t))
    return el("widget", s, widget="heading")


def eyebrow(text, color=C["rose"], align="left", size=28):
    return heading(text, tag="div", color=color, align=align,
                   family=SCRIPT, size=size, weight=400)


def label(text, color=C["muted"], align="left", size=11, spacing=2):
    """Texto pequeño en mayúsculas con tracking (subtítulos de sección)."""
    return heading(text, tag="div", color=color, align=align, family=SANS,
                   size=size, weight=400, transform="uppercase",
                   spacing=spacing, height=2)


def texted(html, color=C["muted"], align="left", **t):
    s = {"editor": "<p>{}</p>".format(html), "text_color": color,
         "align": align}
    s.update(typo("typography", **t))
    return el("widget", s, widget="text-editor")


def para(html, color=C["muted"], align="left", size=13.5):
    return texted(html, color=color, align=align, family=SANS, size=size,
                  weight=300, height=1.95)


def button(text, url="#", bg=C["brown"], color=C["cream"], border=None,
           align="left", hover_bg=C["rose"]):
    s = {"text": text,
         "link": {"url": url, "is_external": "", "nofollow": ""},
         "button_text_color": color, "align": align,
         "border_radius": {"unit": "px", "top": "0", "right": "0",
                           "bottom": "0", "left": "0", "isLinked": True},
         "text_padding": {"unit": "px", "top": "15", "right": "40",
                          "bottom": "15", "left": "40", "isLinked": False},
         "hover_color": "#FFFFFF",
         "button_background_hover_color": hover_bg}
    if bg:
        s["background_color"] = bg
    if border:
        s.update({"border_border": "solid",
                  "border_width": {"unit": "px", "top": "1", "right": "1",
                                   "bottom": "1", "left": "1",
                                   "isLinked": True},
                  "border_color": border,
                  "background_color": "rgba(0,0,0,0)"})
    s.update(typo("typography", family=SANS, size=10, weight=500,
                  transform="uppercase", spacing=3))
    return el("widget", s, widget="button")


def spacer(size=24):
    return el("widget", {"space": px(size)}, widget="spacer")


def icon_box(icon, title, desc, link="#"):
    s = {"selected_icon": {"value": icon, "library": "fa-solid"},
         "title_text": title, "description_text": desc,
         "link": {"url": link, "is_external": "", "nofollow": ""},
         "position": "top", "text_align": "left",
         "primary_color": C["rose"], "title_color": C["brown"],
         "description_color": C["muted"], "icon_size": px(38),
         "icon_space": px(16)}
    s.update(typo("title_typography", family=SERIF, size=24, weight=400))
    s.update(typo("description_typography", family=SANS, size=13,
                  weight=300, height=1.9))
    return el("widget", s, widget="icon-box")


def icon_list(items, icon="fas fa-circle", icon_size=5):
    s = {"icon_list": [
            {"_id": nid(), "text": t,
             "selected_icon": {"value": icon, "library": "fa-solid"}}
            for t in items],
         "icon_color": C["rose"], "text_color": C["muted"],
         "icon_size": px(icon_size),
         "space_between": px(8)}
    s.update(typo("icon_typography", family=SANS, size=12.5, weight=300))
    return el("widget", s, widget="icon-list")


def link_list(items):
    """Lista de enlaces de footer (icon-list sin icono)."""
    s = {"icon_list": [
            {"_id": nid(), "text": t,
             "link": {"url": u, "is_external": "", "nofollow": ""},
             "selected_icon": {"value": "", "library": ""}}
            for t, u in items],
         "text_color": C["muted"], "space_between": px(10)}
    s.update(typo("icon_typography", family=SANS, size=12.5, weight=300))
    return el("widget", s, widget="icon-list")


def stars():
    return el("widget", {"rating": 5, "star_style": "star_fontawesome",
                         "stars_color": C["sage"], "stars_size": px(14),
                         "align": "left"}, widget="star-rating")


def testimonial(quote, name, job):
    s = {"testimonial_content": quote, "testimonial_name": name,
         "testimonial_job": job, "testimonial_image": {"url": "", "id": ""},
         "testimonial_alignment": "left",
         "content_content_color": C["brown"],
         "name_text_color": C["brown"], "job_text_color": C["muted"]}
    s.update(typo("content_typography", family=SERIF, size=17, weight=300,
                  style="italic", height=1.8))
    s.update(typo("job_typography", family=SANS, size=10, weight=400,
                  transform="uppercase", spacing=2))
    return el("widget", s, widget="testimonial")


def counter(number, suffix, title):
    s = {"starting_number": 0, "ending_number": number, "suffix": suffix,
         "title": title, "number_color": C["brown"],
         "title_color": C["muted"]}
    s.update(typo("typography_number", family=SERIF, size=38, weight=300))
    s.update(typo("typography_title", family=SANS, size=9.5, weight=400,
                  transform="uppercase", spacing=2))
    return el("widget", s, widget="counter")


def section_header(script_text, title, sub, dark=False):
    """Encabezado de sección centrado: script + H2 + subtítulo."""
    c1 = C["sage"] if dark else C["rose"]
    c2 = C["cream"] if dark else C["brown"]
    c3 = "rgba(249,242,235,0.62)" if dark else C["muted"]
    return [
        eyebrow(script_text, color=c1, align="center"),
        heading(title, tag="h2", color=c2, align="center", family=SERIF,
                size=44, weight=300),
        label(sub, color=c3, align="center"),
    ]


# ════════════════════════════════════════════════════════════════════
# HEADER (Theme Builder)
# ════════════════════════════════════════════════════════════════════
def build_header():
    announcement = container(
        {"content_width": "full", "background_background": "classic",
         "background_color": C["brown"], **pad(9, 16, 9, 16)},
        [label("Free local delivery in Orlando on orders over $75 · "
               "Same-day gifting available · Corporate gifting specialists",
               color=C["cream"], align="center", size=10.5, spacing=2.5)])

    logo = col([
        heading("JULIA WISTERIA", tag="div", color=C["brown"], family=SERIF,
                size=17, weight=600, spacing=4.5, transform="uppercase"),
        heading("The Art of Artisan Gifting", tag="div", color=C["rose"],
                family=SCRIPT, size=12, weight=400),
    ], width=25, settings={"flex_justify_content": "center"})

    menu = col([el("widget", {
        "menu": "principal",
        "layout": "horizontal", "align_items": "center",
        "pointer": "none",
        "toggle": "burger", "toggle_align": "right",
        "dropdown": "tablet",
        "menu_typography_typography": "custom",
        "menu_typography_font_family": SANS,
        "menu_typography_font_size": px(10),
        "menu_typography_font_weight": "500",
        "menu_typography_text_transform": "uppercase",
        "menu_typography_letter_spacing": px(2.5),
        "color_menu_item": C["brown"],
        "color_menu_item_hover": C["rose"],
    }, widget="nav-menu")], width=50,
        settings={"flex_justify_content": "center",
                  "flex_align_items": "center"})

    icons = col([row([
        el("widget", {"skin": "full_screen",
                      "toggle_button_content": "icon"},
           widget="search-form"),
        el("widget", {"icon": "bag-medium",
                      "items_indicator": "bubble",
                      "show_subtotal": "",
                      "toggle_button_icon_color": C["brown"],
                      "items_indicator_color": "#FFFFFF",
                      "items_indicator_background_color": C["rose"]},
           widget="woocommerce-menu-cart"),
    ], settings={"flex_justify_content": "flex-end",
                 "flex_align_items": "center",
                 "flex_gap": {"unit": "px", "size": 18,
                              "column": "18", "row": "18"}})],
        width=25, settings={"flex_justify_content": "center"})

    bar = container(
        {"content_width": "boxed", "flex_direction": "row",
         "background_background": "classic",
         "background_color": "rgba(249,242,235,0.97)",
         "min_height": px(74),
         "flex_align_items": "center", **pad(0, 52, 0, 52),
         "border_border": "solid",
         "border_width": {"unit": "px", "top": "0", "right": "0",
                          "bottom": "1", "left": "0", "isLinked": False},
         "border_color": "rgba(90,70,66,0.07)",
         # ── Sticky al hacer scroll (efecto de movimiento de Pro) ──
         "sticky": "top",
         "sticky_on": ["desktop", "tablet", "mobile"],
         "sticky_offset": 0,
         "sticky_offset_tablet": 0,
         "sticky_offset_mobile": 0,
         "sticky_effects_offset": 0,
         "z_index": 200,
         # sombra suave solo cuando queda pegado
         "sticky_box_shadow_box_shadow_type": "yes",
         "sticky_box_shadow_box_shadow": {
             "horizontal": 0, "vertical": 4, "blur": 24, "spread": 0,
             "color": "rgba(90,70,66,0.10)"}},
        [logo, menu, icons])

    return [announcement, bar]


# ════════════════════════════════════════════════════════════════════
# FOOTER (Theme Builder)
# ════════════════════════════════════════════════════════════════════
def build_footer():
    brand = col([
        heading("JULIA WISTERIA", tag="div", color=C["brown"], family=SERIF,
                size=16, weight=600, spacing=4, transform="uppercase"),
        heading("The Art of Artisan Gifting", tag="div", color=C["rose"],
                family=SCRIPT, size=14, weight=400),
        para("Thoughtfully crafted gift boxes celebrating life's most "
             "meaningful moments, delivered across Orlando, FL and beyond.",
             size=12.5),
        el("widget", {"social_icon_list": [
            {"_id": nid(), "social_icon": {"value": "fab fa-instagram",
                                           "library": "fa-brands"},
             "link": {"url": "#"}},
            {"_id": nid(), "social_icon": {"value": "fab fa-facebook-f",
                                           "library": "fa-brands"},
             "link": {"url": "#"}},
            {"_id": nid(), "social_icon": {"value": "fab fa-pinterest-p",
                                           "library": "fa-brands"},
             "link": {"url": "#"}},
            {"_id": nid(), "social_icon": {"value": "fab fa-linkedin-in",
                                           "library": "fa-brands"},
             "link": {"url": "#"}},
        ], "shape": "square", "align": "left",
            "icon_color": "custom", "icon_primary_color": "rgba(0,0,0,0)",
            "icon_secondary_color": C["brown"], "icon_size": px(13)},
            widget="social-icons"),
    ], width=40, tablet=100, mobile=100)

    def nav_col(title, items):
        return col([
            heading(title, tag="h4", color=C["brown"], family=SANS, size=9,
                    weight=600, transform="uppercase", spacing=3),
            spacer(12),
            link_list(items),
        ], width=20, tablet=30, mobile=50)

    grid = row([
        brand,
        nav_col("Shop", [("All Collections", "/shop/"),
                         ("Gift Boxes", "/shop/"),
                         ("Corporate Gifts", "/corporate/"),
                         ("Custom Orders", "/build-your-box/"),
                         ("Seasonal Editions", "/shop/")]),
        nav_col("Company", [("Our Story", "/our-story/"),
                            ("Our Artisans", "/our-story/"),
                            ("Press", "#"), ("Careers", "#"),
                            ("Contact Us", "#")]),
        nav_col("Support", [("Shipping & Delivery", "#"),
                            ("Returns & Exchanges", "#"), ("FAQ", "#"),
                            ("Privacy Policy", "#"),
                            ("Terms of Service", "#")]),
    ], stack="wrap", settings={"flex_gap": {"unit": "px", "size": 48,
                              "column": "48", "row": "48"}})

    bottom = row([
        col([texted("© 2025 Julia Wisteria LLC · All rights reserved · "
                    "Orlando, Florida", size=11, family=SANS, weight=300)],
            width=60),
        col([heading("Orlando, Florida ✦", tag="div", color=C["rose"],
                     family=SCRIPT, size=20, weight=400, ),], width=40,
            settings={"flex_align_items": "flex-end"}),
    ], settings={"border_border": "solid",
                 "border_width": {"unit": "px", "top": "1", "right": "0",
                                  "bottom": "0", "left": "0",
                                  "isLinked": False},
                 "border_color": "rgba(90,70,66,0.1)",
                 **pad(28, 0, 0, 0)})

    return [container(
        {"background_background": "classic",
         "background_color": C["creamd"], **pad(72, 52, 36, 52),
         "flex_gap": {"unit": "px", "size": 52, "column": "52",
                      "row": "52"}},
        [grid, bottom])]


# ════════════════════════════════════════════════════════════════════
# HOME
# ════════════════════════════════════════════════════════════════════
def build_home():
    hero = container({
        "content_width": "boxed",
        "min_height": {"unit": "vh", "size": 85, "sizes": []},
        "flex_justify_content": "center",
        "background_background": "gradient",
        "background_color": "#EDD9C6", "background_color_b": "#BAA088",
        "background_gradient_type": "linear",
        "background_gradient_angle": {"unit": "deg", "size": 120,
                                      "sizes": []},
        "background_overlay_background": "gradient",
        "background_overlay_color": "rgba(40,28,26,0.58)",
        "background_overlay_color_b": "rgba(40,28,26,0)",
        "background_overlay_gradient_type": "linear",
        "background_overlay_gradient_angle": {"unit": "deg", "size": 90,
                                              "sizes": []},
        **pad(80, 80, 80, 80)},
        [
        eyebrow("Welcome to", color="rgba(249,242,235,0.85)", size=34),
        heading("The Art of <em>Artisan</em> Gifting.", tag="h1",
                color="#FFFFFF", family=SERIF, size=68, weight=300,
                height=1.06),
        spacer(8),
        label("Premium handcrafted gift boxes for every milestone — "
              "curated for Orlando's most memorable moments",
              color="rgba(249,242,235,0.72)"),
        spacer(20),
        row([
            button("Shop the Collection", "/shop/", bg="#FFFFFF",
                   color=C["brown"]),
            button("Corporate Gifting", "/corporate/", bg=None,
                   color="rgba(255,255,255,0.85)",
                   border="rgba(255,255,255,0.55)"),
        ], settings={"flex_gap": {"unit": "px", "size": 14, "column": "14",
                                  "row": "14"}}),
    ])

    trust = container(
        {"content_width": "full", "background_background": "classic",
         "background_color": C["brown"], **pad(12, 16, 12, 16)},
        [label("Artisan Crafted ✦ Same-Day Orlando Delivery ✦ Corporate "
               "Specialists ✦ Fully Customizable ✦ Premium Local Products "
               "✦ Gift Wrapping Included ✦ Handwritten Notecards",
               color=C["cream"], align="center", size=9.5, spacing=3)])

    pillars = container({**pad(52, 48, 52, 48)}, [row([
        col([icon_box("fas fa-gift", "Individual Gift Boxes",
                      "We help you surprise the people who matter most with "
                      "thoughtfully curated artisan boxes for every occasion "
                      "— birthdays, anniversaries, baby showers, and beyond.",
                      "/shop/")], width=33),
        col([icon_box("fas fa-briefcase", "Corporate Gifting",
                      "We revolutionize corporate gifting culture. Custom "
                      "branded boxes for clients, employees, and events — "
                      "white-glove service with a personal touch that leaves "
                      "a lasting impression.", "/corporate/")], width=33),
        col([icon_box("fas fa-plus-circle", "Build Your Own Box",
                      "Curate something completely yours. Choose from our "
                      "selection of premium local products and create a "
                      "fully personalized gift box that tells your unique "
                      "story.", "/build-your-box/")], width=33),
    ])])

    collections = container({**pad(80, 48, 80, 48)}, [
        *section_header("Shop by Collection", "Find the Perfect Box",
                        "Thoughtfully organized for every occasion and "
                        "recipient"),
        spacer(36),
        el("widget", {"number": "4", "columns": "4", "columns_tablet": "2",
                      "columns_mobile": "2"},
           widget="wc-categories"),
    ])

    products = container(
        {"background_background": "classic",
         "background_color": "#FFFFFF", **pad(80, 48, 80, 48)}, [
        *section_header("Our Curated Selection", "Signature Gift Boxes",
                        "Each box assembled by hand with premium artisanal "
                        "products — made for Orlando's most meaningful "
                        "moments"),
        spacer(36),
        el("widget", {"columns": 3, "columns_tablet": 2, "columns_mobile": 2,
                      "rows": 2, "paginate": "",
                      "orderby": "date", "order": "desc"},
           widget="woocommerce-products"),
        spacer(36),
        button("View All Collections", "/shop/", align="center"),
    ])

    featured = row([
        col([el("widget", {"image": {"url": "", "id": ""},
                           "image_size": "full"}, widget="image")],
            width=53, settings={
                "background_background": "gradient",
                "background_color": "#EAD6C2",
                "background_color_b": "#C6AA90",
                "background_gradient_type": "linear",
                "background_gradient_angle": {"unit": "deg", "size": 145,
                                              "sizes": []},
                "min_height": px(580), "min_height_mobile": px(320),
                "flex_justify_content": "center",
                "flex_align_items": "center", **pad(60, 60, 60, 60)}),
        col([
            label("● Featured Collection", color=C["muted"], size=9.5,
                  spacing=2.5),
            eyebrow("Most Loved"),
            heading("The Romance Box", tag="h2", family=SERIF, size=44,
                    weight=300, height=1.12),
            para("Our signature bestseller — a love letter in a box. "
                 "Artisan-curated with premium dried florals, hand-poured "
                 "candles, and indulgent local treats. The gift that never "
                 "fails to move hearts."),
            spacer(8),
            heading("WHAT'S INSIDE", tag="h4", family=SANS, size=9,
                    weight=600, transform="uppercase", spacing=2.5),
            icon_list(["Hand-poured soy candle — Rose & Jasmine",
                       "Artisan dried floral arrangement",
                       "Premium chocolate truffles (6 pc)",
                       "Herbal bath salts & body oil",
                       "Handwritten personalized notecard"]),
            heading("$89.00", tag="div", family=SERIF, size=30, weight=500),
            spacer(8),
            row([
                button("Add to Cart", "/product/the-romance-box/"),
                button("View Details", "/product/the-romance-box/",
                       bg=None, color=C["brown"], border=C["brown"]),
            ], settings={"flex_gap": {"unit": "px", "size": 12,
                                      "column": "12", "row": "12"}}),
        ], width=47, settings={"flex_justify_content": "center",
                               **pad(80, 72, 80, 60)}),
    ], inner=False, settings={
        "content_width": "full",
        "background_background": "classic",
        "background_color": C["cream"],
        "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0"}})

    about = row([
        col([
            heading("J", tag="div", color="rgba(249,242,235,0.45)",
                    align="center", family=SERIF, size=112, weight=300,
                    height=1),
            heading("Wisteria", tag="div", color="rgba(249,242,235,0.4)",
                    align="center", family=SCRIPT, size=26, weight=400),
        ], width=50, settings={
            "background_background": "gradient",
            "background_color": "#CABAAE", "background_color_b": "#A89086",
            "background_gradient_type": "linear",
            "background_gradient_angle": {"unit": "deg", "size": 145,
                                          "sizes": []},
            "min_height": px(500), "min_height_mobile": px(300), "flex_justify_content": "center"}),
        col([
            eyebrow("Our Philosophy"),
            heading("Gifting as an <em>Art Form</em>", tag="h2",
                    family=SERIF, size=42, weight=300, height=1.12),
            para("Every Julia Wisteria box is a love letter. We believe the "
                 "most meaningful gifts aren't just beautiful — they tell a "
                 "story. Sourced from local Orlando artisans and curated "
                 "with an unwavering eye for quality, each box is designed "
                 "to leave a lasting impression long after the ribbon is "
                 "untied."),
            spacer(16),
            row([
                col([counter(500, "+", "Boxes delivered")], width=33),
                col([counter(100, "%", "Handcrafted")], width=33),
                col([
                    heading("Local", tag="div", family=SERIF, size=38,
                            weight=300),
                    label("Orlando artisans", size=9.5),
                ], width=33),
            ]),
            spacer(16),
            button("Discover Our Story", "/our-story/"),
        ], width=50, settings={
            "background_background": "classic",
            "background_color": C["creamd"],
            "flex_justify_content": "center", **pad(80, 80, 80, 80)}),
    ], inner=False, settings={
        "content_width": "full",
        "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0"}})

    def testi_col(quote, name):
        return col([stars(), testimonial(quote, name, "")], width=33,
                   settings=pad(40, 36, 40, 36))

    testimonials = container(
        {"background_background": "classic",
         "background_color": "#FFFFFF", **pad(88, 48, 88, 48)}, [
        *section_header("Client Stories", "Words from Our Community",
                        "Trusted by Orlando's finest individuals and "
                        "businesses"),
        spacer(36),
        row([
            testi_col("The most stunning gift box I've ever received. Every "
                      "detail was perfect — from the packaging to the "
                      "artisanal treats inside. Julia Wisteria truly "
                      "elevated our corporate gifting.",
                      "Sarah M. — Marketing Director, Orlando"),
            testi_col("We ordered 50 boxes for our annual client "
                      "appreciation event. The response was overwhelming. "
                      "Our clients are still talking about it months later. "
                      "Absolutely world-class.",
                      "James R. — CEO, Florida Tech Group"),
            testi_col("Absolutely magical. The attention to detail is "
                      "unparalleled. I sent the Romance Box for my best "
                      "friend's birthday and she was moved to tears. This "
                      "is gifting perfected.", "Natalie V. — Orlando, FL"),
        ]),
    ])

    corporate_cta = container(
        {"background_background": "classic",
         "background_color": C["brown"], **pad(96, 48, 96, 48)}, [
        *section_header("For Businesses", "Elevate Your Corporate Gifting",
                        "", dark=True)[:2],
        para("From client appreciation to employee milestones, Julia "
             "Wisteria transforms corporate gifting into an unforgettable "
             "experience. Custom branded boxes, bulk orders, and "
             "white-glove delivery — tailored to represent your brand with "
             "elegance.", color="rgba(249,242,235,0.62)", align="center",
             size=13),
        spacer(20),
        row([
            button("Request a Custom Quote", "/corporate/", bg=C["rose"],
                   color="#FFFFFF", hover_bg="#9E7373"),
            button("Learn More", "/corporate/", bg=None,
                   color="rgba(249,242,235,0.8)",
                   border="rgba(249,242,235,0.4)"),
        ], settings={"flex_justify_content": "center",
                     "flex_gap": {"unit": "px", "size": 14, "column": "14",
                                  "row": "14"}}),
    ])

    newsletter = container(
        {"background_background": "classic",
         "background_color": C["cream"], **pad(72, 48, 72, 48)}, [
        heading("Join the Julia Wisteria World", tag="h3", align="center",
                family=SERIF, size=36, weight=300),
        label("Early access to new collections, seasonal boxes & gifting "
              "inspiration", align="center"),
        spacer(20),
        container({"content_width": "full",
                   "width": {"unit": "px", "size": 440, "sizes": []},
                   "align_self": "center"}, [
            el("widget", {
                "form_name": "Newsletter",
                "form_fields": [
                    {"_id": nid(), "custom_id": "email",
                     "field_type": "email", "required": "true",
                     "placeholder": "your@email.com",
                     "field_label": "Email", "width": "70"},
                ],
                "show_labels": "",
                "button_text": "SUBSCRIBE", "button_width": "30",
                "button_background_color": C["brown"],
                "button_text_color": C["cream"],
                "button_border_radius": {"unit": "px", "top": "0",
                                         "right": "0", "bottom": "0",
                                         "left": "0", "isLinked": True},
            }, widget="form"),
        ], inner=True),
    ])

    return [hero, trust, pillars, collections, products, featured, about,
            testimonials, corporate_cta, newsletter]


# ════════════════════════════════════════════════════════════════════
# ABOUT / OUR STORY
# ════════════════════════════════════════════════════════════════════
def build_about():
    hero = container({
        "background_background": "gradient",
        "background_color": C["cream"], "background_color_b": C["creamd"],
        "background_gradient_type": "linear",
        "background_gradient_angle": {"unit": "deg", "size": 160,
                                      "sizes": []},
        "flex_align_items": "center", **pad(96, 48, 96, 48)}, [
        eyebrow("Our Journey", align="center", size=32),
        heading("Crafted with <em>Purpose</em>", tag="h1", align="center",
                family=SERIF, size=58, weight=300),
        spacer(8),
        para("Julia Wisteria began as a simple idea — that a gift should "
             "feel like an embrace. Born in Orlando, Florida, our story is "
             "one of passion, artisanship, and the belief that every moment "
             "deserves to be celebrated beautifully.", align="center"),
    ])

    mission = container({**pad(80, 48, 80, 48)}, [
        *section_header("Our Mission", "More Than a Gift Box", ""),
        para("We exist to make people feel seen, celebrated, and loved — "
             "through the art of thoughtful gifting. Every ribbon tied, "
             "every item curated, every box sealed with intention is our "
             "way of helping you speak when words fall short.",
             align="center"),
        spacer(8),
        label("Orlando, Florida", align="center", size=10),
    ])

    founder = row([
        col([
            heading("J", tag="div", color="rgba(249,242,235,0.45)",
                    align="center", family=SERIF, size=112, weight=300,
                    height=1),
            heading("Julia", tag="div", color="rgba(249,242,235,0.4)",
                    align="center", family=SCRIPT, size=26, weight=400),
        ], width=45, settings={
            "background_background": "gradient",
            "background_color": "#CABAAE", "background_color_b": "#A89086",
            "background_gradient_type": "linear",
            "background_gradient_angle": {"unit": "deg", "size": 145,
                                          "sizes": []},
            "min_height": px(520), "min_height_mobile": px(320), "flex_justify_content": "center"}),
        col([
            eyebrow("Meet the Founder"),
            heading("Julia's <em>Vision</em>", tag="h2", family=SERIF,
                    size=42, weight=300),
            para("Julia grew up surrounded by the warmth of handmade things "
                 "— her grandmother's kitchen, her mother's garden, the "
                 "artisan markets of downtown Orlando. When she began "
                 "creating gift boxes in 2020, it wasn't a business plan. "
                 "It was a love language made tangible."),
            para("Today, Julia Wisteria is a reflection of everything she "
                 "believed a gift could be: intentional, beautiful, and "
                 "deeply personal. Every artisan partner is chosen by Julia "
                 "herself, every product tested at her own table, every box "
                 "approved before it leaves the studio. Her standard is "
                 "simple — if she wouldn't be moved to receive it, it "
                 "doesn't ship."),
            para("Based in Orlando, Florida, Julia's mission is to keep "
                 "gifting local, keep it artisan, and keep it extraordinary "
                 "— one perfectly tied ribbon at a time."),
            heading("Julia", tag="div", color=C["rose"], family=SCRIPT,
                    size=40, weight=400),
        ], width=55, settings={
            "background_background": "classic",
            "background_color": C["creamd"],
            "flex_justify_content": "center", **pad(72, 72, 72, 60)}),
    ], inner=False, settings={
        "content_width": "full",
        "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0"}})

    values = container({**pad(80, 48, 80, 48)}, [
        *section_header("The Heart of Everything We Do", "What We Stand For",
                        "Four principles that guide every box we build"),
        spacer(36),
        row([
            col([icon_box("fas fa-bullseye", "Intentionality",
                          "Every item is chosen with purpose. We believe in "
                          "quality over quantity and meaning over trends. "
                          "Nothing enters a Julia Wisteria box by accident.")],
                width=25),
            col([icon_box("fas fa-heart", "Connection",
                          "Gifts are bridges between hearts. We help you "
                          "strengthen relationships that matter most — with "
                          "clients, colleagues, family, and friends.")],
                width=25),
            col([icon_box("fas fa-map-marker-alt", "Local Love",
                          "We partner exclusively with Orlando-based "
                          "artisans, keeping our community thriving. Every "
                          "purchase supports a local maker and their "
                          "craft.")], width=25),
            col([icon_box("fas fa-award", "Excellence",
                          "From packaging to product, we hold every detail "
                          "to the highest standard of luxury. Because you "
                          "deserve to give — and receive — nothing less.")],
                width=25),
        ], stack="column"),
    ])

    def milestone(year, title, text):
        return col([
            heading(year, tag="div", color=C["rose"], family=SERIF, size=38,
                    weight=300),
            heading(title, tag="h3", family=SERIF, size=24, weight=400),
            para(text, size=13),
        ], width=50, settings=pad(0, 24, 32, 0))

    timeline = container(
        {"background_background": "classic",
         "background_color": C["cream"], **pad(80, 48, 56, 48)}, [
        *section_header("Then & Now", "Our Journey",
                        "From a kitchen table in Orlando to gifting over "
                        "500 families"),
        spacer(36),
        row([
            milestone("2020", "The First Box",
                      "Julia assembles the very first gift box in her "
                      "Orlando kitchen, gifting it to a friend who had just "
                      "gone through a difficult month. The response changes "
                      "everything — three orders follow within a week, all "
                      "from word of mouth alone."),
            milestone("2021", "Going Official",
                      "Julia Wisteria is born as a formal business. The "
                      "first 50 orders are hand-delivered across Orlando in "
                      "Julia's own car, each box accompanied by a "
                      "personally written card. The brand's voice — warm, "
                      "artisan, intentional — is established from day one."),
        ]),
        row([
            milestone("2022", "Corporate Discovery",
                      "Local businesses begin requesting custom branded "
                      "boxes for client gifts and employee milestones. "
                      "Corporate gifting becomes a pillar of the brand, "
                      "opening a new chapter of scale without ever "
                      "sacrificing the handmade touch."),
            milestone("2024", "Growing Family",
                      "The team expands to 8 artisans — each a specialist "
                      "in their craft, each sharing Julia's obsession with "
                      "quality. Over 500 boxes delivered. Still every box "
                      "made with the same love as the first one assembled "
                      "on that kitchen table."),
        ]),
    ])

    artisans = container({**pad(80, 48, 80, 48)}, [
        *section_header("The Hands Behind the Magic", "Our Local Artisans",
                        "Every product inside a Julia Wisteria box is made "
                        "by someone you can name"),
    ])

    return [hero, mission, founder, values, timeline, artisans]


# ════════════════════════════════════════════════════════════════════
# CORPORATE
# ════════════════════════════════════════════════════════════════════
def build_corporate():
    hero = container(
        {"background_background": "classic",
         "background_color": C["brown"],
         "flex_align_items": "center", **pad(96, 48, 72, 48)}, [
        eyebrow("For Businesses", color=C["sage"], align="center", size=30),
        heading("Elevate Your Corporate <em>Gifting</em>", tag="h1",
                color=C["cream"], align="center", family=SERIF, size=54,
                weight=300),
        spacer(8),
        para("Transform your corporate relationships into unforgettable "
             "experiences. From client appreciation to employee milestones, "
             "Julia Wisteria curates premium artisan gift boxes that speak "
             "volumes — branded, beautiful, and delivered with white-glove "
             "care across Orlando and beyond.",
             color="rgba(249,242,235,0.62)", align="center"),
        spacer(20),
        row([
            button("Request a Quote", "#quote", bg=C["rose"],
                   color="#FFFFFF", hover_bg="#9E7373"),
            button("View Packages", "#packages", bg=None,
                   color="rgba(249,242,235,0.8)",
                   border="rgba(249,242,235,0.4)"),
        ], settings={"flex_justify_content": "center",
                     "flex_gap": {"unit": "px", "size": 14, "column": "14",
                                  "row": "14"}}),
        spacer(48),
        row([
            col([counter(500, "+", "Boxes Delivered")], width=25, mobile=50),
            col([counter(98, "%", "Client Satisfaction")], width=25,
                mobile=50),
            col([counter(48, "h", "Average Turnaround")], width=25,
                mobile=50),
            col([counter(10, "+", "Minimum Order")], width=25, mobile=50),
        ], stack="wrap"),
    ])

    process = container({**pad(80, 48, 80, 48)}, [
        *section_header("Effortless from Start to Finish", "Simple Process",
                        "Three steps to extraordinary gifting"),
        spacer(36),
        row([
            col([icon_box("fas fa-comments", "1 · Consult",
                          "Tell us your vision, budget, and occasion. Our "
                          "corporate gifting specialists will guide you "
                          "through every option and help you define the "
                          "perfect gifting strategy for your brand.")],
                width=33),
            col([icon_box("fas fa-box-open", "2 · Curate",
                          "We handcraft your custom box selection, sourcing "
                          "only the finest artisan products from our "
                          "trusted Orlando partners. Every element is "
                          "chosen with intention and precision.")],
                width=33),
            col([icon_box("fas fa-truck", "3 · Deliver",
                          "White-glove delivery to your recipients — "
                          "whether across Orlando or nationwide. Each box "
                          "arrives pristine, on time, and wrapped in the "
                          "unmistakable Julia Wisteria elegance.")],
                width=33),
        ]),
    ])

    def package(name, tagline, price, period, features, ribbon=False):
        s = {"heading": name, "sub_heading": tagline,
             "currency_symbol": "dollar", "price": price,
             "currency_format": ",", "period": period,
             "features_list": [
                 {"_id": nid(), "item_text": f,
                  "selected_item_icon": {"value": "fas fa-check",
                                         "library": "fa-solid"},
                  "item_icon_color": "custom",
                  "item_icon_color_custom": C["rose"]} for f in features],
             "button_text": "GET STARTED",
             # El plan viaja en la URL → el formulario lo pre-selecciona
             "link": {"url": "?plan={}#quote".format(name),
                      "is_external": "", "nofollow": ""},
             "header_bg_color": C["creamd"],
             "heading_color": C["brown"], "sub_heading_color": C["muted"],
             "price_color": C["brown"],
             "button_background_color": C["brown"],
             "button_text_color": C["cream"],
             "features_list_color": C["muted"]}
        s.update(typo("heading_typography", family=SERIF, size=28,
                      weight=400))
        s.update(typo("price_typography", family=SERIF, size=44,
                      weight=300))
        s.update(typo("features_list_typography", family=SANS, size=12.5,
                      weight=300))
        if ribbon:
            s.update({"show_ribbon": "yes", "ribbon_title": "Most Popular",
                      "ribbon_horizontal_position": "right"})
        return el("widget", s, widget="price-table")

    packages = container(
        {"background_background": "classic",
         "background_color": C["cream"], "_element_id": "packages",
         **pad(80, 48, 80, 48)}, [
        *section_header("Designed for Every Budget", "Corporate Packages",
                        "All packages include professional packaging & "
                        "handwritten notecards"),
        spacer(36),
        row([
            col([package("Essential", "Perfect for small teams", "75",
                         "Per box · Min. 10 units",
                         ["Branded tissue paper", "Handwritten notecards",
                          "Standard gift box", "5 product slots",
                          "Email delivery confirmation"])], width=33),
            col([package("Signature", "Our most loved package", "120",
                         "Per box · Min. 25 units",
                         ["Custom branded box",
                          "Satin ribbon in brand colors",
                          "Premium product selection",
                          "Handwritten notecards", "Personalized inserts",
                          "Same-day Orlando delivery",
                          "Dedicated account manager",
                          "Digital gift tracking"], ribbon=True)], width=33),
            col([package("Prestige", "The ultimate impression", "185",
                         "Per box · Min. 10 units",
                         ["Fully custom packaging", "Gold foil embossing",
                          "Luxury product curation",
                          "Premium courier delivery",
                          "Brand experience consultation",
                          "Nationwide shipping",
                          "Post-delivery report"])], width=33),
        ]),
    ])

    def field(cid, ftype, lbl, width="50", options=None):
        f = {"_id": nid(), "custom_id": cid, "field_type": ftype,
             "field_label": lbl, "placeholder": lbl, "width": width}
        if options:
            f["field_options"] = "\n".join(options)
        return f

    quote_form = container({"_element_id": "quote", **pad(80, 48, 80, 48)}, [
        *section_header("Let's Create Something Beautiful",
                        "Request a Custom Quote",
                        "Tell us about your gifting vision and we'll be in "
                        "touch within 24 hours"),
        spacer(36),
        container({"content_width": "full",
                   "width": {"unit": "px", "size": 760, "sizes": []},
                   "align_self": "center"}, [
            el("widget", {
                "form_name": "Corporate Quote",
                "form_fields": [
                    field("plan", "select", "Plan of Interest", width="100",
                          options=["Essential", "Signature", "Prestige",
                                   "Custom / Not sure"]),
                    field("first_name", "text", "First Name"),
                    field("last_name", "text", "Last Name"),
                    field("company", "text", "Company Name"),
                    field("email", "email", "Email Address"),
                    field("phone", "tel", "Phone Number"),
                    field("boxes", "number", "Number of Boxes"),
                    field("budget", "select", "Budget per Box",
                          options=["$50 – $75", "$75 – $120", "$120 – $185",
                                   "$185+"]),
                    field("occasion", "select", "Event / Occasion",
                          options=["Client Appreciation",
                                   "Employee Milestones", "Holiday Gifting",
                                   "Company Event", "Other"]),
                    field("message", "textarea", "Message", width="100"),
                ],
                "button_text": "SEND INQUIRY", "button_width": "100",
                "button_background_color": C["brown"],
                "button_text_color": C["cream"],
            }, widget="form"),
        ], inner=True),
    ])

    clients = container(
        {"background_background": "classic",
         "background_color": C["creamd"], **pad(48, 48, 48, 48)}, [
        label("Trusted by Orlando's finest", align="center", size=10),
        spacer(12),
        heading("Marriott Hotels · Orlando Health · KPMG · Advent Health · "
                "Universal · Disney", tag="div", color=C["muted"],
                align="center", family=SERIF, size=20, weight=400),
        spacer(28),
        testimonial("We ordered 50 boxes for our annual client appreciation "
                    "event. The response was overwhelming. Our clients are "
                    "still talking about it months later. Absolutely "
                    "world-class.",
                    "James R., CEO · Florida Tech Group", ""),
    ])

    return [hero, process, packages, quote_form, clients]


# ════════════════════════════════════════════════════════════════════
# SHOP ALL (Theme Builder → Product Archive)
# ════════════════════════════════════════════════════════════════════
def build_shop_archive():
    pills = [("All", "/shop/"),
             ("For Her", "/product-category/for-her/"),
             ("For Him", "/product-category/for-him/"),
             ("Corporate", "/product-category/corporate/"),
             ("Baby", "/product-category/baby/"),
             ("Seasonal", "/product-category/seasonal/"),
             ("Custom", "/product-category/custom/")]

    def pill(text, url, active=False):
        return el("widget", {
            "text": text,
            "link": {"url": url, "is_external": "", "nofollow": ""},
            "background_color": C["brown"] if active else "rgba(0,0,0,0)",
            "button_text_color": C["cream"] if active else C["brown"],
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1",
                             "bottom": "1", "left": "1", "isLinked": True},
            "border_color": C["brown"] if active else "rgba(90,70,66,0.25)",
            "border_radius": {"unit": "px", "top": "20", "right": "20",
                              "bottom": "20", "left": "20",
                              "isLinked": True},
            "text_padding": {"unit": "px", "top": "8", "right": "20",
                             "bottom": "8", "left": "20",
                             "isLinked": False},
            "hover_color": C["cream"],
            "button_background_hover_color": C["brown"],
            **typo("typography", family=SANS, size=10, weight=500,
                   transform="uppercase", spacing=2),
        }, widget="button")

    header = container(
        {"background_background": "classic",
         "background_color": C["cream"],
         "flex_align_items": "center", **pad(64, 48, 48, 48)}, [
        el("widget", {"align": "center", "text_color": C["muted"],
                      **typo("typography", family=SANS, size=10,
                             weight=400, transform="uppercase",
                             spacing=2)},
           widget="woocommerce-breadcrumb"),
        spacer(8),
        # Título dinámico del archivo vía shortcode robusto (el widget
        # theme-archive-title de Pro no resuelve el contexto en archivos Woo)
        el("widget", {"shortcode": "[jw_archive_title]"},
           widget="shortcode"),
        label("Thoughtfully curated gift boxes for every occasion",
              align="center", size=10.5),
    ])

    filters = container(
        {"background_background": "classic",
         "background_color": C["cream"], **pad(0, 48, 40, 48)}, [
        row([pill(t, u, active=(t == "All")) for t, u in pills],
            settings={"flex_justify_content": "center",
                      "flex_wrap": "wrap",
                      "flex_gap": {"unit": "px", "size": 10,
                                   "column": "10", "row": "10"}}),
    ])

    grid = container({**pad(56, 48, 80, 48)}, [
        el("widget", {"columns": 3, "columns_tablet": 2, "columns_mobile": 2,
                      "rows": 4, "paginate": "yes",
                      "allow_order": "yes", "show_result_count": "yes"},
           widget="wc-archive-products"),
    ])

    return [header, filters, grid]


# ════════════════════════════════════════════════════════════════════
# PÁGINA DE PRODUCTO (Theme Builder → Single Product)
# ════════════════════════════════════════════════════════════════════
def build_single_product():
    breadcrumb = container({**pad(24, 48, 0, 48)}, [
        el("widget", {"text_color": C["muted"],
                      **typo("typography", family=SANS, size=10,
                             weight=400, transform="uppercase",
                             spacing=2)},
           widget="woocommerce-breadcrumb"),
    ])

    gallery = col([
        el("widget", {"sale_flash": "yes"},
           widget="woocommerce-product-images"),
    ], width=52, settings={
        "background_background": "gradient",
        "background_color": "#FBF0EC", "background_color_b": "#E4CEC6",
        "background_gradient_type": "linear",
        "background_gradient_angle": {"unit": "deg", "size": 145,
                                      "sizes": []},
        **pad(48, 48, 48, 48)})

    summary = col([
        eyebrow("Handcrafted in Orlando"),
        el("widget", {"title_color": C["brown"],
                      **typo("typography", family=SERIF, size=44,
                             weight=300, height=1.1)},
           widget="woocommerce-product-title"),
        el("widget", {"wc_style_warning": "",
                      "star_color": C["sage"],
                      "link_color": C["muted"],
                      "text_typography_typography": "custom",
                      "text_typography_font_family": SANS,
                      "text_typography_font_size": px(11)},
           widget="woocommerce-product-rating"),
        el("widget", {"price_color": C["brown"],
                      **typo("typography", family=SERIF, size=30,
                             weight=500)},
           widget="woocommerce-product-price"),
        spacer(8),
        el("widget", {"text_color": C["muted"],
                      **typo("typography", family=SANS, size=13.5,
                             weight=300, height=1.9)},
           widget="woocommerce-product-short-description"),
        spacer(8),
        el("widget", {"show_quantity": "yes",
                      "button_background_color": C["brown"],
                      "button_text_color": C["cream"],
                      "button_hover_background_color": C["rose"],
                      "button_border_radius": {"unit": "px", "top": "0",
                                               "right": "0", "bottom": "0",
                                               "left": "0",
                                               "isLinked": True},
                      **typo("button_typography", family=SANS, size=10,
                             weight=500, transform="uppercase", spacing=3)},
           widget="woocommerce-product-add-to-cart"),
        spacer(16),
        icon_list(["Same-day delivery available in Orlando (order by 1 PM)",
                   "Free local delivery on orders over $75",
                   "Standard shipping 3–5 business days nationwide",
                   "All boxes arrive in signature Julia Wisteria packaging"],
                  icon="fas fa-check", icon_size=10),
    ], width=48, settings={"flex_justify_content": "center",
                           **pad(56, 72, 56, 56)})

    main = row([gallery, summary], inner=False, settings={
        "content_width": "full",
        "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0"}})

    tabs = container({**pad(48, 48, 48, 48)}, [
        el("widget", {}, widget="woocommerce-product-data-tabs"),
    ])

    related = container(
        {"background_background": "classic",
         "background_color": C["cream"], **pad(72, 48, 80, 48)}, [
        *section_header("Curated just for you", "You May Also Love", ""),
        spacer(32),
        el("widget", {"posts_per_page": 4, "columns": 4},
           widget="woocommerce-product-related"),
    ])

    return [breadcrumb, main, tabs, related]


# ════════════════════════════════════════════════════════════════════
# BUILD YOUR BOX (página)
# ════════════════════════════════════════════════════════════════════
BOX_ITEMS = [
    ("Soy Candle", "Wellness", 18, "fas fa-spa"),
    ("Botanical Tea Set", "Beverage", 22, "fas fa-mug-hot"),
    ("Artisan Chocolates", "Gourmet", 24, "fas fa-cookie-bite"),
    ("Silk Eye Mask", "Beauty", 28, "fas fa-moon"),
    ("Rose Bath Salts", "Wellness", 20, "fas fa-bath"),
    ("Honey & Fig Jam", "Gourmet", 16, "fas fa-lemon"),
    ("Cashmere Hand Cream", "Beauty", 26, "fas fa-hand-holding-heart"),
    ("Dried Floral Bunch", "Botanical", 30, "fas fa-seedling"),
    ("Linen Sachet", "Home", 14, "fas fa-leaf"),
    ("Artisan Soap Bar", "Beauty", 16, "fas fa-soap"),
    ("Gold Pen", "Stationery", 22, "fas fa-pen-fancy"),
    ("Truffle Collection", "Gourmet", 32, "fas fa-cookie"),
]


def build_build_page():
    hero = container(
        {"background_background": "gradient",
         "background_color": C["cream"], "background_color_b": C["creamd"],
         "background_gradient_type": "linear",
         "background_gradient_angle": {"unit": "deg", "size": 160,
                                       "sizes": []},
         "flex_align_items": "center", **pad(72, 48, 56, 48)}, [
        eyebrow("Create Something Unique", align="center", size=32),
        heading("Build Your Box", tag="h1", align="center", family=SERIF,
                size=54, weight=300),
        label("Four simple steps to a fully personalized gift",
              align="center"),
    ])

    def step(num, title):
        return col([
            heading(num, tag="div", color=C["rose"], align="center",
                    family=SERIF, size=34, weight=300),
            label(title, align="center", size=10, spacing=2.5),
        ], width=25, mobile=50)

    steps = container({**pad(40, 48, 40, 48)}, [row([
        step("1", "Choose Size"), step("2", "Select Items"),
        step("3", "Personalize"), step("4", "Review"),
    ], stack="wrap")])

    def size_card(name, items, price, ribbon=False):
        s = {"heading": name, "sub_heading": "Up to {} items".format(items),
             "currency_symbol": "dollar", "price": price,
             "period": "starting",
             "features_list": [],
             "button_text": "SELECT THIS SIZE",
             "link": {"url": "#personalize", "is_external": "",
                      "nofollow": ""},
             "header_bg_color": C["creamd"],
             "heading_color": C["brown"], "sub_heading_color": C["muted"],
             "price_color": C["brown"],
             "button_background_color": C["brown"],
             "button_text_color": C["cream"]}
        s.update(typo("heading_typography", family=SERIF, size=28,
                      weight=400))
        s.update(typo("price_typography", family=SERIF, size=44,
                      weight=300))
        if ribbon:
            s.update({"show_ribbon": "yes", "ribbon_title": "Most Loved",
                      "ribbon_horizontal_position": "right"})
        return el("widget", s, widget="price-table")

    sizes = container(
        {"background_background": "classic",
         "background_color": C["cream"], **pad(72, 48, 72, 48)}, [
        *section_header("Step One", "Choose Your Box Size",
                        "Select the size that suits your occasion"),
        spacer(32),
        row([
            col([size_card("Petite Box", 3, "55")], width=33),
            col([size_card("Classic Box", 5, "85", ribbon=True)], width=33),
            col([size_card("Luxe Box", 8, "145")], width=33),
        ]),
    ])

    def item_card(name, cat, price, icon):
        return col([icon_box(icon, name,
                             "{} · +${}".format(cat, price))], width=25,
                   tablet=48, mobile=100,
                   settings={
                       "background_background": "classic",
                       "background_color": "#FFFFFF",
                       "border_border": "solid",
                       "border_width": {"unit": "px", "top": "1",
                                        "right": "1", "bottom": "1",
                                        "left": "1", "isLinked": True},
                       "border_color": "rgba(90,70,66,0.1)",
                       **pad(28, 24, 28, 24)})

    items_rows = []
    for i in range(0, len(BOX_ITEMS), 4):
        items_rows.append(row([item_card(*it)
                               for it in BOX_ITEMS[i:i + 4]],
                              stack="wrap",
                              settings={"flex_gap": {"unit": "px",
                                                     "size": 16,
                                                     "column": "16",
                                                     "row": "16"}}))

    items = container({**pad(72, 48, 72, 48)}, [
        *section_header("Step Two", "Select Your Items",
                        "Premium artisan products, all made by Orlando "
                        "makers"),
        spacer(32),
        *items_rows,
    ])

    def field(cid, ftype, lbl, width="50", options=None, required=False):
        f = {"_id": nid(), "custom_id": cid, "field_type": ftype,
             "field_label": lbl, "placeholder": lbl, "width": width}
        if options:
            f["field_options"] = "\n".join(options)
        if required:
            f["required"] = "true"
        return f

    personalize = container(
        {"background_background": "classic",
         "background_color": C["creamd"], **pad(72, 48, 72, 48)}, [
        *section_header("Steps Three & Four", "Personalize & Review",
                        "Tell us how to build it — we confirm your box and "
                        "total by email within 24 hours"),
        spacer(32),
        container({"content_width": "full",
                   "width": {"unit": "px", "size": 760, "sizes": []},
                   "align_self": "center"}, [
            el("widget", {
                "form_name": "Build Your Box",
                "form_fields": [
                    field("name", "text", "Your Name", required=True),
                    field("email", "email", "Your Email", required=True),
                    field("box_size", "select", "Box Size",
                          options=["Petite Box — $55 (up to 3 items)",
                                   "Classic Box — $85 (up to 5 items)",
                                   "Luxe Box — $145 (up to 8 items)"],
                          required=True),
                    field("recipient", "text", "Recipient Name"),
                    field("items", "textarea",
                          "Items for your box (list from the selection "
                          "above)", width="100", required=True),
                    field("occasion", "select", "Occasion",
                          options=["Birthday", "Anniversary", "Baby Shower",
                                   "Wedding", "Corporate Thank You",
                                   "Holiday", "Just Because"]),
                    field("ribbon", "select", "Ribbon Color",
                          options=["Blush", "Ivory", "Sage",
                                   "Chocolate Brown"]),
                    field("wrapping", "select", "Gift Wrapping",
                          options=["Standard (included)",
                                   "Premium tissue + bow (+$5)",
                                   "Luxury satin wrap (+$12)"]),
                    field("message", "textarea", "Handwritten Message",
                          width="100"),
                ],
                "button_text": "SUBMIT MY BOX →", "button_width": "100",
                "button_background_color": C["brown"],
                "button_text_color": C["cream"],
            }, widget="form"),
        ], inner=True),
        spacer(20),
        label("Free Orlando delivery on orders over $75 · Ships in 1–2 "
              "business days", align="center", size=10),
    ])

    return [hero, steps, sizes, items, personalize]


# ════════════════════════════════════════════════════════════════════
def template(title, ttype, content):
    return {"version": "0.4", "title": title, "type": ttype,
            "content": content,
            "page_settings": {"hide_title": "yes"}}


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "templates")
    os.makedirs(out, exist_ok=True)
    files = {
        "header-theme-builder.json":
            template("JW – Header", "header", build_header()),
        "footer-theme-builder.json":
            template("JW – Footer", "footer", build_footer()),
        "home-page.json":
            template("JW – Home", "page", build_home()),
        "about-page.json":
            template("JW – Our Story", "page", build_about()),
        "corporate-page.json":
            template("JW – Corporate", "page", build_corporate()),
        "shop-archive-theme-builder.json":
            template("JW – Shop All", "product-archive",
                     build_shop_archive()),
        "single-product-theme-builder.json":
            template("JW – Single Product", "product",
                     build_single_product()),
        "build-your-box-page.json":
            template("JW – Build Your Box", "page", build_build_page()),
    }
    for name, data in files.items():
        path = os.path.join(out, name)
        with open(path, "w") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
        print("✓", name)


if __name__ == "__main__":
    main()
