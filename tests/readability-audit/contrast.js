()=>{
 const parse=s=>{const n=s.match(/[\d.]+/g)?.map(Number);return n&&n.length>=3?[n[0],n[1],n[2],n[3]??1]:[0,0,0,0]};
 const over=(a,b)=>a.slice(0,3).map((v,i)=>v*a[3]+b[i]*(1-a[3]));
 const luminance=c=>{const s=c.slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4});return s[0]*.2126+s[1]*.7152+s[2]*.0722};
 const ratio=(a,b)=>{const l=[luminance(a),luminance(b)].sort((x,y)=>y-x);return (l[0]+.05)/(l[1]+.05)};
 const checks=[];
 function check(e,text,style=getComputedStyle(e)){
  if(!text.trim()||parseFloat(style.fontSize)===0||e.closest('[aria-hidden="true"],.sr-only,script,style,noscript')||!e.getClientRects().length||style.visibility!=='visible')return;
  const ancestors=[];let node=e;while(node&&node!==document.body){ancestors.push(node);node=node.parentElement;}
  let worst=Infinity;
  for(const base of [[255,255,255],[0,0,0]]){
   let bg=base;
   for(const ancestor of ancestors.reverse()){
    const css=getComputedStyle(ancestor);bg=over(parse(css.backgroundColor),bg);
    const stops=css.backgroundImage.match(/rgba?\([^)]*\)/g)||[];
    if(stops.length)bg=stops.map(c=>over(parse(c),bg)).sort((a,b)=>luminance(b)-luminance(a))[0];
   }
   ancestors.reverse();worst=Math.min(worst,ratio(over(parse(style.color),bg),bg));
  }
  const size=parseFloat(style.fontSize),large=size>=24||(size>=18.66&&Number(style.fontWeight)>=700),minimum=large?3:4.5;
  checks.push({tag:e.tagName,cls:typeof e.className==='string'?e.className:'',text:text.trim().slice(0,95),size,contrast:worst,minimum,pass:worst>=minimum});
 }
 const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let node;
 while(node=walker.nextNode())check(node.parentElement,node.textContent);
 document.querySelectorAll('input,select').forEach(e=>check(e,e.tagName==='SELECT'?(e.selectedOptions[0]?.textContent||'Domain'):(e.value||e.placeholder||''),getComputedStyle(e,e.placeholder?'::placeholder':null)));
 return {count:checks.length,failures:checks.filter(c=>!c.pass),small:checks.filter(c=>c.size<12),lowest:checks.sort((a,b)=>a.contrast-b.contrast).slice(0,6)};
}
