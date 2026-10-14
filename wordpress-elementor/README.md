# Julia Wisteria — Kit de migración a WordPress + Elementor + WooCommerce

> **Actualización (Christmas Season, oct. 2026):** el diseño vigente está en [`christmas/`](christmas/README.md). Este kit (`templates/`, `generate_templates.py`, `woocommerce/productos.csv`) corresponde al diseño anterior y queda solo como referencia.


Este kit convierte el diseño HTML estático en un sitio WordPress montado **100 % con widgets nativos de Elementor** (sin bloques de HTML personalizado).

## Contenido del kit

```
wordpress-elementor/
├── templates/                    # Plantillas JSON importables en Elementor
│   ├── header-theme-builder.json          (Theme Builder → Header)
│   ├── footer-theme-builder.json          (Theme Builder → Footer)
│   ├── home-page.json                     (página Inicio)
│   ├── about-page.json                    (página Our Story)
│   ├── corporate-page.json                (página Corporate)
│   ├── shop-archive-theme-builder.json    (Theme Builder → Product Archive: Shop All)
│   ├── single-product-theme-builder.json  (Theme Builder → Single Product)
│   └── build-your-box-page.json           (página Build Your Box)
├── woocommerce/
│   └── productos.csv             # 6 productos importables (1 variable + 5 simples)
├── assets/                       # Imágenes SVG extraídas del diseño original
└── generate_templates.py         # Script que genera los JSON (por si quieres regenerarlos)
```

---

## 1. Requisitos (plugins)

| Plugin | Obligatorio | Para qué |
|---|---|---|
| **Elementor** (gratis) | Sí | Constructor base |
| **Elementor Pro** | Sí | Theme Builder (header/footer), widgets WooCommerce, widget Form (newsletter y cotización corporate), Price Table, Nav Menu |
| **WooCommerce** | Sí | Tienda, carrito, checkout, productos |
| **Safe SVG** | Recomendado | WordPress bloquea la subida de SVG por defecto; este plugin la habilita de forma segura |
| **Hello Elementor** (tema) | Recomendado | Tema en blanco ideal para construir todo con Elementor |

> Los widgets usados de Pro son: `nav-menu`, `search-form`, `woocommerce-menu-cart`, `woocommerce-products`, `wc-categories`, `form`, `price-table`. Todo lo demás es Elementor gratuito (heading, text-editor, button, icon-box, icon-list, testimonial, counter, star-rating, social-icons, image, spacer).

---

## 2. Ajustes globales del sitio (Site Settings)

Abre cualquier página con Elementor → menú hamburguesa → **Site Settings** y configura:

### Colores globales

| Nombre | Hex | Uso |
|---|---|---|
| Primary / Brown | `#5A4642` | Textos, fondos oscuros, botones |
| Secondary / Rose | `#B88889` | Acentos, hovers, script |
| Accent / Sage | `#C1C099` | Detalles, estrellas, etiquetas |
| Cream | `#F9F2EB` | Fondo claro principal |
| Cream Dark | `#F0E6D9` | Fondo de footer y secciones alternas |
| Rose Light | `#D4B4B5` | Acentos suaves |
| Muted | `#8B7B78` | Texto secundario / párrafos |

### Tipografías globales (Google Fonts, Elementor las carga solo)

| Rol | Fuente | Pesos |
|---|---|---|
| Títulos (H1–H4) | **Cormorant Garamond** | 300 / 400 / 500 / 600 |
| Acentos script ("Welcome to", "Most Loved"…) | **Sacramento** | 400 |
| Cuerpo, botones, menú | **Jost** | 300 / 400 / 500 |

### Layout
- Anchura de contenido (Content Width): **1440 px**
- Espacio entre widgets por defecto: 16–20 px

---

## 3. Orden de montaje

### Paso 1 — Subir las imágenes
1. Instala y activa **Safe SVG**.
2. Sube todo el contenido de `assets/` a **Medios**. Son las ilustraciones del diseño original (hero, colecciones, productos, destacado).

### Paso 2 — Crear categorías de producto
En **Productos → Categorías** crea: `For Her`, `Corporate`, `Baby`, `Seasonal`, `Custom`, `Wellness`.
Asigna a cada categoría su imagen (`collection-*.svg`) — el widget **Product Categories** de la home las muestra automáticamente.

### Paso 3 — Importar productos
**Productos → Todos los productos → Importar** → selecciona `woocommerce/productos.csv`.
- The Romance Box es **producto variable** con atributo `Size` (Standard $89 / Deluxe $119 / Grand $149), igual que el selector de la página de producto original.
- Si las imágenes ya están en Medios con el mismo nombre de archivo, el importador las asociará; si no, asígnalas a mano.

