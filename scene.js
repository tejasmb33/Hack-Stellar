import * as THREE from './vendor/three.module.js';

// Original 3D gravitational ray tracer. No Earth, image, texture or video background.
const canvas = document.querySelector('#universe-canvas');
const quiet = document.body.classList.contains('directory');
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const constrained = matchMedia('(max-width: 760px)').matches || navigator.connection?.saveData || (navigator.deviceMemory && navigator.deviceMemory < 4);
let renderer;
try { renderer = new THREE.WebGLRenderer({canvas, alpha: true, antialias: false, powerPreference: constrained ? 'low-power' : 'high-performance'}); }
catch { document.body.classList.add('scene-unavailable'); }
if (renderer) createUniverse();

function createUniverse() {
  const pixelRatio = Math.min(devicePixelRatio, constrained ? .85 : 1.15);
  renderer.setPixelRatio(pixelRatio);
  renderer.setSize(innerWidth, innerHeight);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NoToneMapping;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(43, innerWidth / innerHeight, .1, 200);
  const blackHole = new THREE.Group();
  scene.add(blackHole);
  const uniforms = {
    uTime: {value: 0},
    uSize: {value: new THREE.Vector2(innerWidth * pixelRatio, innerHeight * pixelRatio)},
    uCenter: {value: new THREE.Vector2(.5, .82)},
    uCamera: {value: new THREE.Vector3(0, .8, 14)},
    uForward: {value: new THREE.Vector3()}, uRight: {value: new THREE.Vector3()}, uUp: {value: new THREE.Vector3()},
    uFade: {value: 1}, uQuiet: {value: quiet ? 1 : 0}
  };
  const shader = new THREE.ShaderMaterial({
    depthTest: false, depthWrite: false,
    uniforms,
    defines: {RAY_STEPS: constrained ? 100 : 150},
    vertexShader: `void main(){gl_Position=vec4(position.xy,0.,1.);}`,
    fragmentShader: `
      precision highp float;
      uniform float uTime,uFade,uQuiet;
      uniform vec2 uSize,uCenter;
      uniform vec3 uCamera,uForward,uRight,uUp;
      const float PI=3.14159265359;
      float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
      float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
      vec3 sky(vec3 d){
        float a=atan(d.z,d.x),b=asin(clamp(d.y,-1.,1.));
        vec2 uv=vec2(a,b)*290.;vec2 cell=floor(uv),f=fract(uv)-.5;
        float seed=hash(cell),star=pow(max(0.,1.-length(f)*5.),5.)*step(.993,seed);
        float haze=pow(max(0.,1.-abs(d.y+.15)),9.)*.006;
        return vec3(.006,.012,.023)+vec3(.38,.52,.71)*star*.7+vec3(.04,.12,.24)*haze;
      }
      vec3 accretion(vec3 p,vec3 ray){
        float r=length(p.xz);
        float inner=smoothstep(1.72,2.15,r),outer=1.-smoothstep(6.7,8.0,r);
        float angle=atan(p.z,p.x);
        float flow=angle-uTime*.26/pow(r*.32,1.5);
        float bands=.55+.20*sin(r*33.+sin(flow*4.+r*3.)*1.4)+.12*sin(r*83.+flow*8.);
        float turbulence=noise(vec2(flow*13.+r*2.,r*18.));
        float filament=pow(max(0.,sin(r*65.+noise(vec2(flow*8.,r*3.))*7.)),10.);
        float density=(bands*.6+turbulence*.55+filament*.22)*inner*outer;
        float hot=pow(2.0/max(r,2.),.8);
        vec3 amber=mix(vec3(1.0,.23,.035),vec3(1.0,.68,.29),smoothstep(.22,.7,hot));
        vec3 colour=mix(amber,vec3(1.,.92,.72),smoothstep(.7,1.,hot)*.82);
        vec3 velocity=normalize(vec3(-p.z,0.,p.x));
        float beaming=pow(clamp(1.+dot(velocity,-ray)*.28,.55,1.4),2.);
        return colour*density*pow(hot,1.8)*beaming*3.4;
      }
      void main(){
        vec2 uv=(gl_FragCoord.xy-uCenter*uSize)/uSize.y;
        vec3 ray=normalize(uForward*1.27+uRight*uv.x+uUp*uv.y);
        if(uQuiet>.5){gl_FragColor=vec4(sky(ray)*.6,1.);return;}
        vec3 pos=uCamera,dir=ray,light=vec3(0.);
        vec3 angular=cross(pos,dir);float angular2=dot(angular,angular);
        float minRadius=100.;float swallowed=0.;float transmission=1.;
        for(int i=0;i<RAY_STEPS;i++){
          float r=length(pos);minRadius=min(minRadius,r);
          if(r<1.025){swallowed=1.;break;}
          if(r>27.)break;
          float stepSize=clamp((r-1.)*.11,.055,.8);
          vec3 previous=pos;
          // Null-ray central-force approximation. Paths bend in three dimensions.
          vec3 acceleration=-1.5*angular2*pos/pow(r,5.);
          dir+=acceleration*stepSize;
          pos+=dir*stepSize;
          if(previous.y*pos.y<0.){
            float fraction=previous.y/(previous.y-pos.y);
            vec3 hit=mix(previous,pos,fraction);
            float diskRadius=length(hit.xz);
            if(diskRadius>1.72&&diskRadius<8.){
              vec3 emission=accretion(hit,normalize(dir));
              light+=emission*transmission;
              transmission*=.44;
            }
          }
          // Thin volumetric corona around the emitting plane, integrated along the curved ray.
          float diskR=length(pos.xz);
          if(diskR>1.8&&diskR<7.8){
            float corona=exp(-abs(pos.y)*13.)*.018*stepSize;
            light+=vec3(.8,.4,.12)*corona*transmission;
          }
        }
        if(swallowed<.5)light+=sky(normalize(dir))*transmission;
        // A narrow unresolved photon glow, not a substitute for the lensed disk.
        float photon=exp(-abs(minRadius-1.50)*28.)*.025;
        light+=vec3(1.,.76,.43)*photon;
        light=vec3(1.)-exp(-light*1.35);
        light=pow(max(light,vec3(0.)),vec3(.85));
        float vignette=1.-smoothstep(.25,1.2,length(uv))*.28;
        gl_FragColor=vec4(light*vignette*uFade,1.);
      }
    `
  });
  const raySurface = new THREE.Mesh(new THREE.PlaneGeometry(2,2), shader);
  raySurface.frustumCulled=false;raySurface.renderOrder=-100;
  scene.add(raySurface);
  // A genuine central 3D body also provides depth occlusion for the foreground particle geometry.
  const horizon=new THREE.Mesh(new THREE.SphereGeometry(1,48,32),new THREE.MeshBasicMaterial({color:0x000000,colorWrite:false}));
  blackHole.add(horizon);

  let seed=84;
  const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
  const count=constrained?1000:2800;
  const positions=new Float32Array(count*3),params=new Float32Array(count*3);
  for(let i=0;i<count;i++){
    const radius=3.0+random()*9.5,angle=random()*Math.PI*2;
    positions[i*3]=Math.cos(angle)*radius;
    positions[i*3+1]=(random()-.5)*(.12+radius*.035);
    positions[i*3+2]=Math.sin(angle)*radius;
    params[i*3]=radius;params[i*3+1]=random();params[i*3+2]=random();
  }
  const dustGeometry=new THREE.BufferGeometry();dustGeometry.setAttribute('position',new THREE.BufferAttribute(positions,3));dustGeometry.setAttribute('aParams',new THREE.BufferAttribute(params,3));
  const dustMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
    uniforms:{uTime:uniforms.uTime,uOpacity:{value:.28},uPixel:{value:pixelRatio}},
    vertexShader:`attribute vec3 aParams;uniform float uTime,uPixel;varying float vAlpha;varying vec3 vColour;void main(){float angle=uTime*.14/pow(aParams.x*.3,1.5);mat2 rotate=mat2(cos(angle),-sin(angle),sin(angle),cos(angle));vec3 p=position;p.xz=rotate*p.xz;p.y+=sin(uTime*.12+aParams.y*6.28)*.04;vec4 mv=modelViewMatrix*vec4(p,1.);gl_Position=projectionMatrix*mv;gl_PointSize=clamp((.45+aParams.z)*19./-mv.z,.5,1.8)*uPixel;vAlpha=.2+aParams.y*.5;vColour=mix(vec3(.36,.51,.7),vec3(1.,.7,.35),1.-aParams.z*.7);}`,
    fragmentShader:`uniform float uOpacity;varying float vAlpha;varying vec3 vColour;void main(){float d=length(gl_PointCoord-.5);float a=smoothstep(.5,.04,d);gl_FragColor=vec4(vColour,a*vAlpha*uOpacity);}`});
  const dust=new THREE.Points(dustGeometry,dustMaterial);blackHole.add(dust);

  // A subtle geometry Easter egg emerges in the shared gravitational field after the hero.
  const lattice=new THREE.Group();lattice.position.set(7,3,-10);scene.add(lattice);
  const latticeMaterial=new THREE.LineBasicMaterial({color:0x80b5dc,transparent:true,opacity:0});
  for(const size of [.6,1.2])lattice.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(size,size,size)),latticeMaterial));
  let elapsed=0,scroll=scrollY,targetScroll=scrollY,lastTime=0,lastFrame=0,paused=false,slowFrames=0;
  const state={frames:0,webgl:true,scene:'black-hole',diskTime:0,raySteps:constrained?100:150,particles:count,mode:constrained?'balanced':'full',paused:false};
  window.__cosmos=state;
  function render(time=0){
    if(document.hidden)return;
    if(!paused&&time-lastFrame<(constrained?1000/24:1000/36))return;
    const frameDuration=lastTime ? time-lastTime : 0;
    const delta=lastTime?Math.min(frameDuration/1000,.1):0;lastTime=time;lastFrame=time;
    if(!paused&&frameDuration>100)slowFrames++;else slowFrames=Math.max(0,slowFrames-1);
    if(slowFrames>16&&renderer.getPixelRatio()>.65){
      renderer.setPixelRatio(Math.max(.65,renderer.getPixelRatio()*.82));renderer.setSize(innerWidth,innerHeight);
      uniforms.uSize.value.set(innerWidth*renderer.getPixelRatio(),innerHeight*renderer.getPixelRatio());
      dustMaterial.uniforms.uPixel.value=renderer.getPixelRatio();slowFrames=0;state.mode='adaptive';
    }
    if(!paused)elapsed+=delta;
    scroll=paused?targetScroll:THREE.MathUtils.lerp(scroll,targetScroll,.15);
    const hero=document.querySelector('#hero');const heroEnd=hero?hero.offsetTop+hero.offsetHeight:innerHeight;
    const progress=Math.max(0,scroll/heroEnd);
    uniforms.uQuiet.value=quiet||progress>2.2?1:0;
    const shift=Math.min(progress,2.5);
    const centerX=constrained ? .5 : .66;
    const centerY=(constrained ? .17 : .27)+Math.min(progress,1.5)*.12;
    uniforms.uCenter.value.set(centerX,centerY);
    uniforms.uCamera.value.set(Math.sin(elapsed*.025)*.16,.8+shift*.7,15+shift*3.5);
    uniforms.uForward.value.copy(uniforms.uCamera.value).negate().normalize();
    uniforms.uRight.value.crossVectors(uniforms.uForward.value,new THREE.Vector3(0,1,0)).normalize();
    uniforms.uUp.value.crossVectors(uniforms.uRight.value,uniforms.uForward.value).normalize();
    uniforms.uTime.value=elapsed;
    uniforms.uFade.value=Math.max(.14,1-Math.max(0,progress-.7)*.55);
    camera.position.copy(uniforms.uCamera.value);camera.lookAt(0,0,0);
    camera.setViewOffset(innerWidth,innerHeight,innerWidth*(.5-centerX),innerHeight*(.5-(1-centerY)),innerWidth,innerHeight);
    blackHole.visible=!quiet&&progress<3;
    dustMaterial.uniforms.uOpacity.value=Math.max(.04,.35-shift*.09);
    latticeMaterial.opacity=quiet?0:Math.sin(Math.min(1,Math.max(0,progress*.45))*Math.PI)*.075;
    lattice.rotation.y=elapsed*.025;lattice.rotation.x=elapsed*.015;
    renderer.render(scene,camera);
    state.frames++;state.diskTime=elapsed;state.paused=paused;state.cameraZ=camera.position.z;state.triangles=renderer.info.render.triangles;state.drawCalls=renderer.info.render.calls;state.pixelRatio=renderer.getPixelRatio();
    canvas.style.opacity=quiet?'.35':'1';
  }
  function drawStatic(){requestAnimationFrame(()=>render(performance.now()));}
  function configureLoop(){paused=motion.matches||quiet||document.hidden;renderer.setAnimationLoop(paused?null:render);lastTime=0;drawStatic();}
  addEventListener('scroll',()=>{targetScroll=scrollY;if(paused)drawStatic();},{passive:true});
  addEventListener('resize',()=>{renderer.setSize(innerWidth,innerHeight);uniforms.uSize.value.set(innerWidth*renderer.getPixelRatio(),innerHeight*renderer.getPixelRatio());camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();drawStatic();});
  motion.addEventListener('change',configureLoop);document.addEventListener('visibilitychange',configureLoop);
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();renderer.setAnimationLoop(null);document.body.classList.remove('scene-ready');document.body.classList.add('scene-unavailable');});
  canvas.addEventListener('webglcontextrestored',()=>{document.body.classList.remove('scene-unavailable');document.body.classList.add('scene-ready');configureLoop();});
  addEventListener('pagehide',()=>renderer.setAnimationLoop(null));addEventListener('pageshow',configureLoop);
  render(performance.now());document.body.classList.add('scene-ready');configureLoop();
}
