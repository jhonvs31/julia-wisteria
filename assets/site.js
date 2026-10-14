/* Julia Wisteria — shared data + helpers */
window.BOXES=[
 {i:'coffee-planning',price:95,cat:'Corporate',k:'Corporate',t:'The Coffee & Planning Gift Box',s:'Fresh starts, productive mornings, inspired plans.',
  d:'A thoughtful gift designed for fresh starts, productive mornings, and inspired plans. It pairs premium specialty coffee with an artisan ceramic mug, an elegant gold coffee scoop, and a 2027 dated planner — a beautiful daily ritual for planning goals while enjoying a favorite cup of coffee. Complete with mini sticky notes and a personalized welcome card, this elevated collection is ideal for employee appreciation, client gifting, executive gifts, onboarding, welcome programs, and New Year celebrations.',
  inc:['Premium specialty coffee','Artisan ceramic mug','Gold coffee scoop','2027 Dated Planner – classic, simple, and playful, designed to keep you organized and inspired all year','Mini sticky notes','Pens','Personalized welcome card','Luxury gift box packaging','Optional custom branding'],q:'Plan the year. Enjoy the moment. Start with great coffee.'},
 {i:'unwind-recharge',price:85,cat:'Wellness',k:'Wellness Gift Collection',t:'Unwind & Recharge Box',s:'A restorative moment of self-care.',
  d:'A thoughtful invitation to slow down, breathe, and enjoy a restorative moment of self-care. It combines artisan body-care essentials with calming organic tea and an aromatherapy shower steamer. Rose & lime soap, grapefruit lip balm, nourishing hand cream, and the soothing notes of lavender, chamomile, and cedar create a comforting ritual for both body and mind. Perfect for wellness programs, executive retreats, employee appreciation, conference speakers, VIP guests, and thoughtful client gifting.',
  inc:['Artisan Rose & Lime Soap','Natural Grapefruit Lip Balm','Luxury Hand Cream','Meditative Mind organic tea','Peace Shower Steamer – a steam-activated aromatherapy blend of organic lavender, chamomile, and cedar essential oils designed to promote relaxation and tranquility','Towel','Personalized welcome card','Luxury gift box packaging'],q:'Sip. Breathe. Recharge.'},
 {i:'teatime-delight',price:75,cat:'Tea',k:'Tea, Honey & Mug Gift Experience',t:'Teatime Delight Box',s:'Tea, honey, candlelight — and a moment to unwind.',
  d:'A cozy gift created for slow, comforting moments. The Teatime Delight Box pairs a premium tea selection with artisan honey and a signature ceramic mug, while a Blooming Lilacs candle adds a soft floral touch to the experience. Together, these pieces create a warm ritual to sip, unwind, and enjoy. Perfect for conference speakers, VIP guests, executive retreats, wellness programs, hotel arrivals, employee appreciation, and client gifting.',
  inc:['Premium tea selection','Artisan honey jar','Honey dipper','Signature ceramic mug','Blooming Lilacs candle','Personalized welcome card','Luxury gift packaging'],q:'Tea, honey, candlelight — and a moment to unwind.'},
 {i:'light-up-your-day',price:80,cat:'Desk',k:'Candle, Planner & Desk Gift Experience',t:'Light Up Your Day Box',s:'Inspiration, greenery, and a little sweetness.',
  d:'Brighten the day with a gift that blends inspiration, greenery, and a little sweetness. It combines a hand-poured artisan candle with a mini succulent, a 2027 dated planner, and bear gummies — a cheerful collection for the desk, home, or office. Thoughtful and practical, this box is perfect for employee appreciation, client thank-yous, onboarding, New Year gifting, speakers, and corporate celebrations.',
  inc:['Hand-poured artisan candle','Mini succulent','2027 Dated Planner – classic, simple, and playful, designed to keep you organized and inspired all year','Gummy bears','Premium gift box packaging','Personalized message card'],q:'Light the candle. Make a plan. Grow something beautiful.'},
 {i:'serenity-sleep',price:90,cat:'Rest',k:'Relaxation & Rest Wellness Gift Box',t:'Serenity Sleep Box',s:'A calming end-of-day ritual.',
  d:'Create a calming end-of-day ritual. Thoughtfully curated for rest and relaxation, this collection combines a therapeutic eye mask, lavender body scrub, botanical body oil, natural lip balm, organic tea, and a playful beaded daisy keychain. From soothing body care to a comforting cup of tea, every element is selected to encourage the recipient to slow down, recharge, and enjoy a well-deserved moment of calm. Perfect for wellness programs, VIP guests, employee appreciation, retreats, speakers, and holiday gifting.',
  inc:['Beaded Daisy Keychain','Meditative Mind organic tea','Therapeutic Eye Mask','Lavender Body Scrub','Relaxing Botanical Body Oil','Natural Lip Balm','Personalized gift card'],q:'Rest. Relax. Recharge.'}
];
window.JW=(function(){
  var K='jw_cart';
  function get(){try{return JSON.parse(localStorage.getItem(K))||[]}catch(e){return[]}}
  function set(v){try{localStorage.setItem(K,JSON.stringify(v))}catch(e){}badge();if(drawer)render()}
  function count(){return get().reduce(function(a,x){return a+x.qty},0)}
  function subtotal(){return get().reduce(function(a,x){return a+x.qty*BOXES[x.id].price},0)}
  function money(n){return '$'+n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g,',')}
  function badge(){var n=count(),b=document.getElementById('qbadge');if(b){b.textContent=n;b.style.display=n?'flex':'none'}}
  function add(item){var l=get(),f=l.filter(function(x){return x.id===item.id&&x.brand===item.brand&&x.note===item.note})[0];if(f)f.qty+=item.qty;else l.push(item);set(l)}
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')}

  // ---- canasta lateral (como el Menu Cart de WordPress) ----
  var drawer;
  function build(){
    drawer=document.createElement('div');drawer.className='drw';drawer.setAttribute('aria-hidden','true');
    drawer.innerHTML='<div class="drw-p" role="dialog" aria-label="Cart"><button class="drw-x" aria-label="Close">✕</button><div class="drw-b"></div></div>';
    document.body.appendChild(drawer);
    drawer.addEventListener('click',function(e){
      if(e.target===drawer||e.target.closest('.drw-x'))return close();
      var r=e.target.closest('[data-rm]');if(r){var l=get();l.splice(+r.dataset.rm,1);set(l)}
    });
  }
  function render(){
    var l=get(),b=drawer.querySelector('.drw-b');
    if(!l.length){b.innerHTML='<p class="drw-empty">No products in the cart.</p><a class="btn-x solid" href="shop.html">Browse the boxes</a>';return}
    b.innerHTML=l.map(function(x,n){var p=BOXES[x.id];return '<div class="drw-i"><img src="images/christmas/'+p.i+'.jpg" alt=""><div><a href="product.html?box='+x.id+'" class="drw-n">'+esc(p.t)+'</a><span class="drw-q">'+x.qty+' × '+money(p.price)+'</span></div><button class="drw-rm" data-rm="'+n+'" aria-label="Remove">✕</button></div>'}).join('')+
      '<div class="drw-s">Subtotal: <b>'+money(subtotal())+'</b></div><div class="drw-a"><a class="btn-x sm" href="cart.html">View cart</a><a class="btn-x sm solid" href="checkout.html">Checkout</a></div>';
  }
  function open(){if(!drawer)build();render();requestAnimationFrame(function(){drawer.classList.add('open')});drawer.setAttribute('aria-hidden','false');document.body.style.overflow='hidden'}
  function close(){drawer.classList.remove('open');drawer.setAttribute('aria-hidden','true');document.body.style.overflow=''}
  addEventListener('keydown',function(e){if(e.key==='Escape'&&drawer&&drawer.classList.contains('open'))close()});

  // ---- Apple Pay / Google Pay (demo: en WordPress los pinta Stripe) ----
  var APPLE='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.6c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9-.7 0-1.9-.8-3-.8-1.6 0-3 .9-3.8 2.3-1.6 2.8-.4 7 1.2 9.3.8 1.1 1.7 2.4 2.9 2.3 1.2 0 1.6-.7 3-.7s1.8.7 3 .7c1.3 0 2.1-1.1 2.8-2.3.9-1.3 1.3-2.6 1.3-2.6s-2.5-1-2.5-3.8zM14.1 5.8c.6-.8 1.1-1.8 1-2.8-.9 0-2 .6-2.7 1.4-.6.7-1.1 1.7-1 2.7 1 .1 2-.5 2.7-1.3z"/></svg>';
  function express(el,getTotal,onPaid){
    el.innerHTML='<div class="xp"><button type="button" class="xp-b xp-apple" data-w="Apple Pay">Buy with '+APPLE+'<b>Pay</b></button>'+
      '<button type="button" class="xp-b xp-google" data-w="Google Pay">Buy with <i class="g">G</i><b>Pay</b></button></div><div class="xp-or">or</div>';
    el.addEventListener('click',function(e){var b=e.target.closest('.xp-b');if(b)sheet(b.dataset.w,getTotal(),onPaid)});
  }
  function sheet(wallet,total,onPaid){
    var m=document.createElement('div');m.className='paysh';
    m.innerHTML='<div class="paysh-c"><div class="paysh-h">'+(wallet==='Apple Pay'?APPLE+'<b>Pay</b>':'<i class="g">G</i><b>Pay</b>')+'</div>'+
      '<div class="paysh-r"><span>Julia Wisteria</span><b>'+money(total)+'</b></div>'+
      '<p class="paysh-n">Demo — in the live store this is the real '+wallet+' sheet powered by Stripe. No payment is made here.</p>'+
      '<button class="btn-x solid paysh-ok">Simulate '+wallet+' payment</button><button class="paysh-cancel">Cancel</button></div>';
    document.body.appendChild(m);requestAnimationFrame(function(){m.classList.add('open')});
    m.addEventListener('click',function(e){
      if(e.target===m||e.target.closest('.paysh-cancel')){m.remove();return}
      if(e.target.closest('.paysh-ok')){m.remove();(onPaid||function(){location.href='checkout.html?paid='+encodeURIComponent(wallet)})(wallet)}
    });
  }

  document.addEventListener('DOMContentLoaded',function(){
    badge();
    var c=document.getElementById('cartlink');
    if(c)c.addEventListener('click',function(e){e.preventDefault();open()});
  });
  return {get:get,set:set,add:add,badge:badge,esc:esc,money:money,count:count,subtotal:subtotal,open:open,express:express};
})();
(function(){
  var ham=document.getElementById('ham'),mn=document.getElementById('mob-nav'),mc=document.getElementById('mob-close');
  window.openMobNav=function(){ham.classList.add('open');mn.classList.add('open');document.body.style.overflow='hidden'};
  window.closeMobNav=function(){ham.classList.remove('open');mn.classList.remove('open');document.body.style.overflow=''};
  if(ham){ham.addEventListener('click',function(){ham.classList.contains('open')?closeMobNav():openMobNav()});mc.addEventListener('click',closeMobNav)}
})();
