<?php
/**
 * Julia Wisteria — aplica out/*.json a las páginas y plantillas de Elementor,
 * actualiza Site Settings (colores, fuentes, Custom CSS) y limpia la caché CSS.
 * Uso: wp eval-file apply_elementor.php
 */
if (!defined('ABSPATH')) exit;

$dir      = __DIR__;
$manifest = json_decode(file_get_contents("$dir/out/manifest.json"), true);
$version  = defined('ELEMENTOR_VERSION') ? ELEMENTOR_VERSION : '4.1.3';
$pages    = ['home', 'about', 'corporate', 'customize', 'cart', 'checkout'];

foreach ($manifest as $name => $post_id) {
    $json = file_get_contents("$dir/out/$name.json");
    if (json_decode($json) === null) { WP_CLI::error("JSON inválido: $name"); }
    update_post_meta($post_id, '_elementor_data', wp_slash($json));
    update_post_meta($post_id, '_elementor_edit_mode', 'builder');
    update_post_meta($post_id, '_elementor_version', $version);
    update_post_meta($post_id, '_elementor_pro_version', defined('ELEMENTOR_PRO_VERSION') ? ELEMENTOR_PRO_VERSION : '');
    delete_post_meta($post_id, '_elementor_css');
    delete_post_meta($post_id, '_elementor_element_cache');
    delete_post_meta($post_id, '_elementor_page_assets');
    if (file_exists("$dir/out/$name.settings.json")) {
        update_post_meta($post_id, '_elementor_page_settings', json_decode(file_get_contents("$dir/out/$name.settings.json"), true));
    }
    if (in_array($name, $pages, true)) {
        update_post_meta($post_id, '_wp_page_template', 'elementor_header_footer');
        update_post_meta($post_id, '_elementor_template_type', 'wp-page');
    }
    WP_CLI::log("✓ $name → #$post_id");
}

// Títulos / slugs
wp_update_post(['ID' => 45, 'post_title' => 'Home']);
wp_update_post(['ID' => 48, 'post_title' => 'Customize', 'post_name' => 'customize']);
wp_update_post(['ID' => 85, 'post_title' => 'JW – Christmas Boxes (Shop)']);

// Site Settings (Kit)
$kit_id   = (int) get_option('elementor_active_kit');
$settings = get_post_meta($kit_id, '_elementor_page_settings', true) ?: [];
$settings['system_colors'] = [
    ['_id' => 'primary', 'title' => 'Brown', 'color' => '#5A4642'],
    ['_id' => 'secondary', 'title' => 'Wine', 'color' => '#6E2F3B'],
    ['_id' => 'text', 'title' => 'Text', 'color' => '#7A6460'],
    ['_id' => 'accent', 'title' => 'Lilac', 'color' => '#B9A6D3'],
];
$settings['custom_colors'] = [
    ['_id' => 'jwcream', 'title' => 'Cream', 'color' => '#F9F2EB'],
    ['_id' => 'jwcreamd', 'title' => 'Cream Dark', 'color' => '#F0E6D9'],
    ['_id' => 'jwrose', 'title' => 'Rose', 'color' => '#B88889'],
    ['_id' => 'jwrosel', 'title' => 'Rose Light', 'color' => '#D4B4B5'],
    ['_id' => 'jwwined', 'title' => 'Wine Dark', 'color' => '#4A1D27'],
    ['_id' => 'jwlilacl', 'title' => 'Lilac Light', 'color' => '#E6DDF2'],
    ['_id' => 'jwmuted', 'title' => 'Muted', 'color' => '#8B7B78'],
];
$settings['body_color']                  = '#5A4642';
$settings['body_typography_typography']  = 'custom';
$settings['body_typography_font_family'] = 'Jost';
$settings['body_typography_font_weight'] = '300';
$settings['site_description']            = 'Corporate Gifting, Crafted with Meaning — Orlando, Florida.';
$settings['custom_css']                  = file_get_contents("$dir/jw-site.css");
update_post_meta($kit_id, '_elementor_page_settings', $settings);
delete_post_meta($kit_id, '_elementor_css');

// Plantillas antiguas sin uso → papelera
foreach ([67, 70, 73, 82] as $old) { if (get_post($old)) wp_trash_post($old); }

if (class_exists('\Elementor\Plugin')) {
    \Elementor\Plugin::$instance->files_manager->clear_cache();
}
WP_CLI::success('Elementor actualizado.');
