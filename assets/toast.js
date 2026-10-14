/* Julia Wisteria — avisos emergentes con información real (sin actividad inventada).
   Uso: JWToast.start(items, {first: 9000, every: 22000, show: 7000})
   item: {kicker, title, sub, img, href} */
window.JWToast=(function(){
  var KEY='jw_toast_off', el, timer, hideT, i=0, items=[], opt={};
  function off(){try{return sessionStorage.getItem(KEY)==='1'}catch(e){return false}}
  function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')}
  function build(){
    el=document.createElement('div');el.className='jwt';el.style.position='fixed';el.style.maxWidth='calc(100vw - 32px)';el.setAttribute('role','status');el.setAttribute('aria-live','polite');
    document.body.appendChild(el);
    el.addEventListener('mouseenter',function(){clearTimeout(hideT)});
    el.addEventListener('mouseleave',function(){hideT=setTimeout(hide,2500)});
    el.addEventListener('click',function(e){
      if(e.target.closest('.jwt-x')){e.preventDefault();try{sessionStorage.setItem(KEY,'1')}catch(_){}hide();clearTimeout(timer)}
    });
  }
  function show(){
    if(off()||document.hidden)return next();
    var it=items[i++%items.length];
    el.innerHTML=(it.img?'<img class="jwt-i" src="'+esc(it.img)+'" alt="" width="56" height="56" style="width:56px;height:56px;object-fit:cover">':'<span class="jwt-ic">'+(it.icon||'✦')+'</span>')+
      '<a class="jwt-b" href="'+esc(it.href||'#')+'"><span class="jwt-k">'+esc(it.kicker)+'</span><b class="jwt-t">'+esc(it.title)+'</b>'+(it.sub?'<span class="jwt-s">'+esc(it.sub)+'</span>':'')+'</a>'+
      '<button class="jwt-x" aria-label="Close notifications">✕</button>';
    el.classList.remove('out');void el.offsetWidth;el.classList.add('in');
    hideT=setTimeout(hide,opt.show);next();
  }
  function hide(){if(!el.classList.contains('in'))return;el.classList.remove('in');el.classList.add('out')}
  function next(){clearTimeout(timer);timer=setTimeout(show,opt.every)}
  function daysToChristmas(){var n=new Date(),x=new Date(n.getFullYear(),11,25);return Math.ceil((x-n)/864e5)}
  return {
    daysToChristmas:daysToChristmas,
    start:function(list,o){
      if(off()||!list.length)return;
      opt={first:(o&&o.first)||9000,every:(o&&o.every)||22000,show:(o&&o.show)||7000};
      items=list.slice().sort(function(){return Math.random()-.5});
      build();timer=setTimeout(show,opt.first);
    }
  };
})();
