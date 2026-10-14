<?php
/**
 * Julia Wisteria — Christmas Season: medios, categorías y productos WooCommerce.
 * Uso: wp eval-file setup_content.php   (idempotente: reutiliza lo ya creado)
 * Escribe ids.json junto a este archivo para que build_elementor.py lo use.
 */
if (!defined('ABSPATH')) exit;
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$dir   = __DIR__;
$boxes = json_decode(file_get_contents("$dir/boxes.json"), true);
$ids   = ['img' => [], 'product' => [], 'cat' => []];

// ---------- medios ----------
function jw_media($file, $key, $title) {
    $found = get_posts(['post_type' => 'attachment', 'meta_key' => '_jw_key', 'meta_value' => $key, 'numberposts' => 1, 'fields' => 'ids']);
    if ($found) return (int) $found[0];
    $tmp = wp_tempnam($file);
    copy($file, $tmp);
    $id = media_handle_sideload(['name' => basename($file), 'tmp_name' => $tmp], 0, $title);
    if (is_wp_error($id)) { WP_CLI::error($id->get_error_message()); }
    update_post_meta($id, '_jw_key', $key);
    update_post_meta($id, '_wp_attachment_image_alt', $title);
    return (int) $id;
}
foreach ($boxes as $b) {
    $ids['img'][$b['i']] = jw_media("$dir/{$b['i']}.jpg", $b['i'], $b['t']);
}
$ids['img']['wisteria'] = jw_media("$dir/wisteria.svg", 'wisteria', 'Wisteria flower');
// logos de la cliente
$ids['img']['logo']       = jw_media("$dir/brand/logo-julia-wisteria.png", 'logo', 'Julia Wisteria — The Art of Artisan Gifting');
$ids['img']['logo-light'] = jw_media("$dir/brand/logo-julia-wisteria-light.png", 'logo-light', 'Julia Wisteria — The Art of Artisan Gifting');
$ids['img']['monogram']   = jw_media("$dir/brand/monogram-jw.png", 'monogram', 'Julia Wisteria monogram');
$ids['img']['site-icon']  = jw_media("$dir/brand/site-icon-512.png", 'site-icon-round', 'Julia Wisteria');   // redondo, con transparencia
$ids['img']['apple-icon'] = jw_media("$dir/brand/apple-touch-icon.png", 'apple-touch', 'Julia Wisteria');   // cuadrado para iOS
update_option('site_icon', $ids['img']['site-icon']);   // favicon
update_option('jw_apple_touch_icon', $ids['img']['apple-icon']);

// ---------- categorías ----------
$cats = ['Christmas Season' => 'christmas-season', 'Corporate' => 'corporate', 'Wellness' => 'wellness', 'Tea' => 'tea', 'Desk' => 'desk', 'Rest' => 'rest'];
foreach ($cats as $name => $slug) {
    $t = get_term_by('slug', $slug, 'product_cat');
    if (!$t) { $r = wp_insert_term($name, 'product_cat', ['slug' => $slug]); $tid = $r['term_id']; }
    else { $tid = $t->term_id; }
    $ids['cat'][$name] = (int) $tid;
}

// ---------- productos antiguos → papelera ----------
$old = get_posts(['post_type' => 'product', 'numberposts' => -1, 'post_status' => 'any', 'meta_query' => [['key' => '_jw_box', 'compare' => 'NOT EXISTS']]]);
foreach ($old as $p) { wp_trash_post($p->ID); }
foreach (['for-her', 'baby', 'custom', 'seasonal'] as $slug) {
    $t = get_term_by('slug', $slug, 'product_cat');
    if ($t) wp_delete_term($t->term_id, 'product_cat');
}

// ---------- productos nuevos ----------
foreach ($boxes as $n => $b) {
    $found = get_posts(['post_type' => 'product', 'meta_key' => '_jw_box', 'meta_value' => $b['i'], 'numberposts' => 1, 'post_status' => 'any']);
    $product = $found ? wc_get_product($found[0]->ID) : new WC_Product_Simple();
    $desc  = '<p>' . esc_html($b['d']) . '</p>';
    $desc .= '<h4>What\'s inside</h4><ul>';
    foreach ($b['inc'] as $item) $desc .= '<li>' . esc_html($item) . '</li>';
    $desc .= '</ul><p class="jw-q">✨ ' . esc_html($b['q']) . '</p>';

    $product->set_name($b['t']);
    $product->set_slug($b['slug']);
    $product->set_status('publish');
    $product->set_catalog_visibility('visible');
    $product->set_description($desc);
    $product->set_short_description('<p>' . esc_html($b['s']) . '</p>');
    $product->set_regular_price((string) $b['price']);   // precio del catálogo de la cliente (boxes.json)
    $product->set_image_id($ids['img'][$b['i']]);
    $product->set_category_ids([$ids['cat'][$b['cat']], $ids['cat']['Christmas Season']]);
    $product->set_menu_order($n);
    $product->set_manage_stock(false);
    $product->set_stock_status('instock');
    $pid = $product->save();
    update_post_meta($pid, '_jw_box', $b['i']);
    update_post_meta($pid, '_jw_kicker', $b['k']);
    $ids['product'][$b['i']] = $pid;
}

// ---------- popups de vista rápida (contenido lo pone apply_elementor.php) ----------
$ids['popup'] = [];
foreach ($boxes as $b) {
    $found = get_posts(['post_type' => 'elementor_library', 'meta_key' => '_jw_qv', 'meta_value' => $b['i'], 'numberposts' => 1, 'post_status' => 'any', 'fields' => 'ids']);
    $pid = $found ? (int) $found[0] : wp_insert_post(['post_type' => 'elementor_library', 'post_status' => 'publish', 'post_title' => 'JW – Quick view: ' . $b['t']]);
    update_post_meta($pid, '_jw_qv', $b['i']);
    update_post_meta($pid, '_elementor_template_type', 'popup');
    wp_set_object_terms($pid, 'popup', 'elementor_library_type');
    $ids['popup'][$b['i']] = (int) $pid;
}

$ids['url'] = [];
foreach ($ids['img'] as $k => $aid) { $ids['url'][$k] = wp_get_attachment_url($aid); }
file_put_contents("$dir/ids.json", json_encode($ids, JSON_PRETTY_PRINT));
WP_CLI::success('Medios, categorías y productos listos: ' . json_encode($ids['product']));
