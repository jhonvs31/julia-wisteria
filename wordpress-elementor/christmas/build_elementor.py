#!/usr/bin/env python3
"""Julia Wisteria — Christmas Season: genera el JSON de Elementor de cada página
y plantilla (Theme Builder) a partir de widgets nativos de Elementor / Pro.

Uso: python3 build_elementor.py   → escribe out/*.json (lo aplica apply_elementor.php)

Animaciones nativas usadas: Entrance Animation (fadeInUp/zoomIn/fadeInLeft),
Motion Effects (scroll translateY, mouse tilt), Sticky (header y columnas),
Progress Tracker (barra de scroll), Text Path (sello giratorio).
El resto (blobs, marquee, brillo del titular, flotación) es CSS de Site Settings.
"""
import itertools, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
IDS = json.load(open(os.path.join(HERE, 'ids.json')))
BOXES = json.load(open(os.path.join(HERE, 'boxes.json')))
URLS = {IDS['img'][k]: v for k, v in IDS.get('url', {}).items()}
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)

_c = itertools.count(1)
def nid(): return 'jc{:05x}'.format(next(_c))

C = dict(cream='#F9F2EB', creamd='#F0E6D9', brown='#5A4642', brownl='#7A6460', rose='#B88889',
         rosel='#D4B4B5', muted='#8B7B78', wine='#6E2F3B', wined='#4A1D27', lilac='#B9A6D3',
         lilacl='#E6DDF2', white='#FFFFFF')
SERIF, SCRIPT, SANS = 'Cormorant Garamond', 'Sacramento', 'Jost'

def u(size, unit='px'): return {'unit': unit, 'size': size, 'sizes': []}
def box4(t, r, b, l, unit='px'):
    return {'unit': unit, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}
def gap(n): return {'unit': 'px', 'size': n, 'column': str(n), 'row': str(n)}
def radius(n): return {'unit': 'px', 'top': str(n), 'right': str(n), 'bottom': str(n), 'left': str(n), 'isLinked': True}

def pad(t, r, b, l, key='padding'):
    d = {key: box4(t, r, b, l)}
    d[key + '_tablet'] = box4(round(t * .72), min(r, 32), round(b * .72), min(l, 32))
    d[key + '_mobile'] = box4(round(t * .55), min(r, 20), round(b * .55), min(l, 20))
    return d

def typo(prefix, family=None, size=None, weight=None, transform=None, spacing=None,
         lh=None, style=None, t=None, m=None):
    s = {prefix + '_typography': 'custom'}
    if family: s[prefix + '_font_family'] = family
    if size:
        s[prefix + '_font_size'] = u(size)
        if t is None and size >= 18: t = round(size * (.75 if size >= 50 else .88))
        if m is None and size >= 16: m = round(size * (.5 if size >= 70 else .62 if size >= 40 else .8))
        if t: s[prefix + '_font_size_tablet'] = u(t)
        if m: s[prefix + '_font_size_mobile'] = u(m)
    if weight: s[prefix + '_font_weight'] = str(weight)
    if transform: s[prefix + '_text_transform'] = transform
    if spacing is not None: s[prefix + '_letter_spacing'] = u(spacing)
    if lh: s[prefix + '_line_height'] = u(lh, 'em')
    if style: s[prefix + '_font_style'] = style
    return s

# ---------- animación nativa ----------
def anim(name='fadeInUp', delay=0, container=False, slow=False):
    if container:
        d = {'animation': name, 'animation_delay': delay}
    else:
        d = {'_animation': name, '_animation_delay': delay}
    d['animation_duration'] = 'slow' if slow else ''
    return d

def tilt(speed=4):
    return {'motion_fx_motion_fx_mouse': 'yes', 'motion_fx_tilt_effect': 'yes', 'motion_fx_tilt_speed': u(speed)}

def parallax(speed=2, direction=''):
    return {'motion_fx_motion_fx_scrolling': 'yes', 'motion_fx_translateY_effect': 'yes',
            'motion_fx_translateY_speed': u(speed), 'motion_fx_translateY_direction': direction,
            'motion_fx_devices': ['desktop', 'tablet']}

# ---------- elementos ----------
def el(t, s, kids=None, w=None, inner=False):
    d = {'id': nid(), 'elType': t, 'settings': s, 'elements': kids or [], 'isInner': inner}
    if w: d['widgetType'] = w
    return d

def con(s, kids, inner=True, cls=''):
    base = {'content_width': 'full', 'flex_direction': 'column', 'padding': box4(0, 0, 0, 0)}
    base.update(s)
    if cls: base['css_classes'] = (base.get('css_classes', '') + ' ' + cls).strip()
    return el('container', base, kids, inner=inner)

def section(s, kids, cls=''):
    base = {'content_width': 'boxed', 'boxed_width': u(1440)}
    base.update(s)
    return con(base, kids, inner=False, cls=cls)

def row(kids, g=28, s=None, stack=True, cls=''):
    base = {'flex_direction': 'row', 'flex_gap': gap(g)}
    if stack: base['flex_direction_mobile'] = 'column'
    base.update(s or {})
    return con(base, kids, cls=cls)

def col(kids, w=50, s=None, tablet=None, mobile=100, cls=''):
    base = {'width': u(w, '%')}
    if tablet: base['width_tablet'] = u(tablet, '%')
    if mobile: base['width_mobile'] = u(mobile, '%')
    base.update(s or {})
    return con(base, kids, cls=cls)

def W(t, s, cls='', extra=None):
    if cls: s['_css_classes'] = cls
    if extra: s.update(extra)
    return el('widget', s, w=t)

def heading(text, tag='h2', color=C['brown'], align='left', cls='', extra=None, link=None, **ty):
    s = {'title': text, 'header_size': tag, 'title_color': color, 'align': align}
    if link: s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    s.update(typo('typography', **ty))
    return W('heading', s, cls, extra)

def script(text, color=C['rose'], align='left', size=34, extra=None, cls=''):
    return heading(text, 'div', color, align, cls, extra, family=SCRIPT, size=size, weight=400, lh=1.2)

def label(text, color=C['muted'], align='left', size=11, spacing=2, extra=None, cls=''):
    return heading(text, 'div', color, align, cls, extra, family=SANS, size=size, weight=400,
                   transform='uppercase', spacing=spacing, lh=2)

def text(html, color=C['brownl'], align='left', size=15, lh=1.95, cls='', extra=None, **more):
    s = {'editor': html if html.startswith('<') else '<p>%s</p>' % html, 'text_color': color, 'align': align}
    s.update(typo('typography', family=more.pop('family', SANS), size=size, weight=more.pop('weight', 300), lh=lh, **more))
    return W('text-editor', s, cls, extra)

def button(txt, url='#', solid=False, light=False, align='left', icon=True, extra=None, small=False):
    cls = 'jw-btn' + (' jw-solid' if solid else '') + (' jw-light' if light else '')
    s = {'text': txt, 'link': {'url': url, 'is_external': '', 'nofollow': ''}, 'align': align,
         'text_padding': box4(13, 24, 13, 24) if small else box4(17, 34, 17, 34),
         'border_radius': radius(999)}
    if icon:
        s.update({'selected_icon': {'value': 'fas fa-arrow-right', 'library': 'fa-solid'},
                  'icon_align': 'row-reverse', 'icon_indent': u(10)})
    s.update(typo('typography', family=SANS, size=9.5 if small else 10.5, weight=500, transform='uppercase', spacing=2.6))
    return W('button', s, cls, extra)

