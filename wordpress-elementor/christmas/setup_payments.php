<?php
/**
 * Julia Wisteria — pagos con Stripe (WooCommerce Stripe Payment Gateway).
 * Uso: wp plugin install woocommerce-gateway-stripe --activate && wp eval-file setup_payments.php
 *
 * Deja configurados tarjetas, Link, ACH Direct Debit y los botones Express Checkout
 * (Apple Pay / Google Pay). NO guarda claves: la cliente conecta su propia cuenta
 * de Stripe desde WooCommerce › Settings › Payments › Stripe.
 */
if (!defined('ABSPATH')) exit;

$s = get_option('woocommerce_stripe_settings', []);
$s = array_merge(is_array($s) ? $s : [], [
    'enabled'                                   => 'yes',
    'testmode'                                  => 'yes',   // pasar a 'no' cuando la cuenta live esté conectada
    'title'                                     => 'Credit / Debit Card',
    'capture'                                   => 'yes',
    'saved_cards'                               => 'yes',
    'statement_descriptor'                      => 'JULIA WISTERIA',
    'short_statement_descriptor'                => 'JWISTERIA',
    'upe_checkout_experience_enabled'           => 'yes',
    'upe_checkout_experience_accepted_payments' => ['card', 'link', 'us_bank_account'],
    // Apple Pay / Google Pay
    'express_checkout'                          => 'yes',
    'express_checkout_button_type'              => 'buy',
    'express_checkout_button_theme'             => 'dark',
    'express_checkout_button_size'              => 'large',
    'express_checkout_button_height'            => '52',
    'express_checkout_button_branded_type'      => 'long',
    'express_checkout_button_locations'         => ['product', 'cart', 'checkout'],
]);
update_option('woocommerce_stripe_settings', $s);

// Contra reembolso no aplica a cajas enviadas por paquetería.
$cod = get_option('woocommerce_cod_settings', []);
$cod['enabled'] = 'no';
update_option('woocommerce_cod_settings', $cod);

// Transferencia: se mantiene solo como "wire" para pedidos corporativos grandes
// hasta conectar Stripe (ACH la sustituye). Desactivar luego si no se usa.
$bacs = get_option('woocommerce_bacs_settings', []);
$bacs['title']       = 'Wire transfer (corporate orders)';
$bacs['description'] = 'For large corporate orders. We will email you our bank details; your order ships once funds clear.';
update_option('woocommerce_bacs_settings', $bacs);

// Tienda en EE. UU.
update_option('woocommerce_currency', 'USD');
if (strpos((string) get_option('woocommerce_default_country'), 'US') !== 0) {
    update_option('woocommerce_default_country', 'US:FL');
}

WP_CLI::success('Stripe listo para conectar: tarjetas, Link, ACH y Apple Pay / Google Pay (Express Checkout).');
