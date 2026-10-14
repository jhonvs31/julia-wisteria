"""Regenera las páginas estáticas (shop, product, build, cart, checkout, corporate) y el
shell común de todas. Home y Our Story se toman del HTML actual (solo se re-envuelven).
Uso: python3 tools/build_static.py"""
import os, re
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
home=open(R+'julia-wisteria.html',encoding='utf8').read()
about=open(R+'about.html',encoding='utf8').read()
HEAD=home[:home.index('<body>')]
HEAD=re.sub(r'<title>.*?</title>','<title>@@TITLE@@</title>',HEAD,flags=re.S)
if 'assets/motion.css' not in HEAD: raise SystemExit('no css')
home_mid=home[home.index('<!-- HERO -->'):home.index('<!-- MODAL -->')]
modal=home[home.index('<!-- MODAL -->'):home.index('<div class="nl">')]
about_mid=about[about.index('<!-- HERO -->'):about.index('<div class="nl">')]
about_mid=about_mid.replace('<!-- NEWSLETTER -->','')

def nav(active,pre=''):
    items=[('about.html','Our Story','about'),('shop.html','Christmas Boxes','shop'),('build.html','Customize','build'),('corporate.html','Corporate','corp')]
    AC=' class="active"'
    return ''.join('<a href="%s"%s>%s</a>'%(h,AC if k==active else '',t) for h,t,k in items)
def mob():
    return '<a href="julia-wisteria.html" onclick="closeMobNav()">Home</a>'+''.join(f'<a href="{h}" onclick="closeMobNav()">{t}</a>' for h,t in [('about.html','Our Story'),('shop.html','Christmas Boxes'),('build.html','Customize'),('corporate.html','Corporate'),('cart.html','Cart')])
def top(active):
    return f'''<body>
<div class="progress"></div><div class="glow"></div><div class="fall" aria-hidden="true"></div>
<div class="ann">Christmas Season 2026 &nbsp;<b>·</b>&nbsp; Free delivery in Orlando, Florida &nbsp;<b>·</b>&nbsp; Corporate gifting, crafted with meaning</div>
<div class="hdr-wrap"><div class="hdr">
  <div class="logo"><a href="julia-wisteria.html" aria-label="Julia Wisteria — Home"><img class="logo-img" src="assets/brand/logo-julia-wisteria.png" alt="Julia Wisteria — The Art of Artisan Gifting" width="900" height="472"></a></div>
  <nav>{nav(active)}</nav>
  <div class="icons">
    <a href="cart.html" id="cartlink" aria-label="Cart" style="display:flex;align-items:flex-start">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
      <span class="cbadge" id="qbadge" style="display:none">0</span>
    </a>
    <button class="ham" id="ham" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</div></div>
<div class="mob-nav" id="mob-nav"><button class="mob-nav-close" id="mob-close">✕</button>{mob()}</div>
'''
BOT='''<div class="nl">
  <h3 class="nl-h">Join the Julia Wisteria World</h3>
  <p class="nl-p">Early access to new collections, seasonal boxes &amp; gifting inspiration</p>
  <div class="nl-form"><input class="nl-i" type="email" placeholder="your@email.com" aria-label="Email"><button class="nl-btn">Subscribe</button></div>
</div>
<footer>
  <div class="fg">
    <div>
      <img class="fb-logo" src="assets/brand/logo-julia-wisteria-light.png" alt="Julia Wisteria — The Art of Artisan Gifting" width="900" height="472" loading="lazy">
      <p class="fb-p">Curated artisan gifts for corporate events, VIP experiences, employee recognition, incentive travel and destination programs. Orlando, Florida.</p>
      <div class="fsoc"><a href="https://www.instagram.com/juliawisteriagifts/" target="_blank" rel="noopener" aria-label="Instagram @juliawisteriagifts"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a><a class="fsoc-t" href="https://www.instagram.com/juliawisteriagifts/" target="_blank" rel="noopener">@juliawisteriagifts</a></div>
    </div>
    <div class="fc"><h4>Boxes</h4><ul><li><a href="product.html?box=0">Coffee &amp; Planning</a></li><li><a href="product.html?box=1">Unwind &amp; Recharge</a></li><li><a href="product.html?box=2">Teatime Delight</a></li><li><a href="product.html?box=3">Light Up Your Day</a></li><li><a href="product.html?box=4">Serenity Sleep</a></li></ul></div>
    <div class="fc"><h4>Company</h4><ul><li><a href="about.html">Our Story</a></li><li><a href="corporate.html">Corporate Gifting</a></li><li><a href="build.html">Customize a Box</a></li></ul></div>
    <div class="fc"><h4>Contact</h4><ul><li><a href="mailto:kangulo@juliawisteria.com">kangulo@juliawisteria.com</a></li><li><a href="corporate.html#quote">Request a Quote</a></li><li><a href="cart.html">Cart</a></li><li><a href="checkout.html">Checkout</a></li></ul></div>
  </div>
  <div class="fbot"><span class="fcp">© 2026 Julia Wisteria · Orlando, FL</span><span class="flo">Crafted with love. Inspired by family.</span></div>
</footer>
'''
FAVICONS='''<link rel="icon" type="image/png" sizes="32x32" href="assets/brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/brand/favicon-192.png">
<link rel="apple-touch-icon" href="assets/brand/apple-touch-icon.png">
<meta name="theme-color" content="#F9F2EB">
'''
def page(fn,title,active,body,js=''):
    h=HEAD.replace('@@TITLE@@',title)
    if 'rel="icon"' not in h:
        h=h.replace('</head>',FAVICONS+'</head>',1)
    out=h+top(active)+body+BOT+'<script src="assets/site.js"></script>\n<script src="assets/motion.js"></script>\n'+js+'</body>\n</html>\n'
    open(R+fn,'w',encoding='utf8').write(out)

