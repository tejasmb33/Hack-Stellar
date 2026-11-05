import * as THREE from './vendor/three.module.js';

// One persistent, real-time 3D scene. Text, logos and controls remain ordinary HTML.
const canvas = document.querySelector('#universe-canvas');
const quiet = document.body.classList.contains('directory');
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const compact = matchMedia('(max-width: 760px)').matches;
const constrained = compact || (navigator.deviceMemory && navigator.deviceMemory < 4) || navigator.connection?.saveData;
let renderer;
try {
  renderer = new THREE.WebGLRenderer({canvas, antialias: !constrained, alpha: true, powerPreference: 'low-power'});
} catch {
  document.body.classList.add('scene-unavailable');
}
if (renderer) init();

function init() {
  renderer.setPixelRatio(Math.min(devicePixelRatio, constrained ? 1.25 : 1.7));
  renderer.setSize(innerWidth, innerHeight);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(43, innerWidth / innerHeight, .1, 260);
  camera.position.set(0, 0, 6);
  scene.add(new THREE.AmbientLight(0x9abde6, .23));
  const sun = new THREE.DirectionalLight(0xd7eaff, 2.4);
  sun.position.set(5, 8, 7);
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x2461a6, .32);
  fill.position.set(-7, 2, -5);scene.add(fill);
  const loader = new THREE.TextureLoader();
  const day = loader.load(constrained ? '/assets/earth-day-mobile.jpg' : '/assets/earth-day-4k.jpg', () => drawStatic());
  day.colorSpace = THREE.SRGBColorSpace;
  day.anisotropy = Math.min(renderer.capabilities.getMaxAnisotropy(), 4);
  const normal = loader.load('/assets/earth-normal.jpg', () => drawStatic());
  const cloudTexture = loader.load('/assets/earth-clouds.png', () => drawStatic());
  const earthGroup = new THREE.Group();
  earthGroup.position.set(0, -20.8, 0);
  earthGroup.rotation.z = -.12;
  scene.add(earthGroup);
  const sphere = new THREE.SphereGeometry(20, constrained ? 64 : 112, constrained ? 48 : 80);
  const earth = new THREE.Mesh(sphere, new THREE.MeshStandardMaterial({map: day, normalMap: normal, normalScale: new THREE.Vector2(.16,.16), roughness:.9, metalness:.02}));
  earth.rotation.x = .5;earth.rotation.y = 3.3;earthGroup.add(earth);
  const clouds = new THREE.Mesh(new THREE.SphereGeometry(20.065,64,48),new THREE.MeshStandardMaterial({map:cloudTexture,alphaMap:cloudTexture,transparent:true,opacity:.32,depthWrite:false,roughness:1}));
  clouds.rotation.x=earth.rotation.x;clouds.rotation.y=earth.rotation.y;earthGroup.add(clouds);
  const atmosphere = new THREE.Mesh(new THREE.SphereGeometry(20.11,80,56), new THREE.ShaderMaterial({
    transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
    uniforms:{uSun:{value:new THREE.Vector3(5,8,7).normalize()}},
    vertexShader:`varying vec3 vNormal;varying vec3 vWorld;void main(){vec4 world=modelMatrix*vec4(position,1.);vWorld=world.xyz;vNormal=normalize(mat3(modelMatrix)*normal);gl_Position=projectionMatrix*viewMatrix*world;}`,
    fragmentShader:`varying vec3 vNormal;varying vec3 vWorld;uniform vec3 uSun;void main(){vec3 n=normalize(vNormal);vec3 eye=normalize(cameraPosition-vWorld);float edge=pow(1.-max(dot(n,eye),0.),5.0);float light=.3+.7*max(dot(n,uSun),0.);vec3 blue=mix(vec3(.035,.22,.55),vec3(.32,.72,1.),edge);gl_FragColor=vec4(blue,edge*light*.75);}`
  }));
  earthGroup.add(atmosphere);

  // Seeded spatial distribution makes the scene reproducible and avoids layout randomness.
  let seed=84;
  function random(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}
  const starCount=constrained?650:1500;
  const positions=new Float32Array(starCount*3), sizes=new Float32Array(starCount), phases=new Float32Array(starCount);
  for(let i=0;i<starCount;i++){positions[i*3]=(random()-.5)*170;positions[i*3+1]=(random()-.5)*120;positions[i*3+2]=-15-random()*170;sizes[i]=.7+random()*1.8;phases[i]=random()*6.28;}
  const starsGeometry=new THREE.BufferGeometry();starsGeometry.setAttribute('position',new THREE.BufferAttribute(positions,3));starsGeometry.setAttribute('aSize',new THREE.BufferAttribute(sizes,1));starsGeometry.setAttribute('aPhase',new THREE.BufferAttribute(phases,1));
  const starsMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,uniforms:{uTime:{value:0},uPixel:{value:renderer.getPixelRatio()}},
    vertexShader:`attribute float aSize;attribute float aPhase;varying float vAlpha;uniform float uTime;uniform float uPixel;void main(){vec4 mv=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*mv;gl_PointSize=clamp(aSize*65./-mv.z, .6, 2.5)*uPixel;vAlpha=.4+.13*sin(uTime*.2+aPhase);}`,
    fragmentShader:`varying float vAlpha;void main(){float d=length(gl_PointCoord-.5);float a=smoothstep(.5,.02,d);gl_FragColor=vec4(.63,.79,1.,a*vAlpha);}`});
  const stars=new THREE.Points(starsGeometry,starsMaterial);scene.add(stars);

  const orbit=new THREE.Group();orbit.position.set(0,-1,-7);orbit.rotation.set(1.05,.25,-.4);scene.add(orbit);
  const ringMaterials=[];
  for(let i=0;i<3;i++){
    const material=new THREE.MeshBasicMaterial({color:i===1?0x83d3ff:0x326a9b,transparent:true,opacity:0,depthWrite:false,blending:THREE.AdditiveBlending});
    ringMaterials.push(material);
    const ring=new THREE.Mesh(new THREE.TorusGeometry(7.3+i*.17,i===1?.012:.028,8,constrained?160:300),material);ring.rotation.x=i*.045;orbit.add(ring);
  }
  const dustCount=constrained?220:650;
  const dustPos=new Float32Array(dustCount*3);
  for(let i=0;i<dustCount;i++){const a=random()*Math.PI*2,r=6.5+random()*2;dustPos[i*3]=Math.cos(a)*r;dustPos[i*3+1]=Math.sin(a)*r;dustPos[i*3+2]=(random()-.5)*.9;}
  const dustGeometry=new THREE.BufferGeometry();dustGeometry.setAttribute('position',new THREE.BufferAttribute(dustPos,3));
  const dustMaterial=new THREE.PointsMaterial({color:0x79bce9,size:.022,transparent:true,opacity:0,depthWrite:false,blending:THREE.AdditiveBlending});
  const dust=new THREE.Points(dustGeometry,dustMaterial);orbit.add(dust);

  // An unobtrusive nested-cube detail, discoverable within the orbital field.
  const lattice=new THREE.Group();lattice.position.set(6.3,2.5,-10);
  const latticeMaterial=new THREE.LineBasicMaterial({color:0x80b5dc,transparent:true,opacity:0});
  for(const size of [.7,1.4])lattice.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(size,size,size)),latticeMaterial));
  const links=[];
  for(const x of [-1,1])for(const y of [-1,1])for(const z of [-1,1])links.push(x*.35,y*.35,z*.35,x*.7,y*.7,z*.7);
  const linkGeometry=new THREE.BufferGeometry();linkGeometry.setAttribute('position',new THREE.Float32BufferAttribute(links,3));lattice.add(new THREE.LineSegments(linkGeometry,latticeMaterial));scene.add(lattice);

  let elapsed=0,lastTime=0,lastFrame=0,scroll=0,targetScroll=0,paused=false;
  const clock={frames:0,earthRotation:earth.rotation.y,cloudRotation:clouds.rotation.y,mode:constrained?'balanced':'full',webgl:true,paused:false};
  window.__cosmos=clock;
  function scenePosition(){
    const h=innerHeight;
    const hero=document.querySelector('#hero');
    const heroEnd=hero?hero.offsetTop+hero.offsetHeight:h;
    const progress=Math.max(0,scroll/heroEnd);
    earthGroup.position.y=-20.8-progress*9;
    earthGroup.position.z=-progress*9;
    earthGroup.rotation.z=-.12+progress*.04;
    camera.position.z=6+Math.min(progress,2)*.6;
    camera.position.x=motion.matches?0:Math.sin(elapsed*.035)*.06;
    camera.position.y=motion.matches?0:Math.sin(elapsed*.027)*.025;
    const affiliations=document.querySelector('#affiliations');
    let energy=0;
    if(affiliations){const top=affiliations.offsetTop;const duration=affiliations.offsetHeight;const p=(scroll+h*.55-top)/(duration+h*.4);energy=Math.sin(Math.max(0,Math.min(1,p))*Math.PI);orbit.rotation.x=1.05+p*.24;orbit.rotation.z=-.4+p*.65;orbit.position.y=.5-p*2.6;}
    for(let i=0;i<ringMaterials.length;i++)ringMaterials[i].opacity=energy*(i===1?.33:.08);
    dustMaterial.opacity=energy*.35;
    latticeMaterial.opacity=energy*.1;
    starsMaterial.opacity=1;
    canvas.style.opacity=quiet?'.3':String(Math.max(.18,1-Math.max(0,progress-1.6)*.75));
    earthGroup.visible=!quiet&&progress<2.4;
    orbit.visible=!quiet&&energy>.005;
    lattice.visible=!quiet&&energy>.05;
  }
  function render(time=0){
    if(document.hidden)return;
    if(!motion.matches&&!paused&&time-lastFrame<(constrained?1000/30:1000/48))return;
    const delta=lastTime?Math.min((time-lastTime)/1000,.06):0;
    lastTime=time;lastFrame=time;
    if(!motion.matches&&!paused&&!quiet){elapsed+=delta;earth.rotation.y+=delta*.012;clouds.rotation.y+=delta*.018;dust.rotation.z+=delta*.025;stars.rotation.y+=delta*.0007;lattice.rotation.y+=delta*.05;lattice.rotation.x+=delta*.02;}
    scroll=motion.matches?targetScroll:THREE.MathUtils.lerp(scroll,targetScroll,.13);
    starsMaterial.uniforms.uTime.value=motion.matches?0:elapsed;
    scenePosition();renderer.render(scene,camera);
    clock.frames++;clock.earthRotation=earth.rotation.y;clock.cloudRotation=clouds.rotation.y;clock.paused=motion.matches||paused||quiet;clock.triangles=renderer.info.render.triangles;clock.drawCalls=renderer.info.render.calls;clock.orbitOpacity=ringMaterials[1].opacity;clock.cameraZ=camera.position.z;
  }
  function drawStatic(){requestAnimationFrame(()=>render(performance.now()));}
  function configureLoop(){
    paused=motion.matches||quiet||document.hidden;
    renderer.setAnimationLoop(paused?null:render);
    lastTime=0;drawStatic();
  }
  addEventListener('scroll',()=>{targetScroll=scrollY;if(paused){scroll=targetScroll;drawStatic();}},{passive:true});
  addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);drawStatic();});
  motion.addEventListener('change',configureLoop);
  document.addEventListener('visibilitychange',configureLoop);
  canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();renderer.setAnimationLoop(null);document.body.classList.remove('scene-ready');document.body.classList.add('scene-unavailable');});
  canvas.addEventListener('webglcontextrestored',()=>{document.body.classList.remove('scene-unavailable');document.body.classList.add('scene-ready');configureLoop();});
  addEventListener('pagehide',()=>{renderer.setAnimationLoop(null);});
  addEventListener('pageshow',configureLoop);
  targetScroll=scrollY;scroll=targetScroll;
  scenePosition();renderer.render(scene,camera);
  document.body.classList.add('scene-ready');
  configureLoop();
}
