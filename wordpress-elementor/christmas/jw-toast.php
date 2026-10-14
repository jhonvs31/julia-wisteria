<?php
/**
 * Plugin Name: Julia Wisteria — Avisos emergentes
 * Description: Cada ~22 s muestra un aviso pequeño con información REAL: una caja destacada
 *              (precio y enlace sacados de WooCommerce), envío gratis en Orlando, regalos
 *              corporativos y los días que faltan para Navidad. No muestra actividad inventada.
 *              Se puede cerrar (queda oculto en esa sesión). No aparece en carrito ni checkout.
 * Version: 1.0
 */
if (!defined('ABSPATH')) exit;

add_action('wp_footer', function () {
    if (isset($_GET['elementor-preview']) || is_admin()) return;
    if (function_exists('is_cart') && (is_cart() || is_checkout())) return;
    if (!function_exists('wc_get_products')) return;

    $items = [];
    foreach (wc_get_products(['status' => 'publish', 'limit' => 12, 'orderby' => 'menu_order', 'order' => 'ASC']) as $p) {
        $img = wp_get_attachment_image_url($p->get_image_id(), 'thumbnail');
        $items[] = [
            'kicker' => 'Featured this season',
            'title'  => html_entity_decode($p->get_name()),
            'sub'    => trim(wp_strip_all_tags(html_entity_decode(wc_price($p->get_price()))) . ' · ' . wp_strip_all_tags($p->get_short_description())),
            'img'    => $img ?: '',
            'href'   => get_permalink($p->get_id()),
        ];
    }
    $items[] = ['icon' => '🚚', 'kicker' => 'Good to know', 'title' => 'Free delivery in Orlando, Florida', 'sub' => 'On every Christmas box', 'href' => home_url('/shop/')];
    $items[] = ['icon' => '✉️', 'kicker' => 'Corporate gifting', 'title' => 'Personalized cards & custom branding', 'sub' => 'Request a quote for your team', 'href' => home_url('/corporate/#quote')];

    $js = @file_get_contents(__DIR__ . '/jw-toast.js');
    if (!$js) return;
    ?>
<script><?php echo $js; ?></script>
<script>
(function(){
  var list=<?php echo wp_json_encode($items); ?>;
  var d=JWToast.daysToChristmas();
  if(d>0)list.push({icon:'🎄',kicker:'Christmas Season',title:d+(d===1?' day':' days')+' until Christmas',sub:'Order early so your gifts arrive on time',href:<?php echo wp_json_encode(home_url('/shop/')); ?>});
  JWToast.start(list);
})();
</script>
    <?php
}, 60);