# ---------- HOME ----------
home_js='''<script>
(function(){
  var m=document.getElementById('mdl');
  function open(i){var b=BOXES[i];
    document.getElementById('mdl-img').src='images/christmas/'+b.i+'.jpg';document.getElementById('mdl-img').alt=b.t;
    document.getElementById('mdl-k').textContent=b.k;document.getElementById('mdl-t').textContent=b.t;
    document.getElementById('mdl-d').textContent=b.d;document.getElementById('mdl-q').textContent=b.q;
    document.getElementById('mdl-l').innerHTML=b.inc.map(function(x){return '<li>'+JW.esc(x)+'</li>'}).join('');
    document.getElementById('mdl-go').href='product.html?box='+i;document.getElementById('mdl-p').textContent=JW.money(b.price);
    m.classList.add('open');m.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';}
  function close(){if(!m.classList.contains('open')||m.classList.contains('closing'))return;m.classList.add('closing');m.setAttribute('aria-hidden','true');
    setTimeout(function(){m.classList.remove('open','closing');document.body.style.overflow=''},520)}
  document.querySelectorAll('[data-box]').forEach(function(b){b.addEventListener('click',function(){open(+b.dataset.box)})});
  document.getElementById('mdl-x').addEventListener('click',close);
  m.addEventListener('click',function(e){if(e.target===m)close()});
  addEventListener('keydown',function(e){if(e.key==='Escape')close()});
})();
</script>
'''
modal2=re.sub(r'<a (id="mdl-go" )?href="[^"]*" class="btn-x solid">[^<]*<span class="ar">→</span></a>','<a id="mdl-go" href="product.html" class="btn-x solid">View &amp; add to cart <span class="ar">→</span></a>',modal)
if 'id="mdl-p"' not in modal2: modal2=modal2.replace('<h3 id="mdl-t"></h3>','<h3 id="mdl-t"></h3>\n      <span class="price" id="mdl-p"></span>')
home_mid=home_mid.replace('href="corporate.html#quote"','href="corporate.html#quote"')
page('julia-wisteria.html','Julia Wisteria — Corporate Gifting, Crafted with Meaning','',home_mid+modal2,home_js)

# ---------- ABOUT ----------
page('about.html','Our Story — Julia Wisteria','about',about_mid)