def chip(txt, url='', active=False, extra=None):
    s = {'text': txt, 'link': {'url': url, 'is_external': '', 'nofollow': ''},
         'background_color': C['wine'] if active else '#FFFFFF',
         'button_text_color': '#FFFFFF' if active else C['brown'],
         'button_background_hover_color': C['wine'] if active else C['lilacl'],
         'hover_color': '#FFFFFF' if active else C['brown'],
         'border_border': 'solid', 'border_width': radius(1),
         'border_color': C['wine'] if active else 'rgba(90,70,66,0.16)',
         'border_radius': radius(999), 'text_padding': box4(11, 24, 11, 24)}
    s.update(typo('typography', family=SANS, size=11, weight=400, transform='uppercase', spacing=1.8))
    return W('button', s, 'jw-chip', extra)

def image(img_id, url=None, cls='', extra=None, size='large', h=None, ht=None, hm=None, r=None):
    s = {'image': {'id': img_id, 'url': url or URLS.get(img_id, '')}, 'image_size': size, 'width': u(100, '%')}
    if h:
        s.update({'height': u(h), 'object-fit': 'cover'})
        if ht: s['height_tablet'] = u(ht)
        if hm: s['height_mobile'] = u(hm)
    if r is not None: s['image_border_radius'] = radius(r)
    return W('image', s, cls, extra)

def spacer(n): return W('spacer', {'space': u(n)})

PRODUCT_URL = {b['i']: '/product/%s/' % b['slug'] for b in BOXES}

# ════════════════════════════════════════════════════════════════════
def build_header():
    ann = section({'content_width': 'full', 'background_background': 'classic', 'background_color': C['brown'],
                   **pad(9, 16, 9, 16)}, [
        heading('Christmas Season 2026 &nbsp;<b>·</b>&nbsp; Corporate gifting, crafted with meaning &nbsp;<b>·</b>&nbsp; Orlando, Florida',
                'div', C['cream'], 'center', 'jw-ann', family=SANS, size=10.5, weight=400, transform='uppercase', spacing=2.5, m=9),
        W('progress-tracker', {'type': 'horizontal', 'relative_to': 'entire_page', 'direction': 'ltr', 'percentage': '',
                               'horizontal_height': u(2), 'progress_color': C['wine'],
                               'horizontal_border_style': 'none', 'tracker_background_color': 'rgba(0,0,0,0)'},
          'jw-progress', {'_position': 'fixed', '_offset_x': u(0), '_offset_y': u(0), '_element_width': 'initial',
                          '_element_custom_width': u(100, '%'), '_z_index': 999}),
    ])
    logo = con({'width': u(28, '%'), 'width_tablet': u(60, '%'), 'width_mobile': u(70, '%'), 'flex_justify_content': 'center'}, [
        W('image', {'image': {'id': IDS['img']['logo'], 'url': URLS.get(IDS['img']['logo'], '')}, 'image_size': 'full',
                    'align': 'left', 'width': u(118), 'width_mobile': u(96), 'link_to': 'custom', 'link': {'url': '/'},
                    'hover_animation': 'grow'}, 'jw-logo'),
    ])
    menu = con({'width': u(52, '%'), 'width_tablet': u(20, '%'), 'width_mobile': u(15, '%'),
                'flex_align_items': 'center', 'flex_justify_content': 'center'}, [
        W('nav-menu', {'menu': 'principal', 'layout': 'horizontal', 'align_items': 'center', 'pointer': 'underline',
                       'animation_line': 'grow', 'toggle': 'burger', 'toggle_align': 'right', 'dropdown': 'tablet',
                       'full_width': 'stretch', 'text_align': 'center',
                       'color_menu_item': C['brown'], 'color_menu_item_hover': C['wine'],
                       'pointer_color_menu_item_hover': C['wine'], 'color_menu_item_active': C['wine'],
                       'pointer_color_menu_item_active': C['wine'], 'pointer_width': u(1),
                       'padding_horizontal_menu_item': u(16),
                       'color_dropdown_item': C['brown'], 'background_color_dropdown_item': C['cream'],
                       'color_dropdown_item_hover': C['wine'], 'background_color_dropdown_item_hover': C['lilacl'],
                       'toggle_color': C['brown'], 'toggle_background_color': 'rgba(0,0,0,0)',
                       **typo('menu_typography', family=SANS, size=10, weight=500, transform='uppercase', spacing=2.5),
                       **typo('dropdown_typography', family=SERIF, size=26, weight=300)}),
    ])
    cart = con({'width': u(20, '%'), 'width_tablet': u(20, '%'), 'width_mobile': u(15, '%'),
                'flex_align_items': 'flex-end', 'flex_justify_content': 'center'}, [
        W('woocommerce-menu-cart', {'icon': 'bag-medium', 'items_indicator': 'bubble', 'show_subtotal': '',
                                    'alignment': 'right', 'toggle_button_icon_color': C['brown'],
                                    'toggle_button_hover_icon_color': C['wine'],
                                    'toggle_button_background_color': 'rgba(0,0,0,0)', 'toggle_button_border_width': u(0), 'toggle_button_border_color': 'rgba(0,0,0,0)',
                                    'items_indicator_text_color': '#FFFFFF', 'items_indicator_background_color': C['wine'],
                                    'toggle_icon_size': u(20)}),
    ])
    bar = section({'flex_direction': 'row', 'flex_align_items': 'center', 'flex_wrap': 'nowrap',
                   'background_background': 'classic', 'background_color': 'rgba(249,242,235,0.82)',
                   'min_height': u(84), 'min_height_mobile': u(70), **pad(0, 52, 0, 52),
                   'border_border': 'solid', 'border_width': box4(0, 0, 1, 0), 'border_color': 'rgba(90,70,66,0.07)',
                   'sticky': 'top', 'sticky_on': ['desktop', 'tablet', 'mobile'], 'sticky_offset': 0,
                   'sticky_effects_offset': 0, 'z_index': 200}, [logo, menu, cart], cls='jw-bar')
    return [ann, bar]