### Paso 4 — Importar plantillas
**Plantillas → Plantillas guardadas → Importar plantillas** → sube los 5 JSON de `templates/`.

### Paso 5 — Header y Footer (Theme Builder)
1. **Plantillas → Theme Builder → Header** → verás "JW – Header" importado. Edítalo y:
   - En el widget **Nav Menu**, asigna el menú principal (créalo antes en Apariencia → Menús con: Shop All, Curated Boxes, Build Your Box, Corporate, Our Story).
   - Publica con condición **Todo el sitio**.
2. Igual con **Footer** ("JW – Footer") → condición **Todo el sitio**.

### Paso 6 — Páginas
Crea las páginas y edítalas con Elementor; en cada una inserta su plantilla desde la carpeta (icono 📁 → Mis plantillas):

| Página WP | Plantilla | Slug sugerido |
|---|---|---|
| Inicio | JW – Home | `/` (Ajustes → Lectura → página estática) |
| Our Story | JW – Our Story | `/our-story/` |
| Corporate | JW – Corporate | `/corporate/` |
| Build Your Box | JW – Build Your Box | `/build-your-box/` |

En todas: Atributos de página → plantilla **Elementor Full Width** (u oculta el título desde Page Settings, ya viene marcado en el JSON).

### Paso 7 — Retoques tras importar
- **Home → sección destacada (The Romance Box):** el widget Imagen de la izquierda está vacío a propósito → asígnale `featured-romance-box.svg`.
- **Home → colecciones:** el widget Product Categories mostrará las categorías con imagen del Paso 2.
- **Formularios (newsletter y cotización):** configura en cada widget Form la acción (Email / Mailchimp / etc.) y el destinatario.

---

## 4. Páginas de tienda (Shop, Producto, Carrito)

Shop y Producto NO van como plantillas de página: las gestiona WooCommerce vía **Theme Builder** y ya vienen diseñadas en el kit.

### Shop / archivo de productos (`shop.html`) — plantilla incluida
Importa `shop-archive-theme-builder.json`. Al importarla aparece en **Theme Builder → Product Archive** como "JW – Shop All". Edítala y publícala con condición **All Product Archives** (así aplica también a las categorías). Incluye:
- Breadcrumb + **Archive Title** (Cormorant 48/300) sobre fondo cream.
- Fila de **filtros tipo píldora** (All / For Her / For Him / Corporate / Baby / Seasonal / Custom) que enlazan a cada archivo de categoría. ⚠ La categoría *For Him* no está en el CSV: créala cuando tengas productos masculinos o borra ese botón.
- Rejilla **Archive Products** (3 columnas, con ordenación "Sort by" y contador de resultados nativos de Woo). El "Load More" original se sustituye por paginación.

### Página de producto (`product.html`) — plantilla incluida
Importa `single-product-theme-builder.json` → **Theme Builder → Single Product** → "JW – Single Product" → publica con condición **All Products**. Estructura:
- Breadcrumb arriba.
- 2 columnas: **Product Images** sobre degradado rosado · script "Handcrafted in Orlando" + **Product Title** (Cormorant 44/300) + **Product Rating** (estrellas sage) + **Product Price** (Cormorant 30) + **Short Description** + **Add To Cart** con cantidad (el selector Standard/Deluxe/Grand sale solo en Romance Box por ser variable) + lista de beneficios de envío.
- **Product Data Tabs** (el contenido "What's Inside / Personalization" se escribe en la descripción de cada producto).
- Sección "You May Also Love" con **Related Products** (4 columnas) sobre fondo cream.

### Carrito y checkout (`cart.html`)
- Páginas Cart/Checkout que crea WooCommerce + widgets **Cart** y **Checkout** de Elementor Pro (se estilizan con los colores globales: fondos cream, botones brown→rose).
- El campo "Promo Code" y el resumen de pedido vienen incluidos en el widget Cart.

---

## 5. Build Your Box (`build.html`) — plantilla incluida

Importa `build-your-box-page.json` y úsala en la página `/build-your-box/`. Replica el diseño con widgets nativos:

1. **Hero** + indicador de los 4 pasos (Choose Size · Select Items · Personalize · Review).
2. **Paso 1 — tamaños:** 3 Price Tables: Petite $55 (3 items) · Classic $85 (5 items, cinta "Most Loved") · Luxe $145 (8 items).
3. **Paso 2 — catálogo:** los 12 items del configurador original como tarjetas icon-box con categoría y precio (Soy Candle +$18, Botanical Tea Set +$22, Artisan Chocolates +$24, Silk Eye Mask +$28, Rose Bath Salts +$20, Honey & Fig Jam +$16, Cashmere Hand Cream +$26, Dried Floral Bunch +$30, Linen Sachet +$14, Artisan Soap Bar +$16, Gold Pen +$22, Truffle Collection +$32).
4. **Pasos 3 y 4 — formulario:** widget Form con todos los campos del original (tamaño, items, destinatario, ocasión, mensaje manuscrito, color de cinta Blush/Ivory/Sage/Chocolate, envoltura Standard/Premium +$5/Luxury +$12). El pedido llega por email y se confirma manualmente.