# ---------- SHOP ----------
shop='''<section class="ph">
  <div class="x-hero-bg"><div class="blob b1"></div><div class="blob b2"></div><div class="grain"></div></div>
  <div class="crumbs rv"><a href="julia-wisteria.html">Home</a> &nbsp;/&nbsp; Christmas Boxes</div>
  <span class="x-script rv">Christmas Season</span>
  <h1 class="x-h1 split">Five boxes, thoughtfully curated</h1>
  <p class="x-lead rv" style="--d:.3s">Corporate gifts for events, VIP experiences, employee recognition, incentive travel and destination programs.</p>
</section>
<div class="wrap">
  <div class="chips" id="chips"></div>
  <div class="sgrid" id="sgrid"></div>
</div>
'''
shop_js='''<script>
(function(){
  var cats=['All'].concat(BOXES.map(function(b){return b.cat}));
  var chips=document.getElementById('chips'),grid=document.getElementById('sgrid');
  chips.innerHTML=cats.map(function(c,i){return '<button class="chip'+(i?'':' on')+'" data-c="'+c+'">'+c+'</button>'}).join('');
  grid.innerHTML=BOXES.map(function(b,i){return '<article class="sc rv" style="--d:'+(i%3)*.1+'s" data-c="'+b.cat+'">'+
   '<a class="sc-img" href="product.html?box='+i+'"><img src="images/christmas/'+b.i+'.jpg" alt="'+JW.esc(b.t)+'" loading="lazy"><span class="bx-n">0'+(i+1)+'</span></a>'+
   '<div class="sc-b"><span class="sc-k">'+JW.esc(b.k)+'</span><a href="product.html?box='+i+'" class="sc-t">'+JW.esc(b.t)+'</a><span class="price">'+JW.money(b.price)+'</span><p class="sc-s">'+JW.esc(b.s)+'</p>'+
   '<div class="sc-a"><a href="product.html?box='+i+'" class="btn-x sm">See what\\'s inside</a><button class="btn-x sm solid" data-add="'+i+'">Add to cart</button></div></div></article>'}).join('');
  chips.addEventListener('click',function(e){var c=e.target.closest('.chip');if(!c)return;
    chips.querySelectorAll('.chip').forEach(function(x){x.classList.toggle('on',x===c)});
    grid.querySelectorAll('.sc').forEach(function(s){s.classList.toggle('off',c.dataset.c!=='All'&&s.dataset.c!==c.dataset.c);s.classList.add('in')})});
  grid.addEventListener('click',function(e){var b=e.target.closest('[data-add]');if(!b)return;
    JW.add({id:+b.dataset.add,qty:1,brand:false,note:''});JW.open()});
  document.querySelectorAll('.sc').forEach(function(s){if(window.IntersectionObserver)return;s.classList.add('in')});
  // observe newly rendered .rv
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
  grid.querySelectorAll('.rv').forEach(function(x){io.observe(x)});
})();
</script>
'''
page('shop.html','Christmas Boxes — Julia Wisteria','shop',shop,shop_js)