def build_footer():
    nl = section({'content_width': 'full', 'background_background': 'classic', 'background_color': C['lilacl'],
                  'flex_align_items': 'center', **pad(72, 48, 72, 48), 'flex_gap': gap(8)}, [
        heading('Join the Julia Wisteria World', 'h3', C['brown'], 'center', extra=anim(), family=SERIF, size=36, weight=300),
        label('Early access to new collections, seasonal boxes & gifting inspiration', align='center', extra=anim('fadeInUp', 100)),
        spacer(14),
        con({'width': u(440), 'width_mobile': u(100, '%')}, [
            W('form', {'form_name': 'Newsletter', 'form_fields': [
                {'_id': nid(), 'custom_id': 'email', 'field_type': 'email', 'field_label': 'Email',
                 'placeholder': 'your@email.com', 'required': 'true', 'width': '70', 'width_mobile': '100'}],
                'show_labels': '', 'input_size': 'md', 'button_text': 'Subscribe', 'button_width': '30',
                'button_width_mobile': '100', 'column_gap': u(0), 'row_gap': u(10),
                'button_background_color': C['wine'], 'button_text_color': '#FFFFFF',
                'button_background_hover_color': C['brown'], 'field_background_color': '#FFFFFF',
                'success_message': 'Thank you for joining us ✦',
                **typo('button_typography', family=SANS, size=10, weight=500, transform='uppercase', spacing=2.5),
                **typo('field_typography', family=SANS, size=13, weight=300)}, 'jw-form jw-nl', anim('fadeInUp', 200)),
        ]),
    ])

    def links(title, items):
        return col([
            heading(title, 'h4', C['cream'], family=SANS, size=9, weight=600, transform='uppercase', spacing=3),
            spacer(8),
            W('icon-list', {'icon_list': [{'_id': nid(), 'text': t, 'link': {'url': l}, 'selected_icon': {'value': '', 'library': ''}}
                                          for t, l in items],
                            'text_color': 'rgba(249,242,235,0.6)', 'text_color_hover': '#FFFFFF', 'space_between': u(10),
                            **typo('icon_typography', family=SANS, size=12.5, weight=300)}),
        ], 18, tablet=30, mobile=50)

    brand = col([
        W('image', {'image': {'id': IDS['img']['logo-light'], 'url': URLS.get(IDS['img']['logo-light'], '')}, 'image_size': 'full',
                    'align': 'left', 'width': u(230), 'width_mobile': u(190)}, extra={'_margin': box4(0, 0, 8, 0)}),
        text('Curated artisan gifts for corporate events, VIP experiences, employee recognition, incentive travel and destination programs. Orlando, Florida.',
             'rgba(249,242,235,0.6)', size=12.5, lh=1.85, extra={'_element_width': 'initial', '_element_custom_width': u(280)}),
        W('social-icons', {'social_icon_list': [
            {'_id': nid(), 'social_icon': {'value': 'fab fa-instagram', 'library': 'fa-brands'}, 'link': {'url': '#'}},
            {'_id': nid(), 'social_icon': {'value': 'fab fa-facebook-f', 'library': 'fa-brands'}, 'link': {'url': '#'}},
            {'_id': nid(), 'social_icon': {'value': 'fab fa-linkedin-in', 'library': 'fa-brands'}, 'link': {'url': '#'}}],
            'shape': 'circle', 'align': 'left', 'icon_color': 'custom', 'icon_primary_color': 'rgba(0,0,0,0)',
            'icon_secondary_color': C['cream'], 'icon_size': u(13), 'icon_padding': u(10, 'em') | {'size': .8},
            'border_border': 'solid', 'border_width': radius(1), 'border_color': 'rgba(255,255,255,0.2)',
            'hover_primary_color': C['lilac'], 'hover_secondary_color': C['wined'], 'hover_animation': 'grow'}),
    ], 40, tablet=100, mobile=100, s={'flex_gap': gap(10)})

    grid = row([brand,
                links('Boxes', [(b['t'].replace('The ', '').replace(' Gift Box', '').replace(' Box', ''), PRODUCT_URL[b['i']]) for b in BOXES]),
                links('Company', [('Our Story', '/our-story/'), ('Corporate Gifting', '/corporate/'), ('Customize a Box', '/customize/')]),
                links('Shop', [('Christmas Boxes', '/shop/'), ('Cart', '/cart/'), ('Request a Quote', '/corporate/#quote')])],
               48, {'flex_wrap_tablet': 'wrap', 'flex_wrap_mobile': 'wrap', 'flex_direction_mobile': 'row'}, stack=False)
    bottom = row([
        col([text('© 2026 Julia Wisteria · Orlando, FL', 'rgba(249,242,235,0.6)', size=11, lh=1.6)], 60),
        col([heading('Crafted with love. Inspired by family.', 'div', C['lilac'], 'right', family=SCRIPT, size=20, weight=400,
                     extra={'align_mobile': 'left'})], 40),
    ], s={'border_border': 'solid', 'border_width': box4(1, 0, 0, 0), 'border_color': 'rgba(255,255,255,0.1)',
          'padding': box4(28, 0, 0, 0)})
    foot = section({'background_background': 'classic', 'background_color': C['wined'], **pad(72, 52, 36, 52),
                    'flex_gap': gap(52)}, [grid, bottom])
    return [nl, foot]


# ════════════════════════════════════════════════════════════════════
def hero_bg(extra=None):
    d = {'background_background': 'classic', 'background_color': C['cream']}
    d.update(extra or {})
    return d


def box_tile(b, n, minh, minh_t, delay):
    popup_tag = '[elementor-tag id="jwqv%04d" name="popup" settings="%%7B%%22popup%%22%%3A%%22%d%%22%%7D"]' % (n, IDS['popup'][b['i']])
    return con({'html_tag': 'a', 'link': {'url': PRODUCT_URL[b['i']], 'is_external': '', 'nofollow': ''},
                '__dynamic__': {'link': popup_tag},
                'min_height': u(minh), 'min_height_tablet': u(minh_t), 'min_height_mobile': u(320),
                'flex_justify_content': 'space-between', 'background_background': 'classic', 'background_color': C['brown'],
                'border_radius': radius(30), **pad(22, 30, 28, 30), 'flex_grow': 1,
                **anim('zoomIn', delay, container=True)}, [
        image(IDS['img'][b['i']], cls='jw-bx-img', size='large'),
        heading('0%d' % (n + 1), 'div', '#FFFFFF', cls='jw-bx-n', family=SERIF, size=15, weight=400, spacing=3),
        con({'flex_gap': gap(4)}, [
            label(b['k'], 'rgba(255,255,255,0.85)', size=9.5, spacing=2.6),
            heading(b['t'], 'h3', '#FFFFFF', family=SERIF, size=38, weight=400, lh=1.05, m=28),
            heading('→ &nbsp;See what\'s inside', 'div', '#FFFFFF', cls='jw-bx-more', family=SANS, size=10, weight=500,
                    transform='uppercase', spacing=2.4, extra={'_margin': box4(10, 0, 0, 0)}),
        ]),
    ], cls='jw-bx')


def story_block(big_letter, eyebrow, h2, big, paras, btn=None):
    left = col([
        heading(big_letter, 'div', C['wine'], cls='jw-outline', extra=parallax(1.5),
                family=SERIF, size=240, weight=300, lh=.8, spacing=-6, t=170, m=120),
        script(eyebrow, extra=anim('fadeInUp', 0)),
        heading(h2, 'h2', C['brown'], cls='jw-split jw-em', family=SERIF, size=64, weight=300, lh=1.04, spacing=-1.2),
        image(IDS['img']['wisteria'], cls='', size='full', extra={**anim('fadeIn', 400, slow=True), 'width': u(140), 'align': 'left'}),
    ], 42, s={'sticky': 'top', 'sticky_on': ['desktop'], 'sticky_offset': 130, 'sticky_parent': 'yes',
              'flex_gap': gap(14)}, tablet=100)
    right_kids = [text(big, C['brown'], size=30, lh=1.35, cls='jw-big', family=SERIF, extra=anim())]
    for i, p in enumerate(paras):
        right_kids.append(text(p, size=17, lh=2, extra={**anim('fadeInUp', 0), '_element_width': 'initial',
                                                        '_element_custom_width': u(620)}))
    if btn: right_kids.append(btn)
    right = col(right_kids, 58, tablet=100, s={'flex_gap': gap(22), 'padding': box4(20, 0, 0, 0)})
    return [left, right]