La interactividad en vivo (sumar items al total y añadir al carrito directo) no existe como widget nativo. Cuando quieras automatizarlo:
- **WPC Composite Products** (gratis/premium) — producto compuesto con pasos de selección; sustituye la sección del formulario y conserva el resto de la página.
- **YITH Composite Products** o **Advanced Product Fields for WooCommerce** como alternativas.

---

## 6. Detalles que difieren del HTML original (y por qué)

- **Barra "trust" animada (marquee):** Elementor no tiene marquee nativo; quedó como texto centrado estático. Si quieres la animación, el addon gratuito "Ele Custom Skin" o "Premium Addons" traen widget marquee.
- **Ilustraciones SVG inline:** ahora son archivos en `assets/` que se usan como imágenes normales (de ahí el plugin Safe SVG). Cuando tengas fotografía real de producto, solo reemplazas las imágenes.
- **Banner de anuncio superior:** va incluido dentro de la plantilla del Header.
- **Botón "Load More" del shop:** WooCommerce usa paginación; un scroll infinito requiere addon.
- **Precio "From $75.00" del Bespoke:** WooCommerce mostrará el precio base; el "From" aparece automáticamente si lo conviertes en variable o compuesto.

---

## 7. Instalación local actual (con Pro Elements activo)

El WordPress local (`wp-local/`, http://localhost:8081) está montado con los **widgets Pro nativos** funcionando, gracias a **Pro Elements** (alternativa open-source compatible con Elementor Pro). Todo lo que en su día se resolvió con puentes gratuitos volvió a su widget Pro original:

| Sección | Widget Pro nativo en uso |
|---|---|
| Header / Footer | Theme Builder (`JW – Header`, `JW – Footer`) con condición *Entire Site*. El header es **sticky**: la barra de navegación se ancla arriba al hacer scroll (el banner de anuncio scrollea fuera), con sombra suave al fijarse |
| Navegación | **Nav Menu** (menú `principal`, con burger en tablet/móvil) |
| Mini-carrito | **Menu Cart** (subtotal "$0.00" oculto; icono de bolsa en círculo, badge de cantidad en rose) |
| Búsqueda | **Search Form** (lupa en círculo limpio, sin fondo gris) |
| Grids de producto | **Products** (home) y **Archive Products** (shop) |
| Colecciones | **Product Categories** (4 categorías fijadas: For Her, Corporate, Seasonal, Custom) |
| Formularios | **Form** de Elementor (newsletter, cotización corporate, build) |
| Planes Corporate | Cada botón "Get Started" lleva al formulario de cotización (ancla `#quote`) y pre-selecciona el plan en el campo "Plan of Interest". Lo gestiona el mu-plugin `jw-corporate-plan.php` (links `?plan=X#quote` + scroll JS). El CSS de marca fuerza `scroll-behavior:auto` porque el `smooth` del tema bloquea el scroll programático |
| Tablas de precio | **Price Table** |
| Shop All | Theme Builder *Product Archive* (`JW – Shop All`); la página Woo nativa quedó en `/products/`. El título usa el shortcode `[jw_archive_title]` (mu-plugin `jw-archive-title.php`) que muestra el nombre de la categoría — el widget *Archive Title* de Pro no resuelve el contexto en archivos de WooCommerce |
| Ficha de producto | Theme Builder *Single Product* (`JW – Single Product`), condición *All Products* |

Los plugins puente (Header & Footer Elementor y Contact Form 7) quedaron desactivados.

### Responsive

Las plantillas se regeneraron con escalado responsive automático (ver `generate_templates.py`):
- **Tipografía**: cada titular ≥18px tiene tamaños tablet/móvil (ej. hero H1 68→56→39px).
- **Columnas**: las filas de 2 columnas apilan en móvil; las rejillas de 3–4 (pilares, valores, items, paquetes, stats) envuelven a 2 o 1 columna.
- **Padding**: los rellenos grandes se reducen ~25 % en tablet y ~40 % en móvil.
- **Grids Woo**: 3 col → 2 en tablet → 2 en móvil; categorías 4 → 2 → 2.
- Breakpoint principal en 768px, verificado en el render.

### Rendimiento

- **Experimentos de Elementor** activos: optimized assets/CSS loading, font-icon SVG, lazy-load, DOM optimization.
- **CSS en archivo externo** (cacheable) en vez de inline.
- **mu-plugin** `jw-performance.php`: limpia el `<head>` (emojis, oEmbed, wlwmanifest, generator, jQuery Migrate), difiere scripts no críticos, limita los assets y fragmentos de carrito de WooCommerce a las páginas de tienda, fuerza lazy-load y `font-display:swap`.
  - ⚠ `jquery-core` **no** se difiere a propósito: las librerías de Elementor Pro (sticky del header, smartmenus, jquery-ui) lo usan de forma síncrona y diferirlo rompe el header anclado y el menú desplegable.
- En el servidor de desarrollo (PHP `-S`, monohilo, sin opcache) la home tarda ~0,45s; en producción con opcache + HTTP/2 estas optimizaciones rinden bastante más.

### Arrancar / detener el servidor local

```bash
./wp-local/start.sh          # arranca en http://localhost:8081
pkill -f "php.*-S localhost:8081"   # detener
```

> Si más adelante usas Elementor Pro oficial en lugar de Pro Elements, los JSON de `templates/` son la versión canónica e importan igual.

## 8. Páginas legales (requisitos de plataformas de pago)

Creadas y enlazadas en el footer; listas para Stripe/PayPal. Editar los datos de
contacto/negocio en su contenido y en `wp-content/mu-plugins/jw-seo.php`.

| Página | URL | Asignada en |
|---|---|---|
| Privacy Policy | `/privacy-policy/` | WP → Ajustes de privacidad |
| Terms of Service | `/terms-of-service/` | WooCommerce → Términos del checkout |
| Refund & Returns | `/refund-returns/` | Footer |
| Shipping & Delivery | `/shipping-policy/` | Footer |
| Cookie Policy | `/cookie-policy/` | Footer / Privacy |
| Contact Us | `/contact/` | Footer |

El estilo de lectura está en CSS adicional (marcador `LEGAL PAGES`), con el wrapper
`.jw-legal`. El checkout exige aceptar los Términos (checkbox activado).

## 9. SEO

Todo gestionado por el mu-plugin `wp-content/mu-plugins/jw-seo.php` (sin plugins pesados):

- **Meta**: `description` (por página vía meta `_jw_meta_description`, o auto desde
  contenido/short description de producto), `canonical`, `robots`, `theme-color`.
- **Open Graph + Twitter Cards** en todas las páginas; en productos añade
  `product:price:amount/currency/availability`.
- **JSON-LD** (`schema.org`): `Organization` + `WebSite` (con `SearchAction`) en todo
  el sitio; `Product` + `Offer` + `Brand` en fichas de producto; `BreadcrumbList` en
  páginas internas.
- **Títulos**: portada `Julia Wisteria · The Art of Artisan Gifting`; internas
  `Título · Julia Wisteria`.
- **robots.txt** (virtual): permite el rastreo, bloquea cart/checkout/my-account,
  referencia el sitemap y `llms.txt`, y autoriza GPTBot / Google-Extended.
- **Sitemap**: `wp-sitemap.xml` nativo de WordPress (incluye páginas, productos y
  categorías; excluye usuarios y el blog vacío).
- **llms.txt**: `wp-local/site/llms.txt` describe el sitio para crawlers de IA.

### Conectar a Google
1. En Google Search Console, añade la propiedad con tu dominio de producción.
2. Copia el token de verificación (método "etiqueta HTML") en la constante
   `JW_GOOGLE_SITE_VERIFICATION` de `jw-seo.php` → se inyecta el meta automáticamente.
3. Envía el sitemap `https://tu-dominio/wp-sitemap.xml`.
4. En producción cambia las URLs (`siteurl`/`home`) y revisa que `blog_public` = 1.

> Para una imagen social por defecto, sube un PNG 1200×630 y pon su URL en
> `JW_DEFAULT_OG_IMAGE` dentro de `jw-seo.php`.

## 10. Checklist final

- [ ] Hello Elementor + Elementor + Elementor Pro + WooCommerce + Safe SVG activos
- [ ] Site Settings: colores y tipografías globales
- [ ] SVGs subidos a Medios
- [ ] Categorías creadas con imagen
- [ ] `productos.csv` importado (verifica las 3 variaciones de Romance Box)
- [ ] Header/Footer publicados con condición "Todo el sitio"
- [ ] Menú principal creado y asignado al widget Nav Menu
- [ ] Home / Our Story / Corporate / Build Your Box creadas con sus plantillas
- [ ] Theme Builder: "JW – Shop All" publicada (All Product Archives) y "JW – Single Product" (All Products)
- [ ] Cart y Checkout estilizados con los widgets Cart/Checkout
- [ ] Formularios con acción de envío configurada
- [ ] Página de inicio asignada en Ajustes → Lectura
