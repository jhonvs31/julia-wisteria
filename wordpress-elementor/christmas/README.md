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

## Pagos (Stripe + Apple Pay / Google Pay)

Pasarela: **WooCommerce Stripe Payment Gateway** (plugin oficial gratuito). `setup_payments.php` lo deja configurado:

| Método | Dónde aparece | Comisión EE. UU. (estándar de Stripe) |
|---|---|---|
| Apple Pay / Google Pay | Botones *Express Checkout* en ficha, carrito y checkout | Igual que tarjeta |
| Tarjeta de crédito/débito + Link | Checkout | 2.9% + 30¢ |
| ACH Direct Debit (cuenta bancaria) | Checkout | 0.8%, tope $5 — ideal para pedidos corporativos grandes |
| Wire transfer (BACS) | Checkout | Sin comisión; manual. Desactivar si no se usa |

"Cash on Delivery" queda desactivado. En el WordPress local Stripe no aparece en el checkout hasta conectar una cuenta.

### Activar en producción (lo hace la cliente o con su acceso)

1. La web debe estar en su **dominio con HTTPS** (Apple Pay no funciona en `http` ni en `localhost`).
2. WooCommerce › Settings › Payments › **Stripe › Connect** → iniciar sesión / crear la cuenta Stripe de la empresa
   (datos fiscales y bancarios de la cliente). Primero en *test mode* para probar.
3. En el **Dashboard de Stripe › Settings › Payment methods**: activar *Cards, Apple Pay, Google Pay, Link* y
   *ACH Direct Debit*. El plugin sincroniza esa lista.
4. Stripe › *Express checkout* → comprobar que el dominio aparece **verificado** (Apple Pay). Si no, pulsar
   *Re-verify domain* o añadirlo en Dashboard › Settings › Payment method domains.
5. Probar: Google Pay en Chrome con una tarjeta guardada; Apple Pay en Safari (iPhone/Mac) con Wallet.
   Tarjeta de prueba: `4242 4242 4242 4242`.
6. Desactivar *test mode* y hacer una compra real pequeña; reembolsarla desde el pedido.

## Pendiente antes de publicar

- **Precios**: Coffee & Planning $125 · Unwind & Recharge $135 · Teatime Delight $125 · Light Up Your Day $105 · Serenity Sleep $120 (catálogo de la cliente, oct. 2026).
- **Stripe**: conectar la cuenta de la cliente (ver arriba).
- **Impuestos (sales tax)**: configurar WooCommerce Tax o Stripe Tax según los estados donde venda.
- **Email de formularios**: Corporate y Customize envían al email de administración de WordPress.
- **Dominio**: las imágenes guardan URLs `http://localhost:8081`. Tras migrar, usa
  Elementor › Herramientas › Reemplazar URL.