def build_home():
    hero_left = col([
        heading('Christmas Season · Investor Concept · Orlando, FL', 'div', C['brown'], cls='jw-tag', extra=anim(),
                family=SANS, size=10, weight=500, transform='uppercase', spacing=2.4, lh=1.4),
        script('Julia Wisteria', size=38, extra=anim('fadeInUp', 100)),
        heading('Corporate Gifting, Crafted with <em>Meaning</em>', 'h1', C['brown'], cls='jw-split jw-shine',
                family=SERIF, size=104, weight=300, lh=.98, spacing=-2, t=72, m=48),
        text('Curated artisan gifts for corporate events, VIP experiences, employee recognition, incentive travel and destination programs.',
             extra={**anim('fadeInUp', 500), '_element_width': 'initial', '_element_custom_width': u(500),
                    '_element_custom_width_mobile': u(100, '%')}),
        row([button('Explore the boxes', '#boxes', solid=True), button('Our story', '/our-story/', icon=False)], 14,
            {'flex_wrap': 'wrap', 'flex_direction_mobile': 'row', **anim('fadeInUp', 650, container=True)}, stack=False),
    ], 52, tablet=100, s={'flex_gap': gap(18)})

    def card(key, cls, pos, w, h, ht, hm, delay, z):
        ex = {'_position': 'absolute', '_element_width': 'initial', '_element_custom_width': u(w, '%'), '_z_index': z,
              **anim('zoomIn', delay, slow=True), **tilt(3)}
        ex.update(pos)
        return image(IDS['img'][key], cls='jw-card ' + cls, extra=ex, h=h, ht=ht, hm=hm, r=26)

    stack = col([
        card('coffee-planning', 'jw-c1', {'_offset_orientation_h': 'end', '_offset_x_end': u(2, '%'), '_offset_y': u(0)},
             62, 410, 320, 250, 0, 1),
        card('unwind-recharge', 'jw-c2', {'_offset_x': u(0, '%'), '_offset_y': u(30, '%')}, 48, 270, 210, 170, 200, 2),
        card('light-up-your-day', 'jw-c3', {'_offset_orientation_h': 'end', '_offset_x_end': u(6, '%'),
                                             '_offset_orientation_v': 'end', '_offset_y_end': u(0)}, 44, 235, 180, 150, 400, 3),
        W('text-path', {'text': 'CRAFTED WITH LOVE · CURATED WITH PURPOSE · ', 'path': 'circle', 'align': 'center',
                        'text_color': C['lilacl'], 'word_spacing': u(0),
                        **typo('text_typography', family=SANS, size=9.5, weight=400, spacing=3.2)},
          'jw-badge', {'_position': 'absolute', '_offset_x': u(34, '%'), '_offset_orientation_v': 'end', '_offset_y_end': u(6, '%'),
                       '_element_width': 'initial', '_element_custom_width': u(128), '_element_custom_width_mobile': u(96),
                       '_z_index': 5, '_background_background': 'classic', '_background_color': C['wine'],
                       '_border_radius': radius(999), '_padding': box4(6, 6, 6, 6), **anim('zoomIn', 700)}),
        heading('<b>5</b>Christmas<br>boxes', 'div', C['cream'], 'center', cls='jw-badge-c',
                extra={'_position': 'absolute', '_offset_x': u(34, '%'), '_offset_orientation_v': 'end', '_offset_y_end': u(6, '%'),
                       '_element_width': 'initial', '_element_custom_width': u(128), '_element_custom_width_mobile': u(96),
                       '_z_index': 6, '_margin': box4(0, 0, 38, 0), '_margin_mobile': box4(0, 0, 26, 0), **anim('zoomIn', 700)},
                family=SERIF, size=15, weight=400, lh=1.2, m=12),
    ], 48, tablet=100, s={'min_height': u(620), 'min_height_tablet': u(480), 'min_height_mobile': u(400)}, cls='jw-stack')

    hero = section(hero_bg({'flex_direction': 'row', 'flex_align_items': 'center', 'flex_gap': gap(40),
                            'flex_direction_tablet': 'column', 'min_height': u(88, 'vh'), **pad(70, 52, 90, 52)}),
                   [hero_left, stack], cls='jw-hero jw-grain')

    mq_text = ''.join('<span>%s</span>' % t for t in ['Crafted with love', 'Curated with purpose', 'Inspired by family',
                                                       'Supporting local makers'] * 2)
    marquee = section({'content_width': 'full', 'background_background': 'classic', 'background_color': C['wined'],
                       'padding': box4(20, 0, 20, 0), 'overflow': 'hidden'}, [
        heading(mq_text, 'div', C['cream'], family=SERIF, size=28, weight=300, style='italic', m=22)], cls='jw-mq')

    occ = section({'flex_direction': 'row', 'flex_wrap': 'wrap', 'flex_justify_content': 'center', 'flex_gap': gap(12),
                   'flex_direction_mobile': 'row', **pad(64, 52, 0, 52)},
                  [chip(t, extra=anim('fadeInUp', i * 60)) for i, t in enumerate(
                      ['Corporate events', 'VIP experiences', 'Employee recognition', 'Incentive travel', 'Destination programs'])])

    story = section({'flex_direction': 'row', 'flex_gap': gap(90), 'flex_direction_tablet': 'column',
                     'flex_align_items': 'flex-start', '_element_id': 'story', **pad(130, 52, 130, 52)},
                    story_block('JW', 'Our Story', 'Born from love, family, and <em>a story worth telling.</em>',
                                '<p>Julia Wisteria was born from love, family, and the belief that <em>meaningful gifts should tell a story.</em></p>',
                                ['Julia is our grandmother — the woman who raised us, cared for us, and taught us the importance of love, patience, dedication, and giving from the heart. Her values became the inspiration behind everything we want this company to represent.',
                                 'The Wisteria flower symbolizes love, longevity, patience, and devotion — qualities that remind us of Julia and the legacy she created within our family. That is why Julia Wisteria felt like the perfect name.',
                                 'Our small company was created with a simple purpose: to turn gifting into something meaningful while supporting local makers, artisans, and small entrepreneurs.',
                                 'For us, a gift is more than an object. It is a way to say thank you, to celebrate, to connect, and to make someone feel remembered.'],
                                button('Read our full story', '/our-story/', extra=anim('fadeInUp', 0))))

    b = BOXES
    bento = con({'flex_gap': gap(22)}, [
        row([con({'width': u(58, '%'), 'width_tablet': u(100, '%')}, [box_tile(b[0], 0, 642, 520, 0)]),
             con({'width': u(42, '%'), 'width_tablet': u(100, '%'), 'flex_gap': gap(22), 'flex_direction_tablet': 'row',
                  'flex_direction_mobile': 'column'},
                 [box_tile(b[1], 1, 310, 360, 80), box_tile(b[2], 2, 310, 360, 160)])], 22,
            {'flex_direction_tablet': 'column'}),
        row([box_tile(b[3], 3, 470, 400, 0), box_tile(b[4], 4, 470, 400, 80)], 22),
    ])
    boxes = section({'background_background': 'gradient', 'background_color': C['cream'], 'background_color_b': '#F3E7E4',
                     'background_gradient_angle': u(180, 'deg'), '_element_id': 'boxes', **pad(120, 52, 130, 52),
                     'flex_gap': gap(10)}, [
        script('Christmas Season', align='center', size=28, extra=anim()),
        heading('Five boxes, thoughtfully curated', 'h2', C['brown'], 'center', 'jw-split', family=SERIF, size=72,
                weight=300, lh=1.05, spacing=-1.5),
        label('Corporate · Wellness · Tea · Desk · Rest — tap a box to see what\'s inside', align='center',
              extra=anim('fadeInUp', 200)),
        spacer(50), bento])

    feats_data = [('fas fa-gift', 'Luxury packaging', 'Every box arrives in elegant gift packaging, ready to impress.'),
                  ('fas fa-envelope-open-text', 'Personalized card', 'A welcome or message card makes each recipient feel remembered.'),
                  ('fas fa-certificate', 'Optional custom branding', 'Tailor the experience to represent your company and event.'),
                  ('far fa-heart', 'Local makers', 'Whenever possible, we choose locally made products from small businesses.')]
    feats = section({'flex_direction': 'row', 'flex_gap': gap(22), 'flex_wrap_tablet': 'wrap', **pad(110, 52, 110, 52)}, [
        con({'width': u(25, '%'), 'width_tablet': u(48, '%'), 'width_mobile': u(100, '%'), 'background_background': 'classic',
             'background_color': '#FFFFFF', 'border_border': 'solid', 'border_width': radius(1),
             'border_color': 'rgba(90,70,66,0.08)', 'border_radius': radius(26), 'padding': box4(34, 28, 34, 28),
             **anim('fadeInUp', i * 80, container=True)}, [
            W('icon-box', {'selected_icon': {'value': ic, 'library': 'fa-solid' if ic.startswith('fas') else 'fa-regular'},
                           'title_text': t, 'description_text': d, 'position': 'top', 'text_align': 'left',
                           'primary_color': C['wine'], 'icon_size': u(38), 'icon_space': u(22), 'title_color': C['brown'],
                           'description_color': C['muted'], 'hover_animation': 'float',
                           **typo('title_typography', family=SERIF, size=24, weight=400),
                           **typo('description_typography', family=SANS, size=12.5, weight=300, lh=1.85)})],
            cls='jw-lift jw-lilac-hover') for i, (ic, t, d) in enumerate(feats_data)])

    cta_inner = con({'background_background': 'gradient', 'background_color': '#8A3D4B',
                   'background_color_stop': u(0, '%'), 'background_color_b': '#2E1018', 'background_color_b_stop': u(100, '%'),
                   'background_gradient_type': 'radial', 'background_gradient_position': 'top left',
                   'border_radius': radius(44), 'flex_align_items': 'center', 'flex_gap': gap(14), **pad(110, 40, 110, 40),
                   **anim('zoomIn', 0, container=True)}, [
        script('Crafted with love. Curated with purpose.', C['lilac'], 'center', 32),
        heading('Inspired by family.', 'h2', C['cream'], 'center', 'jw-split', family=SERIF, size=80, weight=300, lh=1,
                spacing=-1.5),
        text('Planning a corporate event, VIP experience, recognition program or incentive trip this season? Tell us about it and we\'ll curate the perfect gift.',
             'rgba(249,242,235,0.72)', 'center', 14.5,
             extra={'_element_width': 'initial', '_element_custom_width': u(560), '_element_custom_width_mobile': u(100, '%')}),
        spacer(10),
        row([button('Request a custom quote', '/corporate/#quote', solid=True, light=True),
             button('Browse the boxes', '/shop/', light=True, icon=False)], 14,
            {'flex_justify_content': 'center', 'flex_wrap': 'wrap', 'flex_direction_mobile': 'row'}, stack=False),
    ], cls='jw-cta')
    cta = section({'_element_id': 'corporate', **pad(0, 52, 110, 52)}, [cta_inner])
    return [hero, marquee, occ, story, boxes, feats, cta]


