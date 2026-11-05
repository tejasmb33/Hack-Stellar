'use strict';
(() => {
  const dialog=document.querySelector('.gallery-lightbox');
  const links=[...document.querySelectorAll('[data-gallery-index]')];
  if(!dialog||!links.length||typeof dialog.showModal!=='function')return;
  const image=dialog.querySelector('.lightbox-image');
  const count=dialog.querySelector('.lightbox-count');
  const error=dialog.querySelector('.lightbox-error');
  const close=dialog.querySelector('.lightbox-close');
  let index=0,opener=null,touchStart=null;
  function show(next){
    index=(next+links.length)%links.length;
    error.hidden=true;image.hidden=false;
    image.alt=links[index].querySelector('img').alt;
    image.src=links[index].href;
    count.textContent=`${index+1} / ${links.length}`;
    // Warm the adjacent full photographs without loading the entire gallery.
    for(const offset of [-1,1]){const preload=new Image();preload.src=links[(index+offset+links.length)%links.length].href;}
  }
  links.forEach((link,i)=>link.addEventListener('click',event=>{
    if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
    event.preventDefault();opener=link;show(i);
    document.body.classList.add('gallery-open');dialog.showModal();close.focus();
  }));
  close.addEventListener('click',()=>dialog.close());
  dialog.querySelector('.lightbox-prev').addEventListener('click',()=>show(index-1));
  dialog.querySelector('.lightbox-next').addEventListener('click',()=>show(index+1));
  dialog.addEventListener('keydown',event=>{
    if(event.altKey||event.ctrlKey||event.metaKey)return;
    if(event.key==='Tab'){
      const controls=[...dialog.querySelectorAll('button:not([disabled]),a[href]')];
      const first=controls[0],last=controls.at(-1);
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
    }
    if(event.key==='ArrowRight'){event.preventDefault();show(index+1);}
    if(event.key==='ArrowLeft'){event.preventDefault();show(index-1);}
  });
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
  dialog.addEventListener('close',()=>{document.body.classList.remove('gallery-open');opener?.focus({preventScroll:true});});
  image.addEventListener('error',()=>{image.hidden=true;error.hidden=false;});
  // Horizontal swipes supplement large touch targets; vertical gestures are ignored.
  dialog.querySelector('figure').addEventListener('touchstart',event=>{
    touchStart=event.touches.length===1?{x:event.touches[0].clientX,y:event.touches[0].clientY}:null;
  },{passive:true});
  dialog.querySelector('figure').addEventListener('touchcancel',()=>{touchStart=null;},{passive:true});
  dialog.querySelector('figure').addEventListener('touchend',event=>{
    if(!touchStart||!event.changedTouches.length)return;
    const dx=event.changedTouches[0].clientX-touchStart.x,dy=event.changedTouches[0].clientY-touchStart.y;
    if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.4)show(index+(dx<0?1:-1));
    touchStart=null;
  },{passive:true});
})();