# ---------- PRODUCT ----------
prod='''<div class="wrap">
  <div class="crumbs" style="padding-top:34px"><a href="julia-wisteria.html">Home</a> &nbsp;/&nbsp; <a href="shop.html">Christmas Boxes</a> &nbsp;/&nbsp; <span id="bc"></span></div>
  <div class="pdp2">
    <div class="pdp2-img rv rv-s"><img id="p-img" alt=""></div>
    <div>
      <span class="x-script rv" id="p-k"></span>
      <h1 class="split" id="p-t"></h1>
      <span class="price rv" id="p-price"></span>
      <p class="lead rv" id="p-d"></p>
      <div class="h4s rv">What's inside</div>
      <ul class="inc" id="p-l"></ul>
      <div class="mq-q rv" id="p-q"></div>
      <div class="pdp-buy rv">
        <div class="pdp-row"><div class="stepper"><button type="button" id="m" aria-label="Less">−</button><input id="qty" type="number" min="1" value="1" aria-label="Quantity"><button type="button" id="p" aria-label="More">+</button></div><span style="font-size:12px;color:var(--muted)">boxes</span></div>
        <label class="ck"><input type="checkbox" id="brand"> Add optional custom branding</label>
        <input class="field" id="note" placeholder="Personalized welcome card message (optional)">
        <div class="pdp-row"><button class="btn-x solid" id="add">Add to cart <span class="ar">→</span></button><a class="btn-x" href="corporate.html#quote">Corporate quote</a></div>
        <div id="xp"></div>
      </div>
    </div>
  </div>
  <div class="related2"><h2 class="split">You may also love</h2><div class="rgrid" id="rel"></div></div>
</div>
'''
prod_js='''<script>
(function(){
  var i=+(new URLSearchParams(location.search).get('box'));if(!(i>=0&&i<BOXES.length))i=0;var b=BOXES[i];
  document.title=b.t+' — Julia Wisteria';
  var pi=document.getElementById('p-img');pi.src='images/christmas/'+b.i+'.jpg';pi.alt=b.t;
  document.getElementById('bc').textContent=b.t;document.getElementById('p-k').textContent=b.k;
  document.getElementById('p-t').textContent=b.t;document.getElementById('p-price').textContent=JW.money(b.price);document.getElementById('p-d').textContent=b.d;document.getElementById('p-q').textContent='✨ '+b.q;
  document.getElementById('p-l').innerHTML=b.inc.map(function(x,n){return '<li><i>'+('0'+(n+1)).slice(-2)+'</i><span>'+JW.esc(x)+'</span></li>'}).join('');
  var q=document.getElementById('qty');
  document.getElementById('m').onclick=function(){q.value=Math.max(1,+q.value-1)};
  document.getElementById('p').onclick=function(){q.value=+q.value+1};
  document.getElementById('add').onclick=function(){JW.add({id:i,qty:Math.max(1,+q.value||1),brand:document.getElementById('brand').checked,note:document.getElementById('note').value.trim()});JW.open()};
  function item(){return {id:i,qty:Math.max(1,+q.value||1),brand:document.getElementById('brand').checked,note:document.getElementById('note').value.trim()}}
  JW.express(document.getElementById('xp'),function(){return b.price*Math.max(1,+q.value||1)},function(w){JW.add(item());location.href='checkout.html?paid='+encodeURIComponent(w)});
  document.getElementById('rel').innerHTML=BOXES.map(function(x,n){return n===i?'':'<article class="sc rv" style="--d:'+(n%4)*.08+'s"><a class="sc-img" href="product.html?box='+n+'"><img src="images/christmas/'+x.i+'.jpg" alt="'+JW.esc(x.t)+'" loading="lazy"></a><div class="sc-b"><a class="sc-t" href="product.html?box='+n+'">'+JW.esc(x.t)+'</a></div></article>'}).join('');
  if(window.IntersectionObserver){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});document.querySelectorAll('#rel .rv').forEach(function(x){io.observe(x)})}else document.querySelectorAll('#rel .rv').forEach(function(x){x.classList.add('in')});
})();
</script>
'''
page('product.html','Julia Wisteria — Christmas Box','shop',prod,prod_js)