# ════════════════════════════════════════════════════════════════════
def page_hero(eyebrow, h1, lead=None, crumb=None, buttons=None, bottom=70, breadcrumb_widget=False):
    kids = []
    if breadcrumb_widget:
        kids.append(W('woocommerce-breadcrumb', {'align': 'center', 'text_color': C['muted'], 'link_color': C['muted'],
                                                 **typo('text_typography', family=SANS, size=10, weight=400,
                                                        transform='uppercase', spacing=2)}, extra=anim()))
    elif crumb:
        kids.append(heading('<a href="/">Home</a> &nbsp;/&nbsp; ' + crumb, 'div', C['muted'], 'center', extra=anim(),
                            family=SANS, size=10, weight=400, transform='uppercase', spacing=2))
    kids.append(script(eyebrow, align='center', size=38, extra=anim('fadeInUp', 100)))
    kids.append(heading(h1, 'h1', C['brown'], 'center', 'jw-split jw-shine', family=SERIF, size=88, weight=300,
                        lh=1, spacing=-2, t=62, m=42,
                        extra={'_element_width': 'initial', '_element_custom_width': u(1000),
                               '_element_custom_width_tablet': u(100, '%')}))
    if lead:
        kids.append(text(lead, align='center', extra={**anim('fadeInUp', 400), '_element_width': 'initial',
                                                      '_element_custom_width': u(560),
                                                      '_element_custom_width_mobile': u(100, '%')}))
    if buttons:
        kids.append(row(buttons, 14, {'flex_justify_content': 'center', 'flex_wrap': 'wrap', 'flex_direction_mobile': 'row',
                                      'margin': box4(16, 0, 0, 0), **anim('fadeInUp', 550, container=True)}, stack=False))
    return section(hero_bg({'flex_align_items': 'center', 'flex_gap': gap(12), **pad(110, 52, bottom, 52)}), kids,
                   cls='jw-hero jw-grain')


def dark_cards(eyebrow, h2, intro, cards, num_size=56, cls_extra=''):
    head = [script(eyebrow, C['lilac'], extra=anim()),
            heading(h2, 'h2', C['cream'], cls='jw-split', family=SERIF, size=68, weight=300, lh=1.05, spacing=-1.2,
                    extra={'_element_width': 'initial', '_element_custom_width': u(760),
                           '_element_custom_width_tablet': u(100, '%')})]
    if intro:
        head.append(text(intro, 'rgba(249,242,235,0.65)', extra={**anim('fadeInUp', 200), '_element_width': 'initial',
                                                                  '_element_custom_width': u(760),
                                                                  '_element_custom_width_tablet': u(100, '%')}))
    grid = row([con({'width': u(100 / len(cards) - 2, '%'), 'width_tablet': u(48 if len(cards) == 4 else 100, '%'),
                     'width_mobile': u(100, '%'), 'background_background': 'classic',
                     'background_color': 'rgba(255,255,255,0.05)', 'border_border': 'solid', 'border_width': radius(1),
                     'border_color': 'rgba(255,255,255,0.1)', 'border_radius': radius(28), 'padding': box4(40, 30, 44, 30),
                     'flex_gap': gap(8), **anim('fadeInUp', i * 80, container=True)}, [
        heading(n, 'div', C['lilac'], family=SERIF, size=num_size, weight=300, style='italic', lh=1,
                extra={'_margin': box4(0, 0, 10, 0)}),
        heading(t, 'h3', C['cream'], family=SERIF, size=28, weight=400),
        text(d, 'rgba(249,242,235,0.62)', size=13, lh=1.85),
    ], cls='jw-lift jw-dark-hover') for i, (n, t, d) in enumerate(cards)], 22,
        {'flex_wrap_tablet': 'wrap', 'margin': box4(50, 0, 0, 0)})
    return section({'background_background': 'classic', 'background_color': C['wined'], 'flex_gap': gap(14),
                    **pad(120, 52, 120, 52)}, head + [grid])


