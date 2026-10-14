<?php
/**
 * Plugin Name: Julia Wisteria — Brand icons
 * Description: El favicon (Ajustes › Icono del sitio) es redondo con transparencia. iOS no admite
 *              transparencia en el apple-touch-icon (la pinta en negro), así que aquí se sirve
 *              una versión cuadrada crema; iOS ya le redondea las esquinas.
 * Version: 1.0
 */
if (!defined('ABSPATH')) exit;

add_filter('site_icon_meta_tags', function ($tags) {
    $id = (int) get_option('jw_apple_touch_icon');
    if (!$id) return $tags;
    $url = wp_get_attachment_url($id);
    foreach ($tags as $i => $tag) {
        if (strpos($tag, 'apple-touch-icon') !== false) {
            $tags[$i] = '<link rel="apple-touch-icon" href="' . esc_url($url) . '" />';
        }
    }
    return $tags;
});