# ---------- BUILD ----------
build='''<section class="ph" style="padding-bottom:30px">
  <div class="x-hero-bg"><div class="blob b1"></div><div class="blob b2"></div><div class="grain"></div></div>
  <div class="crumbs rv"><a href="julia-wisteria.html">Home</a> &nbsp;/&nbsp; Customize</div>
  <span class="x-script rv">Made for your team</span>
  <h1 class="x-h1 split">Customize your gift</h1>
  <div class="steps2" id="steps2"><span class="on"><b>1</b>Choose a box</span><span><b>2</b>Personalize</span><span><b>3</b>Review</span></div>
</section>
<div class="wrap">
  <div class="stp on" id="s1">
    <h2 class="sec-h" style="text-align:center">Which box fits the moment?</h2>
    <div class="pick" id="pick"></div>
    <div class="nav-st" style="justify-content:center"><button class="btn-x solid" id="n1" disabled style="opacity:.4">Continue <span class="ar">→</span></button></div>
  </div>
  <div class="stp" id="s2">
    <h2 class="sec-h" style="text-align:center">Make it yours</h2>
    <div class="sform">
      <div><label>Number of boxes</label><div class="stepper"><button type="button" id="bm">−</button><input id="bq" type="number" min="1" value="25"><button type="button" id="bp">+</button></div></div>
      <div><label>Personalized card message</label><textarea class="field" id="bn" rows="3" placeholder="Thank you for a wonderful year…"></textarea></div>
      <label class="ck" style="display:flex;gap:12px;align-items:center;text-transform:none;letter-spacing:0;font-size:14px;cursor:pointer"><input type="checkbox" id="bb" style="accent-color:var(--wine);width:18px;height:18px"> Add optional custom branding (logo &amp; colors)</label>
    </div>
    <div class="nav-st" style="max-width:720px;margin-inline:auto"><button class="btn-x" data-go="1">← Back</button><button class="btn-x solid" data-go="3">Review <span class="ar">→</span></button></div>
  </div>
  <div class="stp" id="s3">
    <h2 class="sec-h" style="text-align:center">Review your box</h2>
    <div class="rev"><img id="rv-i" alt=""><div><span class="x-script" id="rv-k"></span><h3 class="sec-h" style="margin:0" id="rv-t"></h3><dl id="rv-d"></dl>
      <div class="pdp-row"><button class="btn-x solid" id="fin">Add to cart <span class="ar">→</span></button><button class="btn-x" data-go="2">← Edit</button></div></div></div>
  </div>
</div>
'''
build_js='''<script>
(function(){
  var sel=-1,st=document.getElementById('steps2').children;
  var pick=document.getElementById('pick');
  var pre=+(new URLSearchParams(location.search).get('box'));
  pick.innerHTML=BOXES.map(function(b,i){return '<button class="pk rv" style="--d:'+i*.07+'s" data-i="'+i+'"><img src="images/christmas/'+b.i+'.jpg" alt=""><span>'+JW.esc(b.t)+'</span></button>'}).join('');
  function go(n){for(var k=1;k<=3;k++)document.getElementById('s'+k).classList.toggle('on',k===n);
    [].forEach.call(st,function(s,j){s.classList.toggle('on',j===n-1);s.classList.toggle('done',j<n-1)});scrollTo({top:0,behavior:'smooth'});
    if(n===3){var b=BOXES[sel];document.getElementById('rv-i').src='images/christmas/'+b.i+'.jpg';document.getElementById('rv-k').textContent=b.k;document.getElementById('rv-t').textContent=b.t;
      document.getElementById('rv-d').innerHTML='<dt>Boxes</dt><dd>'+(+document.getElementById('bq').value||1)+'</dd><dt>Branding</dt><dd>'+(document.getElementById('bb').checked?'Custom branding':'None')+'</dd><dt>Card</dt><dd>'+(JW.esc(document.getElementById('bn').value)||'Standard welcome card')+'</dd>'}}
  function choose(i){sel=i;[].forEach.call(pick.children,function(c,j){c.classList.toggle('on',j===i)});var n=document.getElementById('n1');n.disabled=false;n.style.opacity=1}
  pick.addEventListener('click',function(e){var c=e.target.closest('.pk');if(c)choose(+c.dataset.i)});
  document.getElementById('n1').onclick=function(){go(2)};
  document.querySelectorAll('[data-go]').forEach(function(b){b.onclick=function(){go(+b.dataset.go)}});
  var q=document.getElementById('bq');document.getElementById('bm').onclick=function(){q.value=Math.max(1,+q.value-1)};document.getElementById('bp').onclick=function(){q.value=+q.value+1};
  document.getElementById('fin').onclick=function(){JW.add({id:sel,qty:Math.max(1,+q.value||1),brand:document.getElementById('bb').checked,note:document.getElementById('bn').value.trim()});location.href='cart.html'};
  if(pre>=0&&pre<BOXES.length)choose(pre);
  if(window.IntersectionObserver){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1});pick.querySelectorAll('.rv').forEach(function(x){io.observe(x)})}else pick.querySelectorAll('.rv').forEach(function(x){x.classList.add('in')});
})();
</script>
'''
page('build.html','Customize Your Gift — Julia Wisteria','build',build,build_js)

# ---------- CART ----------
def small_hero(script, title, crumb):
    return '''<section class="ph" style="padding-bottom:30px">
  <div class="x-hero-bg"><div class="blob b1"></div><div class="blob b2"></div><div class="grain"></div></div>
  <div class="crumbs rv"><a href="julia-wisteria.html">Home</a> &nbsp;/&nbsp; %s</div>
  <span class="x-script rv">%s</span>
  <h1 class="x-h1 split">%s</h1>
</section>
''' % (crumb, script, title)

