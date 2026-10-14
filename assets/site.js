/* Julia Wisteria — shared data + helpers */
window.BOXES=[
 {i:'coffee-planning',cat:'Corporate',k:'Corporate',t:'The Coffee & Planning Gift Box',s:'Fresh starts, productive mornings, inspired plans.',
  d:'A thoughtful gift designed for fresh starts, productive mornings, and inspired plans. It pairs premium specialty coffee with an artisan ceramic mug, an elegant gold coffee scoop, and a 2027 dated planner — a beautiful daily ritual for planning goals while enjoying a favorite cup of coffee. Complete with mini sticky notes and a personalized welcome card, this elevated collection is ideal for employee appreciation, client gifting, executive gifts, onboarding, welcome programs, and New Year celebrations.',
  inc:['Premium specialty coffee','Artisan ceramic mug','Gold coffee scoop','2027 Dated Planner – classic, simple, and playful, designed to keep you organized and inspired all year','Mini sticky notes','Pens','Personalized welcome card','Luxury gift box packaging','Optional custom branding'],q:'Plan the year. Enjoy the moment. Start with great coffee.'},
 {i:'unwind-recharge',cat:'Wellness',k:'Wellness Gift Collection',t:'Unwind & Recharge Box',s:'A restorative moment of self-care.',
  d:'A thoughtful invitation to slow down, breathe, and enjoy a restorative moment of self-care. It combines artisan body-care essentials with calming organic tea and an aromatherapy shower steamer. Rose & lime soap, grapefruit lip balm, nourishing hand cream, and the soothing notes of lavender, chamomile, and cedar create a comforting ritual for both body and mind. Perfect for wellness programs, executive retreats, employee appreciation, conference speakers, VIP guests, and thoughtful client gifting.',
  inc:['Artisan Rose & Lime Soap','Natural Grapefruit Lip Balm','Luxury Hand Cream','Meditative Mind organic tea','Peace Shower Steamer – a steam-activated aromatherapy blend of organic lavender, chamomile, and cedar essential oils designed to promote relaxation and tranquility','Towel','Personalized welcome card','Luxury gift box packaging'],q:'Sip. Breathe. Recharge.'},
 {i:'teatime-delight',cat:'Tea',k:'Tea, Honey & Mug Gift Experience',t:'Teatime Delight Box',s:'Tea, honey, candlelight — and a moment to unwind.',
  d:'A cozy gift created for slow, comforting moments. The Teatime Delight Box pairs a premium tea selection with artisan honey and a signature ceramic mug, while a Blooming Lilacs candle adds a soft floral touch to the experience. Together, these pieces create a warm ritual to sip, unwind, and enjoy. Perfect for conference speakers, VIP guests, executive retreats, wellness programs, hotel arrivals, employee appreciation, and client gifting.',
  inc:['Premium tea selection','Artisan honey jar','Honey dipper','Signature ceramic mug','Blooming Lilacs candle','Personalized welcome card','Luxury gift packaging'],q:'Tea, honey, candlelight — and a moment to unwind.'},
 {i:'light-up-your-day',cat:'Desk',k:'Candle, Planner & Desk Gift Experience',t:'Light Up Your Day Box',s:'Inspiration, greenery, and a little sweetness.',
  d:'Brighten the day with a gift that blends inspiration, greenery, and a little sweetness. It combines a hand-poured artisan candle with a mini succulent, a 2027 dated planner, and bear gummies — a cheerful collection for the desk, home, or office. Thoughtful and practical, this box is perfect for employee appreciation, client thank-yous, onboarding, New Year gifting, speakers, and corporate celebrations.',
  inc:['Hand-poured artisan candle','Mini succulent','2027 Dated Planner – classic, simple, and playful, designed to keep you organized and inspired all year','Gummy bears','Premium gift box packaging','Personalized message card'],q:'Light the candle. Make a plan. Grow something beautiful.'},
 {i:'serenity-sleep',cat:'Rest',k:'Relaxation & Rest Wellness Gift Box',t:'Serenity Sleep Box',s:'A calming end-of-day ritual.',
  d:'Create a calming end-of-day ritual. Thoughtfully curated for rest and relaxation, this collection combines a therapeutic eye mask, lavender body scrub, botanical body oil, natural lip balm, organic tea, and a playful beaded daisy keychain. From soothing body care to a comforting cup of tea, every element is selected to encourage the recipient to slow down, recharge, and enjoy a well-deserved moment of calm. Perfect for wellness programs, VIP guests, employee appreciation, retreats, speakers, and holiday gifting.',
  inc:['Beaded Daisy Keychain','Meditative Mind organic tea','Therapeutic Eye Mask','Lavender Body Scrub','Relaxing Botanical Body Oil','Natural Lip Balm','Personalized gift card'],q:'Rest. Relax. Recharge.'}
];
window.JW=(function(){
  var K='jw_quote';
  function get(){try{return JSON.parse(localStorage.getItem(K))||[]}catch(e){return[]}}
  function set(v){try{localStorage.setItem(K,JSON.stringify(v))}catch(e){}badge()}
  function badge(){var n=get().reduce(function(a,x){return a+x.qty},0),b=document.getElementById('qbadge');if(b){b.textContent=n;b.style.display=n?'flex':'none'}}
  function add(item){var l=get(),f=l.filter(function(x){return x.id===item.id&&x.brand===item.brand&&x.note===item.note})[0];if(f)f.qty+=item.qty;else l.push(item);set(l)}
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')}
  document.addEventListener('DOMContentLoaded',badge);
  return {get:get,set:set,add:add,badge:badge,esc:esc};
})();
(function(){
  var ham=document.getElementById('ham'),mn=document.getElementById('mob-nav'),mc=document.getElementById('mob-close');
  window.openMobNav=function(){ham.classList.add('open');mn.classList.add('open');document.body.style.overflow='hidden'};
  window.closeMobNav=function(){ham.classList.remove('open');mn.classList.remove('open');document.body.style.overflow=''};
  if(ham){ham.addEventListener('click',function(){ham.classList.contains('open')?closeMobNav():openMobNav()});mc.addEventListener('click',closeMobNav)}
})();
