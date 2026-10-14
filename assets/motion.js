/* Julia Wisteria — motion layer */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var $ = function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};

  // split headings into words for masked reveal
  $('.split').forEach(function(el){
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
        } else if(n.nodeType===1 && n.tagName!=='BR'){ walk(n); }
      });
    })(el);
  });

  // reveal on scroll
  var targets = $('.rv,.split,.wist');
  if('IntersectionObserver' in window && !reduce){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)} });
    },{threshold:.15,rootMargin:'0px 0px -6% 0px'});
    targets.forEach(function(t){io.observe(t)});
  } else targets.forEach(function(t){t.classList.add('in')});

  if(reduce) return;

  // scroll progress + parallax
  var bar=document.querySelector('.progress'), par=$('[data-par]');
  var ticking=false;
  function onScroll(){
    if(ticking) return; ticking=true;
    requestAnimationFrame(function(){
      var h=document.documentElement.scrollHeight-innerHeight;
      if(bar) bar.style.transform='scaleX('+(h>0?scrollY/h:0)+')';
      par.forEach(function(el){
        var r=el.getBoundingClientRect();
        if(r.bottom<0||r.top>innerHeight) return;
        var k=parseFloat(el.dataset.par)||.1;
        el.style.setProperty('--py',((r.top+r.height/2-innerHeight/2)*k*-1).toFixed(1)+'px');
        el.style.transform='translate3d(0,'+((r.top+r.height/2-innerHeight/2)*k*-1).toFixed(1)+'px,0)';
      });
      ticking=false;
    });
  }
  addEventListener('scroll',onScroll,{passive:true});onScroll();

  // falling petals (wisteria / soft snow)
  var fall=document.querySelector('.fall');
  if(fall){
    var cols=['#D4B4B5','#B9A6D3','#fff','#E6DDF2','#E8C9CB'];
    for(var i=0;i<22;i++){
      var p=document.createElement('span');
      p.style.cssText='left:'+(Math.random()*100)+'%;--s:'+(6+Math.random()*9)+'px;--c:'+cols[i%cols.length]+';--t:'+(14+Math.random()*16)+'s;--dl:-'+(Math.random()*24)+'s;--x:'+((Math.random()-.5)*220)+'px';
      fall.appendChild(p);
    }
  }

  // cursor glow
  var g=document.querySelector('.glow');
  if(g && matchMedia('(pointer:fine)').matches){
    addEventListener('pointermove',function(e){g.style.left=e.clientX+'px';g.style.top=e.clientY+'px'},{passive:true});
  }

  // 3D tilt + magnetic buttons
  if(matchMedia('(pointer:fine)').matches){
    $('.tilt').forEach(function(el){
      el.addEventListener('pointermove',function(e){
        var r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
        el.style.transform='perspective(900px) rotateY('+(x*7)+'deg) rotateX('+(-y*7)+'deg) translateZ(0)';
      });
      el.addEventListener('pointerleave',function(){el.style.transform=''});
    });
    $('.btn-x').forEach(function(b){
      b.addEventListener('pointermove',function(e){
        var r=b.getBoundingClientRect();
        b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.18)+'px,'+((e.clientY-r.top-r.height/2)*.28)+'px)';
      });
      b.addEventListener('pointerleave',function(){b.style.transform=''});
    });
  }
})();
