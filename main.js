(()=>{const $=(s,c=document)=>c.querySelector(s),$$=(s,c=document)=>[...c.querySelectorAll(s)];
const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
const bg=$('#burger'),nav=$('#nav');
bg.addEventListener('click',()=>bg.setAttribute('aria-expanded',nav.classList.toggle('open')));
const hd=$('.hdr');addEventListener('scroll',()=>hd.classList.toggle('sc',scrollY>20),{passive:true});
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
$$('.rv').forEach(e=>io.observe(e));
const co=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;co.unobserve(e.target);const el=e.target,t=+el.dataset.count,s=el.dataset.suf||'';let n=0;const st=()=>{n+=t/70;if(n>=t){el.textContent=t+s;return}el.textContent=Math.floor(n)+s;requestAnimationFrame(st)};rm?el.textContent=t+s:st()}));
$$('[data-count]').forEach(e=>co.observe(e));
if(!rm){$$('.tilt').forEach(el=>{el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;el.style.setProperty('--ty',x*12+'deg');el.style.setProperty('--tx',-y*12+'deg')});el.addEventListener('pointerleave',()=>{el.style.setProperty('--ty','0deg');el.style.setProperty('--tx','0deg')})});
const sc=$('.stage');if(sc)addEventListener('pointermove',e=>{sc.style.setProperty('--ry',(e.clientX/innerWidth-.5)*28+'deg');sc.style.setProperty('--rx',8-(e.clientY/innerHeight-.5)*22+'deg')});
const px=$$('[data-d]');if(px.length)addEventListener('scroll',()=>px.forEach(e=>e.style.translate='0 '+scrollY*e.dataset.d+'px'),{passive:true})}
$$('[role=tablist]').forEach(l=>{const tb=$$('[role=tab]',l),go=t=>{tb.forEach(x=>{const on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;$('#'+x.getAttribute('aria-controls')).hidden=!on});t.focus()};
tb.forEach((t,i)=>{t.addEventListener('click',()=>go(t));t.addEventListener('keydown',e=>{const k={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[e.key];if(k){e.preventDefault();go(tb[(i+k+tb.length)%tb.length])}})})});
const tr=$('.track');if(tr){const mv=d=>tr.scrollBy({left:d*(tr.firstElementChild.offsetWidth+20),behavior:'smooth'});$('#prev').onclick=()=>mv(-1);$('#next').onclick=()=>mv(1);
const t=rm?0:setInterval(()=>tr.scrollLeft+tr.clientWidth>=tr.scrollWidth-4?tr.scrollTo({left:0,behavior:'smooth'}):mv(1),5000);tr.addEventListener('pointerenter',()=>clearInterval(t))}
const K='ljcart',dr=$('#cart'),ov=$('#ov');let cart=[];try{cart=JSON.parse(localStorage.getItem(K))||[]}catch(e){}
const op=o=>{dr.classList.toggle('open',o);ov.classList.toggle('open',o);dr.setAttribute('aria-hidden',!o);if(o)$('#cx').focus()};
function rd(){try{localStorage.setItem(K,JSON.stringify(cart))}catch(e){}
$('#cc').textContent=cart.reduce((a,i)=>a+i.q,0);$('#ct').textContent='$'+cart.reduce((a,i)=>a+i.p*i.q,0).toFixed(2);
$('#cl').innerHTML=cart.length?cart.map(i=>`<div class="ci"><div><b>${i.n}</b><div class="q"><button data-a="-" data-id="${i.id}" aria-label="Decrease quantity">−</button><span>${i.q}</span><button data-a="+" data-id="${i.id}" aria-label="Increase quantity">+</button></div></div><b>$${(i.p*i.q).toFixed(2)}</b></div>`).join(''):'<p>Your cart is empty.</p>'}
$('#cb').onclick=()=>op(true);$('#cx').onclick=ov.onclick=()=>op(false);addEventListener('keydown',e=>e.key==='Escape'&&op(false));
$('#cl').addEventListener('click',e=>{const b=e.target.closest('[data-a]');if(!b)return;const i=cart.find(x=>x.id===b.dataset.id);i.q+=b.dataset.a==='+'?1:-1;cart=cart.filter(x=>x.q>0);rd()});
$$('[data-add]').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.add,i=cart.find(x=>x.id===id);i?i.q++:cart.push({id,n:b.dataset.n,p:+b.dataset.p,q:1});rd();op(true)}));
$('#cr').onclick=()=>{cart=[];rd()};
$('#co').onclick=()=>{if(!cart.length)return;const body=cart.map(i=>`${i.q} x ${i.n} - $${(i.p*i.q).toFixed(2)}`).join('\n')+'\nTotal: '+$('#ct').textContent;location.href='mailto:info@ljbrowsstudio.com.au?subject='+encodeURIComponent('Shop order')+'&body='+encodeURIComponent(body)};
rd();
const f=$('#cf');if(f)f.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(f);location.href='mailto:info@ljbrowsstudio.com.au?subject='+encodeURIComponent('Message from '+d.get('name'))+'&body='+encodeURIComponent(d.get('message')+'\n\n'+d.get('name')+' - '+d.get('email'))});
})();