def build_about():
    hero = page_hero('Our Story', 'Julia Wisteria was born from love, family, and <em>a gift that tells a story.</em>',
                     'Crafted with love. Curated with purpose. Inspired by family.', bottom=90)
    story = section({'flex_direction': 'row', 'flex_gap': gap(90), 'flex_direction_tablet': 'column',
                     'flex_align_items': 'flex-start', **pad(90, 52, 130, 52)},
                    story_block('J', 'Meet Julia', 'The woman who taught us <em>to give from the heart.</em>',
                                '<p>Julia is our grandmother — the woman who raised us, cared for us, and taught us the importance of love, patience, dedication, and giving from the heart.</p>',
                                ['Her values became the inspiration behind everything we want this company to represent.',
                                 'Our small company was created with a simple purpose: to turn gifting into something meaningful while supporting local makers, artisans, and small entrepreneurs.',
                                 'We carefully curate products made with love, creativity, and craftsmanship, bringing them together in beautiful gifts for companies, events, celebrations, and special moments. Whenever possible, we choose locally made products and collaborate with small businesses, giving their creations an opportunity to become part of someone else\'s story.']))
    symb = dark_cards('Why Wisteria', 'The flower that reminds us of Julia',
                      'The Wisteria flower symbolizes love, longevity, patience, and devotion — qualities that remind us of Julia and the legacy she created within our family. That is why Julia Wisteria felt like the perfect name.',
                      [('01', 'Love', 'Every gift begins with care for the person receiving it.'),
                       ('02', 'Longevity', 'The smallest gestures can leave the longest-lasting memories.'),
                       ('03', 'Patience', 'Thoughtful curation takes time, and we take it.'),
                       ('04', 'Devotion', 'To our family, to local makers, and to every story we help tell.')])
    purpose = section({'flex_direction': 'row', 'flex_gap': gap(90), 'flex_align_items': 'center',
                       'flex_direction_tablet': 'column', **pad(130, 52, 130, 52)}, [
        col([image(IDS['img']['teatime-delight'], cls='jw-frame', extra={**anim('fadeInLeft', 0, slow=True), **parallax(1)},
                   h=620, ht=520, hm=360, r=36)], 50, tablet=100),
        col([script('More than an object', extra=anim()),
             heading('A way to say thank you, to celebrate, to connect.', 'h2', C['brown'], cls='jw-split', family=SERIF,
                     size=64, weight=300, lh=1.04, spacing=-1.2),
             text('For us, a gift is more than an object. It is a way to say thank you, to celebrate, to connect, and to make someone feel remembered.',
                  size=16, lh=2, extra=anim('fadeInUp', 100)),
             text('Julia taught us that the smallest gestures, when made with love, can leave the longest-lasting memories.',
                  size=16, lh=2, extra=anim('fadeInUp', 200)),
             button('Discover the Christmas boxes', '/shop/', solid=True, extra=anim('fadeInUp', 300))],
            50, tablet=100, s={'flex_gap': gap(18)}),
    ])
    quote = section({'flex_align_items': 'center', **pad(120, 52, 60, 52)}, [
        heading('That is the heart of <em>Julia Wisteria.</em>', 'h2', C['brown'], 'center', 'jw-split jw-em-wine',
                family=SERIF, size=60, weight=300, lh=1.15, spacing=-1)])
    motto = section({'flex_direction': 'row', 'flex_wrap': 'wrap', 'flex_justify_content': 'center', 'flex_gap': gap(14),
                     'flex_direction_mobile': 'row', **pad(0, 52, 120, 52)},
                    [heading(t, 'div', C['wined'], 'center', 'jw-pill', anim('fadeInUp', i * 100), family=SERIF, size=36,
                             weight=300, style='italic', m=22)
                     for i, t in enumerate(['Crafted with love.', 'Curated with purpose.', 'Inspired by family.'])])
    return [hero, story, symb, purpose, quote, motto]


def form_field(cid, ftype, lbl, width='50', options=None, required=False, placeholder=None, **more):
    f = {'_id': nid(), 'custom_id': cid, 'field_type': ftype, 'field_label': lbl,
         'placeholder': placeholder if placeholder is not None else lbl, 'width': width, 'width_mobile': '100',
         'required': 'true' if required else ''}
    if options: f['field_options'] = '\n'.join(options)
    f.update(more)
    return f


def form_style():
    return {'label_spacing': u(8), 'label_color': C['brown'], 'field_text_color': C['brown'],
            'field_background_color': '#FFFFFF', 'field_border_color': 'rgba(90,70,66,0.18)',
            'field_border_radius': radius(16), 'column_gap': u(20), 'row_gap': u(20),
            'button_background_color': C['wine'], 'button_text_color': '#FFFFFF',
            'button_background_hover_color': C['brown'], 'button_border_radius': radius(999),
            'button_text_padding': box4(17, 34, 17, 34),
            'previous_button_background_color': '#FFFFFF', 'previous_button_text_color': C['brown'],
            **typo('label_typography', family=SANS, size=10, weight=500, transform='uppercase', spacing=2.2),
            **typo('field_typography', family=SANS, size=14, weight=300),
            **typo('button_typography', family=SANS, size=10.5, weight=500, transform='uppercase', spacing=2.6)}


BOX_NAMES = [b['t'] for b in BOXES]


