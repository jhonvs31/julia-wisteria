#!/bin/zsh
# Julia Wisteria — Christmas Season: instala el diseño en un WordPress con
# Elementor + Pro Elements/Elementor Pro + WooCommerce + Safe SVG.
# Uso:  ./install.sh [ruta-a-wp-cli]     (por defecto: ../../wp-local/bin/wp --path=../../wp-local/site)
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ -n "$1" ]]; then WP=("$@"); else
  export PHPRC="$DIR/../../wp-local"
  WP=("$DIR/../../wp-local/bin/wp" "--path=$DIR/../../wp-local/site")
fi
"${WP[@]}" eval-file "$DIR/setup_content.php" --user=1        # medios, categorías, productos
python3 "$DIR/build_elementor.py"                               # genera out/*.json
"${WP[@]}" eval-file "$DIR/apply_elementor.php" --user=1       # páginas, plantillas, Site Settings
MU="$("${WP[@]}" eval 'echo WPMU_PLUGIN_DIR;')"
cp "$DIR/jw-motion.php" "$MU/jw-motion.php"                     # capa de movimiento
"${WP[@]}" plugin is-installed woocommerce-gateway-stripe || "${WP[@]}" plugin install woocommerce-gateway-stripe
"${WP[@]}" plugin activate woocommerce-gateway-stripe
"${WP[@]}" eval-file "$DIR/setup_payments.php" --user=1      # Stripe: tarjetas, ACH, Apple Pay / Google Pay
"${WP[@]}" rewrite flush
echo "Listo."
