import * as THREE from '../vendor/three.module.js';

// Original 3D gravitational ray tracer. No Earth, image, texture or video background.
const canvas = document.querySelector('#universe-canvas');
const quiet = document.body.classList.contains('directory');
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const smallLayout = matchMedia('(max-width: 760px)').matches;
const constrained = matchMedia('(max-width: 760px)').matches || navigator.connection?.saveData || (navigator.deviceMemory && navigator.deviceMemory < 4);
let renderer;
try { renderer = new THREE.WebGLRenderer({canvas, alpha: true, antialias: false, powerPreference: constrained ? 'low-power' : 'high-performance'}); }
catch { document.body.classList.add('scene-unavailable'); }
if (renderer) createUniverse();

function createUniverse() {
  const pixelRatio = Math.min(devicePixelRatio, constrained ? 1 : 1.5, 1920 / innerWidth);
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
    uQuiet: {value: quiet ? 1 : 0}
  };
  const shader = new THREE.ShaderMaterial({
    depthTest: false, depthWrite: false,
    uniforms,
    defines: {RAY_STEPS: constrained ? 128 : 192},
    vertexShader: `void main(){gl_Position=vec4(position.xy,0.,1.);}`,
    fragmentShader: `
      precision highp float;
      uniform float uTime,uQuiet;
      uniform vec2 uSize,uCenter;
      uniform vec3 uCamera,uForward,uRight,uUp;
      const float PI=3.14159265359;
      float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
      float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
      float fbm(vec2 p){return noise(p)*.6+noise(p*2.1+13.)*.27+noise(p*4.3-8.)*.13;}
      vec3 sky(vec3 origin,vec3 d){
        vec3 background=vec3(.004,.008,.016);
        // Stars occupy three distant world-space planes; camera motion creates real depth parallax.
        for(int layer=0;layer<3;layer++){
          float depth=-160.-float(layer)*190.;
          float travel=(depth-origin.z)/min(d.z,-.025);
          vec2 world=(origin+d*travel).xy*(.44+float(layer)*.16);
          vec2 cell=floor(world),f=fract(world)-.5;
          float seed=hash(cell+float(layer)*41.7);
          vec2 location=vec2(hash(cell+31.),hash(cell+79.))*.65-.325;
          float radius=.035+.05*hash(cell+23.);
          float star=exp(-dot(f-location,f-location)/(radius*radius));
          star*=step(.996-float(layer)*.0005,seed);
          background+=mix(vec3(.42,.58,.83),vec3(.9,.74,.53),hash(cell+16.))*star*(.24+seed*.4);
        }
        // Low-density gas is sampled in world space and advects very slowly with the same environment.
        vec3 gas=origin*.018+d*9.;
        float volume=fbm(gas.xz+vec2(uTime*.006,0.))*fbm(gas.xy*1.3-vec2(0.,uTime*.003));
        float veil=pow(max(0.,volume-.19),2.5);
        background+=vec3(.045,.11,.20)*veil*.38;
        return background;
      }
      vec3 accretion(vec3 p,vec3 ray){
        float r=length(p.xz);
        float inner=smoothstep(1.72,2.15,r),outer=1.-smoothstep(6.7,8.0,r);
        float angle=atan(p.z,p.x);
        float flow=angle-uTime*.43/pow(r*.34,1.5);
        float cloud=fbm(vec2(flow*3.6,r*2.3));
        float fine=noise(vec2(flow*17.+r,r*18.));
        float phase=r*29.+sin(flow*5.+r*2.)*2.;
        float footprint=length(p-uCamera)/max(uSize.y*1.27,1.);
        float antialias=exp(-pow(footprint*48.,2.));
        float bands=.5+.14*sin(phase)*antialias;
        float spiral=pow(max(0.,sin(flow*9.+r*13.)),6.)*antialias;
        float density=(.42+cloud*.65+bands*.12+fine*.15+spiral*.11)*inner*outer;
        float hot=pow(2.0/max(r,2.),.8);
        vec3 amber=mix(vec3(1.0,.27,.055),vec3(1.0,.70,.33),smoothstep(.22,.7,hot));
        vec3 colour=mix(amber,vec3(1.,.96,.83),smoothstep(.65,1.,hot)*.9);
        vec3 velocity=normalize(vec3(-p.z,0.,p.x));
        float beaming=pow(clamp(1.+dot(velocity,-ray)*.28,.55,1.4),2.);
        return colour*density*pow(hot,1.8)*beaming*3.4;
      }
      void main(){
        vec2 uv=(gl_FragCoord.xy-uCenter*uSize)/uSize.y;
        vec3 ray=normalize(uForward*1.27+uRight*uv.x+uUp*uv.y);
        if(uQuiet>.5){gl_FragColor=vec4(sky(uCamera,ray)*.65,1.);return;}
        vec3 pos=uCamera,dir=ray,light=vec3(0.);
        vec3 angular=cross(pos,dir);float angular2=dot(angular,angular);
        float minRadius=100.;float swallowed=0.;float transmission=1.;
        for(int i=0;i<RAY_STEPS;i++){
          float r=length(pos);minRadius=min(minRadius,r);
          if(r<1.025){swallowed=1.;break;}
          if(r>75.&&dot(pos,dir)>0.)break;
          float stepSize=clamp((r-1.)*.105,.045,3.0);
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
        if(swallowed<.5)light+=sky(pos,normalize(dir))*transmission;
        // A narrow unresolved photon glow, not a substitute for the lensed disk.
        float photon=exp(-abs(minRadius-1.50)*28.)*.025;
        light+=vec3(1.,.76,.43)*photon;
        light=vec3(1.)-exp(-light*1.35);
        light=pow(max(light,vec3(0.)),vec3(.85));
        float vignette=1.-smoothstep(.25,1.2,length(uv))*.28;
        gl_FragColor=vec4(light*vignette,1.);
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
  const count=constrained?1800:4800;
  const positions=new Float32Array(count*3),params=new Float32Array(count*4);
  for(let i=0;i<count;i++){
    const radius=3.0+random()*21,angle=random()*Math.PI*2;
    positions[i*3]=Math.cos(angle)*radius;
    positions[i*3+1]=(random()-.5)*(.25+radius*.12);
    positions[i*3+2]=Math.sin(angle)*radius;
    params[i*4]=radius;params[i*4+1]=random();params[i*4+2]=random();params[i*4+3]=random();
  }
  const dustGeometry=new THREE.BufferGeometry();dustGeometry.setAttribute('position',new THREE.BufferAttribute(positions,3));dustGeometry.setAttribute('aParams',new THREE.BufferAttribute(params,4));
  const dustMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
    uniforms:{uTime:uniforms.uTime,uOpacity:{value:.28},uPixel:{value:pixelRatio}},
    vertexShader:`attribute vec4 aParams;uniform float uTime,uPixel;varying float vAlpha;varying vec3 vColour;void main(){
      float life=fract(aParams.y+uTime*.012);float r=aParams.x;
      float envelope=1.;
      if(aParams.w>.58){r=mix(25.,3.2,life);envelope=smoothstep(0.,.12,life)*(1.-smoothstep(.86,1.,life));}
      float angle=atan(position.z,position.x)+uTime*.23/pow(r*.24,1.5);
      vec3 p=vec3(cos(angle)*r,position.y,sin(angle)*r);
      if(aParams.w<.58)p.y*=.14;
      p.y+=sin(uTime*.12+aParams.y*6.28)*.08;
      vec4 mv=modelViewMatrix*vec4(p,1.);gl_Position=projectionMatrix*mv;
      gl_PointSize=clamp((.35+aParams.z*1.8)*26./max(1.,-mv.z),.6,3.3)*uPixel;
      vAlpha=(.14+aParams.y*.55)*envelope;
      vColour=mix(vec3(.26,.41,.61),vec3(1.,.79,.50),clamp(1.-r/28.,0.,1.));
    }`,
    fragmentShader:`uniform float uOpacity;varying float vAlpha;varying vec3 vColour;void main(){float d=length(gl_PointCoord-.5);float a=smoothstep(.5,.04,d);gl_FragColor=vec4(vColour,a*vAlpha*uOpacity);}`});
  const dust=new THREE.Points(dustGeometry,dustMaterial);blackHole.add(dust);

  const cameraPath=new THREE.CatmullRomCurve3([
    new THREE.Vector3(.05,.75,10.5),new THREE.Vector3(1.6,.9,9.9),
    new THREE.Vector3(4.0,1.6,13.8),new THREE.Vector3(8.2,3.6,19.5),
    new THREE.Vector3(13.5,6.0,27.0),new THREE.Vector3(20.0,9.0,37.0)
  ],false,'centripetal');
  const compositionPath=new THREE.CatmullRomCurve3([
    new THREE.Vector3(smallLayout?.57:.80,smallLayout?.18:.19,0),
    new THREE.Vector3(smallLayout?.70:.87,.29,0),
    new THREE.Vector3(1.04,.48,0),new THREE.Vector3(1.26,.66,0),
    new THREE.Vector3(1.42,.78,0),new THREE.Vector3(1.55,.90,0)
  ],false,'centripetal');
  const pathPosition=new THREE.Vector3(),composition=new THREE.Vector3();
  let elapsed=0,scroll=scrollY,targetScroll=scrollY,lastTime=0,lastFrame=0,paused=false,slowFrames=0;
  const state={frames:0,webgl:true,scene:'black-hole',diskTime:0,raySteps:constrained?128:192,particles:count,mode:constrained?'balanced':'full',paused:false};
  window.__cosmos=state;
  function render(time=0){
    if(document.hidden)return;
    if(!paused&&time-lastFrame<(constrained?1000/24:1000/36))return;
    const frameDuration=lastTime ? time-lastTime : 0;
    const delta=lastTime?Math.min(frameDuration/1000,.1):0;lastTime=time;lastFrame=time;
    if(!paused&&frameDuration>100)slowFrames++;else slowFrames=Math.max(0,slowFrames-1);
    const minimumResolution=constrained?.72:.85;
    if(slowFrames>16&&renderer.getPixelRatio()>minimumResolution){
      renderer.setPixelRatio(Math.max(minimumResolution,renderer.getPixelRatio()*.9));renderer.setSize(innerWidth,innerHeight);
      uniforms.uSize.value.set(innerWidth*renderer.getPixelRatio(),innerHeight*renderer.getPixelRatio());
      dustMaterial.uniforms.uPixel.value=renderer.getPixelRatio();slowFrames=0;state.mode='adaptive';
    }
    if(!paused)elapsed+=delta;
    // Damping is time-based; it remains consistent at different frame rates and reverses without a restart.
    const smoothing=1.-Math.exp(-Math.max(delta,.016)*8.);
    scroll=paused?targetScroll:THREE.MathUtils.lerp(scroll,targetScroll,smoothing);
    const hero=document.querySelector('#hero');const heroEnd=hero?hero.offsetTop+hero.offsetHeight:innerHeight;
    const progress=Math.max(0,scroll/heroEnd);
    const pathT=THREE.MathUtils.clamp(progress/4.8,0,1);
    cameraPath.getPoint(pathT,pathPosition);compositionPath.getPoint(pathT,composition);
    // Continuous camera drift changes inclination and perspective; the central body itself never spins.
    uniforms.uCamera.value.copy(pathPosition);
    uniforms.uCamera.value.x+=Math.sin(elapsed*.055)*.18;
    uniforms.uCamera.value.y+=Math.sin(elapsed*.075)*.10;
    uniforms.uCenter.value.set(composition.x,composition.y);
    uniforms.uForward.value.copy(uniforms.uCamera.value).negate().normalize();
    uniforms.uRight.value.crossVectors(uniforms.uForward.value,new THREE.Vector3(0,1,0)).normalize();
    uniforms.uUp.value.crossVectors(uniforms.uRight.value,uniforms.uForward.value).normalize();
    uniforms.uTime.value=elapsed;
    camera.position.copy(uniforms.uCamera.value);camera.lookAt(0,0,0);
    camera.setViewOffset(innerWidth,innerHeight,innerWidth*(.5-composition.x),innerHeight*(composition.y-.5),innerWidth,innerHeight);
    // No scroll visibility switch, opacity ramp, model scaling, or scene replacement.
    blackHole.visible=!quiet;
    dustMaterial.uniforms.uOpacity.value=quiet?0:.48;
    renderer.render(scene,camera);
    state.frames++;state.diskTime=elapsed;state.paused=paused;state.cameraZ=camera.position.z;state.triangles=renderer.info.render.triangles;state.drawCalls=renderer.info.render.calls;state.pixelRatio=renderer.getPixelRatio();state.camera=uniforms.uCamera.value.toArray();state.center=uniforms.uCenter.value.toArray();state.holeVisible=blackHole.visible;state.pathProgress=pathT;state.diskPhase=elapsed*.43;state.sceneOpacity=1;
    canvas.style.opacity='1';
  }
  function drawStatic(){requestAnimationFrame(()=>render(performance.now()));}
  function configureLoop(){paused=motion.matches||quiet||document.hidden;renderer.setAnimationLoop(paused?null:render);lastTime=0;drawStatic();}
  addEventListener('scroll',()=>{targetScroll=scrollY;if(paused)drawStatic();},{passive:true});
  addEventListener('resize',()=>{const narrow=innerWidth<=760;compositionPath.points[0].set(narrow?.57:.80,narrow?.18:.19,0);compositionPath.points[1].x=narrow?.70:.87;renderer.setSize(innerWidth,innerHeight);uniforms.uSize.value.set(innerWidth*renderer.getPixelRatio(),innerHeight*renderer.getPixelRatio());camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();drawStatic();});
  motion.addEventListener('change',configureLoop);document.addEventListener('visibilitychange',configureLoop);
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();renderer.setAnimationLoop(null);document.body.classList.remove('scene-ready');document.body.classList.add('scene-unavailable');});
  canvas.addEventListener('webglcontextrestored',()=>{document.body.classList.remove('scene-unavailable');document.body.classList.add('scene-ready');configureLoop();});
  addEventListener('pagehide',()=>renderer.setAnimationLoop(null));addEventListener('pageshow',configureLoop);
  render(performance.now());document.body.classList.add('scene-ready');configureLoop();
}