cart = small_hero('Your selection', 'Cart', 'Cart') + '''<div class="wrap">
  <div class="empty x-hide" id="em"><p>Your cart is empty. Choose a box to get started.</p><a href="shop.html" class="btn-x solid">Browse the boxes <span class="ar">→</span></a></div>
  <div class="cart2 x-hide" id="full">
    <div class="qlist" id="ql" style="padding:0"></div>
    <aside class="tot rv">
      <h3>Cart totals</h3>
      <div class="tot-r"><span>Subtotal</span><b id="st"></b></div>
      <div class="tot-r"><span>Shipping</span><span>Calculated at checkout</span></div>
      <div class="tot-r big"><span>Total</span><span id="tt"></span></div>
      <div id="xp" style="margin-top:18px"></div>
      <a href="checkout.html" class="btn-x solid">Proceed to checkout <span class="ar">→</span></a>
      <small>Ordering 25+ boxes? <a href="corporate.html#quote" style="color:var(--wine);text-decoration:underline">Request a corporate quote</a></small>
    </aside>
  </div>
</div>
'''
cart_js = '''<script>
(function(){
  var ql=document.getElementById('ql');
  function draw(){var l=JW.get();document.getElementById('em').classList.toggle('x-hide',l.length>0);document.getElementById('full').classList.toggle('x-hide',!l.length);
    ql.innerHTML=l.map(function(x,n){var b=BOXES[x.id];return '<div class="qi"><img src="images/christmas/'+b.i+'.jpg" alt=""><div><h3>'+JW.esc(b.t)+'</h3><span class="lp">'+JW.money(b.price*x.qty)+'</span><small>'+JW.money(b.price)+' each'+(x.brand?' · Custom branding':'')+(x.note?' · “'+JW.esc(x.note)+'”':'')+'</small><button class="rm" data-rm="'+n+'">Remove</button></div><div class="stepper"><button data-d="-1" data-n="'+n+'">−</button><input value="'+x.qty+'" data-q="'+n+'" type="number" min="1" aria-label="Quantity"><button data-d="1" data-n="'+n+'">+</button></div></div>'}).join('');
    document.getElementById('st').textContent=JW.money(JW.subtotal());document.getElementById('tt').textContent=JW.money(JW.subtotal());JW.badge()}
  ql.addEventListener('click',function(e){var l=JW.get(),d=e.target.closest('[data-d]'),r=e.target.closest('[data-rm]');
    if(d){var n=+d.dataset.n;l[n].qty=Math.max(1,l[n].qty+ +d.dataset.d);JW.set(l);draw()}
    if(r){var n2=+r.dataset.rm,row=r.closest('.qi');row.classList.add('gone');setTimeout(function(){l.splice(n2,1);JW.set(l);draw()},420)}});
  ql.addEventListener('change',function(e){var i=e.target.dataset.q;if(i==null)return;var l=JW.get();l[+i].qty=Math.max(1,+e.target.value||1);JW.set(l);draw()});
  JW.express(document.getElementById('xp'),JW.subtotal);
  draw();
})();
</script>
'''
page('cart.html','Cart — Julia Wisteria','',cart,cart_js)

