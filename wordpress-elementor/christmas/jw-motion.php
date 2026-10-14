<?php
/**
 * Plugin Name: Julia Wisteria — Motion layer
 * Description: Efectos que Elementor no trae de serie: pétalos que caen, brillo que sigue
 *              al cursor, titulares que entran palabra a palabra (.jw-split) y botones
 *              magnéticos (.jw-btn). Las entradas, parallax, tilt y sticky son nativos
 *              de Elementor. Respeta prefers-reduced-motion. No corre dentro del editor.
 * Version: 1.0
 */

if (!defined('ABSPATH')) exit;

// Progress Tracker (Pro) falla en archivos de Woo/carrito porque settings.page no existe.
add_action('wp_footer', function () {
    echo "<script>(function(c){if(c&&c.settings&&!c.settings.page){c.settings.page={}}})(window.elementorFrontendConfig);</script>\n";
}, 25);

add_action('wp_footer', function () {
    if (isset($_GET['elementor-preview'])) return;
    ?>
<div class="jw-glow" aria-hidden="true"></div><div class="jw-fall" aria-hidden="true"></div>
<script>
(function(){
  var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  var $=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))};

  // titulares palabra a palabra
  $('.jw-split .elementor-heading-title').forEach(function(el){
    var i=0;
    (function walk(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(n){
        if(n.nodeType===3){
          var f=document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function(t){
            if(!t) return;
            if(/^\s+$/.test(t)){f.appendChild(document.createTextNode(' '));return}
            var w=document.createElement('span');w.className='w';
            var s=document.createElement('span');s.textContent=t;s.style.setProperty('--i',i++);
            w.appendChild(s);f.appendChild(w);
          });
          node.replaceChild(f,n);
        } else if(n.nodeType===1&&n.tagName!=='BR'){walk(n)}
      });
    })(el);
  });
  var splits=$('.jw-split');
  if(reduce||!('IntersectionObserver' in window)){splits.forEach(function(s){s.classList.add('in')});return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.2});
  splits.forEach(function(s){io.observe(s)});

  // pétalos de wisteria / nieve suave
  var fall=document.querySelector('.jw-fall'),cols=['#D4B4B5','#B9A6D3','#fff','#E6DDF2','#E8C9CB'];
  for(var k=0;k<22;k++){var p=document.createElement('span');
    p.style.cssText='left:'+(Math.random()*100)+'%;--s:'+(6+Math.random()*9)+'px;--c:'+cols[k%5]+';--t:'+(14+Math.random()*16)+'s;--dl:-'+(Math.random()*24)+'s;--x:'+((Math.random()-.5)*220)+'px';
    fall.appendChild(p)}

  if(!matchMedia('(pointer:fine)').matches) return;
  // brillo que sigue al cursor
  var g=document.querySelector('.jw-glow');
  addEventListener('pointermove',function(e){g.style.left=e.clientX+'px';g.style.top=e.clientY+'px'},{passive:true});
  // botones magnéticos
  $('.jw-btn .elementor-button').forEach(function(b){
    b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect();
      b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.18)+'px,'+((e.clientY-r.top-r.height/2)*.28)+'px)'});
    b.addEventListener('pointerleave',function(){b.style.transform=''});
  });
})();
</script>
    <?php
}, 50);
