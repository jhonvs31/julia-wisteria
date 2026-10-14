# Julia Wisteria — Christmas Season en WordPress + Elementor + WooCommerce

Kit que monta en WordPress el diseño de la propuesta *Christmas Season* (la misma de la web estática:
`julia-wisteria.html`, `about.html`, `shop.html`, `product.html`, `build.html`, `cart.html`, `corporate.html`).

## Qué se construye

| Web estática | WordPress | Cómo |
|---|---|---|
| Header + barra de anuncio | Theme Builder › Header (#79) | Heading, Nav Menu, Menu Cart, Progress Tracker, contenedor *sticky* |
| Footer + newsletter | Theme Builder › Footer (#76) | Heading, Form, Icon List, Social Icons |
| Home | Página *Home* (#45) | Hero con collage, marquee, chips, historia, bento de cajas, features, CTA |
| Our Story | Página *Our Story* (#46) | Historia de Julia, simbolismo Wisteria, propósito, lema |
| Christmas Boxes (shop) | Theme Builder › Product Archive (#85) | Archive Products + chips de categoría |
| Ficha de caja | Theme Builder › Single Product (#88) | Product Images/Title/Price/Add to Cart/Content + Related |
| Customize | Página *Customize* (#48) | **Form multipaso** (elige caja → personaliza → datos) |
| Quote list / carrito | Páginas *Cart* (#7) y *Checkout* (#8) | Widgets Cart y Checkout de Woo |
| Corporate | Página *Corporate* (#47) | Ocasiones, proceso, **Form** de cotización |

Todo con widgets nativos de Elementor / Pro. No hay widgets de HTML personalizado.

## Animaciones

**Nativas de Elementor** (editables en *Avanzado › Efectos de movimiento*):
- Entrance Animation: `fadeInUp`, `zoomIn`, `fadeInLeft`, `fadeIn` con retardos escalonados.
- Mouse Effects › 3D Tilt en el collage del hero y en las miniaturas de Customize.
- Scrolling Effects › Vertical Scroll (parallax) en "JW/J" y en la foto de Our Story.
- Sticky: header y columna izquierda de la historia y de la ficha de producto.
- Progress Tracker: barra de progreso de scroll.
- Text Path: el sello circular que gira en el hero.
- Hover Animation `float`/`grow` en icon-box y redes.

**CSS de marca** (*Site Settings › Custom CSS*, archivo `jw-site.css`): blobs del fondo, grano, brillo del
titular, flotación del collage, marquee, botones pill con relleno, hover de las tarjetas, estilos de Woo y formularios.
Se activa con clases CSS (`jw-hero`, `jw-btn`, `jw-bx`, `jw-lift`…) puestas en *Avanzado › Clases CSS*.

**mu-plugin `jw-motion.php`**: pétalos que caen, brillo que sigue al cursor, titulares que entran palabra
a palabra (`jw-split`) y botones magnéticos. Respeta *prefers-reduced-motion* y no corre en el editor.

## Instalar / regenerar

```bash
./install.sh
```

1. `setup_content.php` sube las 5 fotos + `wisteria.svg`, crea categorías (*Christmas Season, Corporate, Wellness,
   Tea, Desk, Rest*) y los 5 productos. Manda a la papelera los productos antiguos. Es idempotente.
2. `build_elementor.py` genera `out/*.json` (lee `boxes.json` e `ids.json`).
3. `apply_elementor.php` escribe el JSON en las páginas/plantillas, actualiza Site Settings y limpia la caché.

Para cambiar textos o productos, edita `boxes.json` o `build_elementor.py` y vuelve a ejecutar `install.sh`;
o edita directamente en Elementor (regenerar sobrescribe esos cambios).

## Pendiente antes de publicar

- **Precios**: $95 / $85 / $75 / $80 / $90 son **de ejemplo**. Confírmalos con la cliente (Productos › editar).
- **Pagos**: activar una pasarela en WooCommerce › Ajustes › Pagos.
- **Email de formularios**: Corporate y Customize envían al email de administración de WordPress.
- **Dominio**: las imágenes guardan URLs `http://localhost:8081`. Tras migrar, usa
  Elementor › Herramientas › Reemplazar URL.