# ---------- CHECKOUT (demo: en WordPress lo procesa Stripe) ----------
STATES = ['Florida','Alabama','Arizona','California','Colorado','Georgia','Illinois','Massachusetts','Michigan','Nevada','New Jersey','New York','North Carolina','Ohio','Pennsylvania','South Carolina','Tennessee','Texas','Virginia','Washington','Other']
checkout = small_hero('Almost there', 'Checkout', 'Checkout') + '''<div class="wrap">
  <p class="demo-note rv">Demo checkout for presentation — no payment is processed. In the live store, payments run through Stripe (Apple Pay, Google Pay, cards and ACH).</p>
  <div class="empty x-hide" id="em"><p>Your cart is empty.</p><a href="shop.html" class="btn-x solid">Browse the boxes <span class="ar">→</span></a></div>
  <form class="co" id="co">
    <div>
      <div class="co-s rv"><h3>Express checkout</h3><div id="xp"></div></div>
      <div class="co-s rv">
        <h3>Contact &amp; delivery</h3>
        <div class="co-g">
          <div><label>First name</label><input class="field" required></div>
          <div><label>Last name</label><input class="field" required></div>
          <div class="full"><label>Company (optional)</label><input class="field"></div>
          <div><label>Email</label><input class="field" type="email" required></div>
          <div><label>Phone</label><input class="field" type="tel"></div>
          <div class="full"><label>Street address</label><input class="field" required placeholder="House number and street name"></div>
          <div><label>City</label><input class="field" required></div>
          <div><label>State</label><select class="field">%s</select></div>
          <div><label>ZIP code</label><input class="field" required inputmode="numeric"></div>
          <div><label>Needed by</label><input class="field" type="date"></div>
          <div class="full"><label>Order notes (optional)</label><textarea class="field" rows="3" placeholder="Gift message, delivery instructions…"></textarea></div>
        </div>
      </div>
      <div class="co-s rv">
        <h3>Payment</h3>
        <label class="pm"><span><input type="radio" name="pm" value="card" checked> Credit / Debit card <em>VISA · MC · AMEX</em></span>
          <div class="pm-b co-g"><div class="full"><label>Card number</label><input class="field" placeholder="4242 4242 4242 4242 (demo — do not use a real card)" autocomplete="off"></div><div><label>Expiry</label><input class="field" placeholder="MM / YY" autocomplete="off"></div><div><label>CVC</label><input class="field" placeholder="123" autocomplete="off"></div></div></label>
        <label class="pm"><span><input type="radio" name="pm" value="ach"> ACH Direct Debit <em>US bank account</em></span>
          <div class="pm-b"><p>Pay directly from your bank account. You will connect your bank securely through Stripe — ideal for large corporate orders.</p></div></label>
        <label class="pm"><span><input type="radio" name="pm" value="wire"> Wire transfer <em>Corporate orders</em></span>
          <div class="pm-b"><p>We will email our bank details. Your order ships once funds clear.</p></div></label>
      </div>
    </div>
    <aside class="tot rv">
      <h3>Your order</h3>
      <div id="sum"></div>
      <div class="tot-r"><span>Shipping</span><span>Free delivery in Orlando, FL</span></div>
      <div class="tot-r big"><span>Total</span><span id="tt"></span></div>
      <label style="display:flex;gap:10px;align-items:flex-start;font-size:13px;margin:14px 0 6px;cursor:pointer"><input type="checkbox" required style="accent-color:var(--wine);margin-top:3px"> I have read and agree to the terms and conditions</label>
      <button type="submit" class="btn-x solid">Place order <span class="ar">→</span></button>
      <small>Secure payments powered by Stripe</small>
    </aside>
  </form>
  <div class="co-ok" id="ok"><span class="x-script">Thank you</span><h2 class="sec-h">Your order is confirmed.</h2><p style="color:var(--muted);margin-bottom:8px" id="okmsg"></p><p style="color:var(--muted);margin-bottom:28px">Demo — no payment was processed.</p><a href="julia-wisteria.html" class="btn-x solid">Back to home <span class="ar">→</span></a></div>
</div>
''' % ''.join('<option>%s</option>' % s for s in STATES)
checkout_js = '''<script>
(function(){
  var f=document.getElementById('co');
  function done(how){var n='JW-'+(1000+Math.floor(Math.random()*9000));
    document.getElementById('okmsg').textContent='Order '+n+' · '+JW.money(JW.subtotal())+' · paid with '+how+'.';
    f.style.display='none';document.querySelector('.demo-note').style.display='none';document.getElementById('ok').classList.add('on');JW.set([]);scrollTo({top:0,behavior:'smooth'})}
  var paid=new URLSearchParams(location.search).get('paid');
  if(!JW.get().length&&!paid){f.style.display='none';document.getElementById('em').classList.remove('x-hide');return}
  document.getElementById('sum').innerHTML=JW.get().map(function(x){var b=BOXES[x.id];return '<div class="tot-r"><span>'+JW.esc(b.t)+' × '+x.qty+'</span><b>'+JW.money(b.price*x.qty)+'</b></div>'}).join('');
  document.getElementById('tt').textContent=JW.money(JW.subtotal());
  JW.express(document.getElementById('xp'),JW.subtotal,done);
  if(paid){done(paid);return}
  f.addEventListener('submit',function(e){e.preventDefault();var m=f.querySelector('input[name=pm]:checked').value;done({card:'card',ach:'ACH Direct Debit',wire:'wire transfer'}[m])});
})();
</script>
'''
page('checkout.html','Checkout — Julia Wisteria','',checkout,checkout_js)