def build_corporate():
    hero = page_hero('For businesses', 'Corporate gifting, crafted with <em>meaning</em>',
                     'Curated artisan gifts for corporate events, VIP experiences, employee recognition, incentive travel and destination programs.',
                     'Corporate', [button('Request a quote', '#quote', solid=True), button('See the boxes', '/shop/', icon=False)])
    occ = section({'flex_direction': 'row', 'flex_gap': gap(18), 'flex_wrap_tablet': 'wrap', **pad(60, 52, 100, 52)}, [
        con({'width': u(20, '%'), 'width_tablet': u(48, '%'), 'width_mobile': u(100, '%'), 'background_background': 'classic',
             'background_color': '#FFFFFF', 'border_border': 'solid', 'border_width': radius(1),
             'border_color': 'rgba(90,70,66,0.08)', 'border_radius': radius(26), 'padding': box4(34, 26, 34, 26),
             'flex_gap': gap(10), **anim('fadeInUp', i * 80, container=True)}, [
            heading('0%d' % (i + 1), 'div', C['lilac'], family=SERIF, size=44, weight=300, style='italic', lh=1),
            heading(t, 'h3', C['brown'], family=SERIF, size=23, weight=400, lh=1.15)], cls='jw-lift jw-lilac-hover')
        for i, t in enumerate(['Corporate events', 'VIP experiences', 'Employee recognition', 'Incentive travel',
                               'Destination programs'])])
    proc = dark_cards('Simple process', 'Three steps to a gift that tells a story', None, [
        ('01', 'Consult', 'Tell us your vision, occasion and group size. We help you choose the right box and the right personal touches.'),
        ('02', 'Curate', 'We assemble each box with products made with love, creativity and craftsmanship — locally made whenever possible.'),
        ('03', 'Deliver', 'Luxury packaging, a personalized card and optional custom branding, ready to make every recipient feel remembered.')],
        num_size=60)
    form = W('form', {'form_name': 'Corporate Quote', 'form_fields': [
        form_field('boxes', 'checkbox', 'Boxes you are interested in', '100', BOX_NAMES, inline_list='elementor-subgroup-inline'),
        form_field('first_name', 'text', 'First name', required=True, placeholder='Julia'),
        form_field('last_name', 'text', 'Last name', required=True, placeholder='Smith'),
        form_field('company', 'text', 'Company', '100', placeholder='Your Company, LLC'),
        form_field('email', 'email', 'Email', required=True, placeholder='julia@yourcompany.com'),
        form_field('phone', 'tel', 'Phone', placeholder='(407) 000-0000'),
        form_field('occasion', 'select', 'Event / occasion', options=['Corporate event', 'VIP experience', 'Employee recognition',
                                                                      'Incentive travel', 'Destination program', 'Other']),
        form_field('quantity', 'number', 'Number of boxes', placeholder='e.g. 50'),
        form_field('date', 'date', 'Needed by', '100', placeholder=''),
        form_field('message', 'textarea', 'Message', '100', placeholder='Tell us about your brand, timeline or special requests…',
                   rows=5)],
        'button_text': 'Send request', 'button_width': '100', 'button_align': 'start',
        'selected_button_icon': {'value': 'fas fa-arrow-right', 'library': 'fa-solid'}, 'button_icon_align': 'right',
        'submit_actions': ['email'], 'email_subject': 'New corporate quote request — Julia Wisteria',
        'success_message': 'Thank you! We received your request and will get back to you very soon.',
        **form_style()}, 'jw-form', anim('fadeInUp', 200))
    quote = section({'flex_align_items': 'center', '_element_id': 'quote', 'flex_gap': gap(10), **pad(120, 24, 120, 24)}, [
        script("Let's create something beautiful", align='center', extra=anim()),
        heading('Request a custom quote', 'h2', C['brown'], 'center', 'jw-split', family=SERIF, size=56, weight=300, lh=1.05),
        label("Tell us about your gifting vision and we'll be in touch", align='center', extra=anim('fadeInUp', 100)),
        spacer(30),
        con({'width': u(900), 'width_tablet': u(100, '%')}, [form])])
    return [hero, occ, proc, quote]


def build_customize():
    hero = page_hero('Made for your team', 'Customize your gift',
                     'Choose a box, add your personal touches and we will prepare a proposal for your team.',
                     'Customize', bottom=40)
    form = W('form', {'form_name': 'Customize your gift', 'form_fields': [
        form_field('step1', 'step', 'Choose a box', '100', previous_button='', next_button='Continue'),
        form_field('box', 'radio', 'Which box fits the moment?', '100', BOX_NAMES, required=True),
        form_field('step2', 'step', 'Personalize', '100', previous_button='Back', next_button='Continue'),
        form_field('quantity', 'number', 'Number of boxes', placeholder='25', required=True, field_min=1),
        form_field('date', 'date', 'Needed by', placeholder=''),
        form_field('card', 'textarea', 'Personalized card message', '100', placeholder='Thank you for a wonderful year…', rows=3),
        form_field('branding', 'checkbox', 'Branding', '100', ['Add optional custom branding (logo & colors)']),
        form_field('step3', 'step', 'Your details', '100', previous_button='Back', next_button=''),
        form_field('name', 'text', 'Full name', required=True),
        form_field('company', 'text', 'Company'),
        form_field('email', 'email', 'Email', required=True),
        form_field('phone', 'tel', 'Phone')],
        'step_type': 'progress_bar', 'button_text': 'Send request', 'button_width': '100',
        'submit_actions': ['email'], 'email_subject': 'New custom box request — Julia Wisteria',
        'success_message': 'Thank you! We will prepare your proposal and get back to you very soon.',
        **form_style()}, 'jw-form', anim('fadeInUp', 300))
    body = section({'flex_align_items': 'center', **pad(40, 24, 120, 24)}, [con({'width': u(860), 'width_tablet': u(100, '%')}, [form])])
    thumbs = section({'flex_direction': 'row', 'flex_gap': gap(18), 'flex_wrap_mobile': 'wrap', 'flex_direction_mobile': 'row',
                      **pad(0, 52, 110, 52)}, [
        con({'width': u(20, '%'), 'width_mobile': u(47, '%'), 'flex_gap': gap(10), **anim('zoomIn', i * 70, container=True)}, [
            image(IDS['img'][b['i']], extra={'link_to': 'custom', 'link': {'url': PRODUCT_URL[b['i']]}, **tilt(3)}, h=230, ht=170,
                  hm=150, r=22),
            heading(b['t'], 'div', C['brown'], 'center', family=SERIF, size=18, weight=400, lh=1.15)])
        for i, b in enumerate(BOXES)])
    return [hero, body, thumbs]


def build_shop_archive():
    hero = page_hero('Christmas Season', 'Five boxes, thoughtfully curated',
                     'Corporate gifts for events, VIP experiences, employee recognition, incentive travel and destination programs.',
                     bottom=60, breadcrumb_widget=True)
    chips = section({'flex_direction': 'row', 'flex_wrap': 'wrap', 'flex_justify_content': 'center', 'flex_gap': gap(10),
                     'flex_direction_mobile': 'row', **pad(46, 52, 10, 52)},
                    [chip(t, url, i == 0, anim('fadeInUp', i * 60)) for i, (t, url) in enumerate(
                        [('All', '/shop/'), ('Corporate', '/product-category/corporate/'), ('Wellness', '/product-category/wellness/'),
                         ('Tea', '/product-category/tea/'), ('Desk', '/product-category/desk/'), ('Rest', '/product-category/rest/')])])
    grid = section({**pad(40, 52, 130, 52)}, [
        W('wc-archive-products', {'columns': 3, 'columns_tablet': 2, 'columns_mobile': 1, 'rows': 4, 'paginate': 'yes',
                                  'allow_order': '', 'show_result_count': '', 'column_gap': u(34), 'row_gap': u(50),
                                  'align': 'left', 'title_color': C['brown'], 'price_color': C['wine'],
                                  'button_text_color': '#FFFFFF', 'button_background_color': C['wine'],
                                  'button_hover_background_color': C['brown'], 'button_hover_color': '#FFFFFF',
                                  'button_border_radius': radius(999), 'button_text_padding': box4(13, 24, 13, 24),
                                  'button_spacing': u(14),
                                  **typo('title_typography', family=SERIF, size=30, weight=400, lh=1.08),
                                  **typo('price_typography', family=SERIF, size=20, weight=500),
                                  **typo('button_typography', family=SANS, size=9.5, weight=500, transform='uppercase', spacing=2.6)},
          'jw-shop', anim('fadeInUp', 200))])
    return [hero, chips, grid]