# ---------- CORPORATE ----------
corp='''<section class="ph">
  <div class="x-hero-bg"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="grain"></div></div>
  <div class="crumbs rv"><a href="julia-wisteria.html">Home</a> &nbsp;/&nbsp; Corporate</div>
  <span class="x-script rv">For businesses</span>
  <h1 class="x-h1 split">Corporate gifting, crafted with <em>meaning</em></h1>
  <p class="x-lead rv" style="--d:.4s">Curated artisan gifts for corporate events, VIP experiences, employee recognition, incentive travel and destination programs.</p>
  <div class="x-cta rv" style="--d:.55s;justify-content:center;margin-top:34px"><a href="#quote" class="btn-x solid">Request a quote <span class="ar">→</span></a><a href="shop.html" class="btn-x">See the boxes</a></div>
</section>
<div class="wrap"><div class="occg">
  <div class="oc rv"><b>01</b><h3>Corporate events</h3></div><div class="oc rv" style="--d:.08s"><b>02</b><h3>VIP experiences</h3></div><div class="oc rv" style="--d:.16s"><b>03</b><h3>Employee recognition</h3></div><div class="oc rv" style="--d:.24s"><b>04</b><h3>Incentive travel</h3></div><div class="oc rv" style="--d:.32s"><b>05</b><h3>Destination programs</h3></div>
</div></div>
<section class="symb" style="margin-top:100px"><div class="symb-in">
  <div class="sh" style="text-align:left;max-width:760px"><span class="sh-eye rv" style="text-align:left">Simple process</span><h2 class="sh-h2 split" style="text-align:left">Three steps to a gift that tells a story</h2></div>
  <div class="proc">
    <div class="pr rv"><b>01</b><h3>Consult</h3><p>Tell us your vision, occasion and group size. We help you choose the right box and the right personal touches.</p></div>
    <div class="pr rv" style="--d:.1s"><b>02</b><h3>Curate</h3><p>We assemble each box with products made with love, creativity and craftsmanship — locally made whenever possible.</p></div>
    <div class="pr rv" style="--d:.2s"><b>03</b><h3>Deliver</h3><p>Luxury packaging, a personalized card and optional custom branding, ready to make every recipient feel remembered.</p></div>
  </div>
</div></section>
<section class="qsec" id="quote">
  <div class="sh"><span class="sh-eye rv">Let's create something beautiful</span><h2 class="sh-h2 split">Request a custom quote</h2><p class="sh-p rv">Tell us about your gifting vision and we'll be in touch</p></div>
  <div class="ok" id="ok"><span class="x-script">Thank you</span><h3 class="sec-h">We received your request.</h3><p style="color:var(--muted)">Our team will get back to you very soon.</p></div>
  <form class="qform" id="qf">
    <div class="qsel" id="qsel"></div>
    <div><label>First name</label><input required placeholder="Julia"></div>
    <div><label>Last name</label><input required placeholder="Smith"></div>
    <div class="full"><label>Company</label><input placeholder="Your Company, LLC"></div>
    <div><label>Email</label><input type="email" required placeholder="julia@yourcompany.com"></div>
    <div><label>Phone</label><input type="tel" placeholder="(407) 000-0000"></div>
    <div><label>Event / occasion</label><select><option>Corporate event</option><option>VIP experience</option><option>Employee recognition</option><option>Incentive travel</option><option>Destination program</option><option>Other</option></select></div>
    <div><label>Needed by</label><input type="date"></div>
    <div class="full"><label>Message</label><textarea rows="5" placeholder="Tell us about your brand, timeline or special requests…"></textarea></div>
    <div class="full"><button type="submit" class="btn-x solid">Send request <span class="ar">→</span></button></div>
  </form>
</section>
'''
corp_js='''<script>
(function(){
  var l=JW.get(),el=document.getElementById('qsel');
  var pre=new URLSearchParams(location.search).get('box');
  if(pre!==null&&BOXES[+pre]&&!l.length)l=[{id:+pre,qty:10,brand:false,note:''}];
  el.innerHTML=l.length?'<b>Boxes in your request:</b><br>'+l.map(function(x){return '• '+JW.esc(BOXES[x.id].t)+' × '+x.qty+(x.brand?' (custom branding)':'')}).join('<br>')+'<br><a href="cart.html">Edit cart</a>':'<b>No boxes selected yet.</b> <a href="shop.html">Browse the five Christmas boxes</a> or just tell us what you need below.';
  document.getElementById('qf').addEventListener('submit',function(e){e.preventDefault();this.style.display='none';document.querySelector('.qsec .sh').style.display='none';document.getElementById('ok').classList.add('on')});
})();
</script>
'''
page('corporate.html','Corporate Gifting — Julia Wisteria','corp',corp,corp_js)
print('built')