def build_single_product():
    left = col([W('woocommerce-product-images', {'sale_flash': ''}, 'jw-pdp-img', anim('zoomIn', 0, slow=True))], 52, tablet=100,
               s={'sticky': 'top', 'sticky_on': ['desktop'], 'sticky_offset': 110, 'sticky_parent': 'yes'})
    right = col([
        script('Christmas Season', extra=anim()),
        W('woocommerce-product-title', {'title_color': C['brown'], 'header_size': 'h1', '__dynamic__': {'title': '[elementor-tag id="jwpt0001" name="woocommerce-product-title-tag" settings="%7B%7D"]'},
                                        **typo('typography', family=SERIF, size=66, weight=300, lh=1.02, spacing=-1.2, t=52, m=38)},
          'jw-split'),
        W('woocommerce-product-price', {'price_color': C['wine'], **typo('typography', family=SERIF, size=30, weight=500)},
          extra=anim('fadeInUp', 200)),
        W('woocommerce-product-short-description', {'text_color': C['brownl'],
                                                     **typo('text_typography', family=SANS, size=15, weight=300, lh=1.95)},
          extra=anim('fadeInUp', 250)),
        con({'background_background': 'classic', 'background_color': C['lilacl'], 'border_radius': radius(28),
             'padding': box4(30, 30, 30, 30), **anim('fadeInUp', 300, container=True)}, [
            W('woocommerce-product-add-to-cart', {'show_quantity': 'yes', 'button_text_color': '#FFFFFF',
                                                  'button_bg_color': C['wine'], 'button_hover_bg_color': C['brown'],
                                                  'button_border_radius': radius(999), 'button_padding': box4(17, 34, 17, 34),
                                                  **typo('button_typography', family=SANS, size=10.5, weight=500,
                                                         transform='uppercase', spacing=2.6)}, 'jw-atc')]),
        W('woocommerce-product-content', {'text_color': C['brownl'],
                                          **typo('typography', family=SANS, size=15, weight=300, lh=1.95)},
          'jw-desc', anim('fadeInUp', 0)),
    ], 48, tablet=100, s={'flex_gap': gap(18)})
    main = section({'flex_gap': gap(30), **pad(34, 52, 100, 52)}, [
        W('woocommerce-breadcrumb', {'text_color': C['muted'], 'link_color': C['muted'],
                                     **typo('text_typography', family=SANS, size=10, weight=400, transform='uppercase', spacing=2)}),
        row([left, right], 80, {'flex_direction_tablet': 'column'})])
    related = section({**pad(0, 52, 120, 52), 'flex_gap': gap(10)}, [
        heading('You may also love', 'h2', C['brown'], cls='jw-split', family=SERIF, size=56, weight=300, spacing=-1),
        W('woocommerce-product-related', {'posts_per_page': 4, 'columns': 4, 'columns_tablet': 2, 'columns_mobile': 2,
                                          'orderby': 'menu_order', 'title_color': C['brown'], 'price_color': C['wine'],
                                          'button_text_color': '#FFFFFF', 'button_background_color': C['wine'],
                                          'button_border_radius': radius(999), 'heading_show': '',
                                          **typo('title_typography', family=SERIF, size=22, weight=400)},
          'jw-related', anim('fadeInUp', 100))])
    return [main, related]


def build_wc_page(eyebrow, title, widget, settings):
    hero = page_hero(eyebrow, title, crumb=title, bottom=30)
    body = section({**pad(40, 52, 120, 52)}, [W(widget, settings, 'jw-wc', anim('fadeInUp', 100))])
    return [hero, body]



# ════════════════════════════════════════════════════════════════════
# QUICK VIEW (Popups de Elementor Pro, uno por caja)
def build_quickview(b):
    img = col([image(IDS['img'][b['i']], cls='jw-qv-img', size='large', h=640, ht=520, hm=260)], 50, tablet=50, mobile=100,
              s={'flex_justify_content': 'center'})
    body = col([
        script(b['k'], size=28, cls='jw-qv-in'),
        heading(b['t'], 'h3', C['brown'], cls='jw-qv-in', family=SERIF, size=36, weight=300, lh=1.08, m=28),
        text(b['d'], size=13.5, lh=1.9, cls='jw-qv-in'),
        label('Includes', C['brown'], size=9.5, spacing=3, cls='jw-qv-in', extra={'_margin': box4(8, 0, 0, 0)}),
        W('icon-list', {'icon_list': [{'_id': nid(), 'text': t, 'selected_icon': {'value': 'fas fa-circle', 'library': 'fa-solid'}}
                                      for t in b['inc']],
                        'icon_color': C['lilac'], 'icon_size': u(6), 'text_color': C['brownl'], 'space_between': u(10),
                        'text_indent': u(10), **typo('icon_typography', family=SANS, size=12.5, weight=300, lh=1.5)},
          'jw-qv-in jw-qv-list'),
        heading(b['q'], 'div', C['wine'], cls='jw-qv-in', family=SERIF, size=21, weight=400, style='italic',
                extra={'_margin': box4(6, 0, 10, 0)}),
        con({'flex_direction': 'row', 'flex_gap': gap(12), 'flex_wrap': 'wrap'}, [
            button('View & add to cart', PRODUCT_URL[b['i']], solid=True),
            button('Request a quote', '/corporate/#quote', icon=False)], cls='jw-qv-in'),
    ], 50, tablet=50, mobile=100, s={'flex_gap': gap(12), 'padding': box4(46, 44, 46, 44),
                                     'padding_mobile': box4(30, 24, 34, 24), 'flex_justify_content': 'center'})
    return [con({'flex_direction': 'row', 'flex_direction_mobile': 'column', 'flex_gap': gap(0),
                 'flex_align_items': 'stretch'}, [img, body], inner=False, cls='jw-qv')]


def quickview_settings():
    return {'width': u(1020), 'width_tablet': u(92, 'vw'), 'width_mobile': u(92, 'vw'), 'height_type': 'auto',
            'horizontal_position': 'center', 'vertical_position': 'center',
            'overlay': 'yes', 'overlay_background_background': 'classic', 'overlay_background_color': 'rgba(40,20,24,0.55)',
            'background_background': 'classic', 'background_color': C['cream'], 'border_radius': radius(30),
            'close_button': 'yes', 'close_button_position': 'inside', 'close_button_vertical': u(16),
            'close_button_horizontal': u(16), 'close_button_color': C['brown'], 'close_button_background_color': '#FFFFFF',
            'close_button_hover_color': C['wine'], 'icon_size': u(16),
            'entrance_animation': 'fadeIn', 'entrance_animation_duration': u(0.5), 'exit_animation': 'fadeIn',
            'prevent_scroll': 'yes', 'avoid_multiple_popups': 'yes', 'classes': 'jw-qv-popup',
            'padding': box4(0, 0, 0, 0)}


TARGETS = {
    'header': (79, build_header), 'footer': (76, build_footer), 'home': (45, build_home), 'about': (46, build_about),
    'corporate': (47, build_corporate), 'customize': (48, build_customize), 'shop-archive': (85, build_shop_archive),
    'single-product': (88, build_single_product),
    'cart': (7, lambda: build_wc_page('Your selection', 'Cart', 'woocommerce-cart', {})),
    'checkout': (8, lambda: build_wc_page('Almost there', 'Checkout', 'woocommerce-checkout-page', {})),
}

if __name__ == '__main__':
    manifest = {}
    for b in BOXES:
        TARGETS['quickview-' + b['i']] = (IDS['popup'][b['i']], (lambda b=b: build_quickview(b)))
        json.dump(quickview_settings(), open(os.path.join(OUT, 'quickview-%s.settings.json' % b['i']), 'w'))
    for name, (pid, fn) in TARGETS.items():
        data = fn()
        path = os.path.join(OUT, name + '.json')
        json.dump(data, open(path, 'w'), ensure_ascii=False)
        manifest[name] = pid
    json.dump(manifest, open(os.path.join(OUT, 'manifest.json'), 'w'))
    print('OK', manifest)
