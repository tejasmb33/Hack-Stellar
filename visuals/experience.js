import * as THREE from '../vendor/three.module.js';
import {createFlight} from './camera.js';
import {createPipeline} from './pipeline.js';

export function startExperience(){
  const canvas=document.querySelector('#universe-canvas');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const constrained=innerWidth<=760||navigator.connection?.saveData||(navigator.deviceMemory&&navigator.deviceMemory<4);
  let renderer;
  try{renderer=new THREE.WebGLRenderer({canvas,alpha:false,antialias:false,powerPreference:constrained?'low-power':'high-performance'});}
  catch{document.body.classList.add('scene-unavailable');return;}
  renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.NoToneMapping;
  renderer.setPixelRatio(Math.min(devicePixelRatio,constrained?1.25:1.75,2400/innerWidth));
  renderer.info.autoReset=false;
  const camera=new THREE.PerspectiveCamera(43,innerWidth/innerHeight,.1,350);
  const flight=createFlight(camera);
  let pipeline=createPipeline(renderer,camera,{constrained});
  let scale=constrained?.72:.85,scroll=scrollY,targetScroll=scrollY;
  let elapsed=0,lastTime=performance.now(),qualityStart=lastTime,qualityFrames=0,qualityCooldown=0;
  let paused=reduced.matches||document.hidden,raf=0,restore=false,disposed=false;
  const projected=new THREE.Vector3();
  const state=window.__cosmos={frames:0,webgl:true,scene:'black-hole',pipeline:'curved-ray-volume/HDR/depth-aware-dust',raySteps:pipeline.raySteps,particles:pipeline.particles,hdr:pipeline.hdr,paused,sceneOpacity:1,holeVisible:true,mode:constrained?'balanced':'full',samples:[],fps:0};
  pipeline.resize(scale);
  function draw(now){
    if(disposed||document.hidden||restore)return;
    // Wall-clock time is never clamped to a tenth of a second. GPU advection is
    // analytic, so even a long frame advances matter by the full elapsed time.
    const delta=Math.max(0,(now-lastTime)/1000);lastTime=now;
    if(!paused)elapsed+=delta;
    const smoothing=1.-Math.exp(-Math.min(delta,.5)*7.);
    const previous=scroll;
    scroll=paused?targetScroll:THREE.MathUtils.lerp(scroll,targetScroll,smoothing);
    const hero=document.querySelector('#hero');
    const journey=(hero?hero.offsetTop+hero.offsetHeight:innerHeight)*4.8;
    const progress=THREE.MathUtils.clamp(scroll/journey,0,1);
    flight(progress,elapsed,innerWidth<=760);
    pipeline.render(elapsed,Math.abs(scroll-previous)/Math.max(delta,.016)/90.);
    projected.set(0,0,0).project(camera);
    Object.assign(state,{frames:state.frames+1,diskTime:elapsed,diskPhase:elapsed*1.28,paused,camera:camera.position.toArray(),cameraZ:camera.position.z,center:[projected.x*.5+.5,projected.y*.5+.5],pathProgress:progress,pixelRatio:renderer.getPixelRatio(),resolution:pipeline.resolution,drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles});
    if(!paused){
      qualityFrames++;
      if(now-qualityStart>1800){
        const fps=qualityFrames*1000/(now-qualityStart);state.fps=+fps.toFixed(1);
        state.samples.push({time:+elapsed.toFixed(2),fps:state.fps,scale});if(state.samples.length>24)state.samples.shift();
        if(now>qualityCooldown){
          if(fps<(constrained?27:47)&&scale>.4){scale=Math.max(.4,scale*Math.max(.55,Math.sqrt(fps/(constrained?30:55))*.92));pipeline.resize(scale);state.mode='adaptive';qualityCooldown=now+1800;}
          else if(fps>58&&scale<(constrained?.8:1.0)){scale=Math.min(constrained?.8:1.,scale+.05);pipeline.resize(scale);qualityCooldown=now+5000;}
        }
        qualityFrames=0;qualityStart=now;
      }
    }
    if(!paused)raf=requestAnimationFrame(draw);
  }
  function requestStatic(){if(paused&&!document.hidden&&!restore){cancelAnimationFrame(raf);raf=requestAnimationFrame(draw);}}
  function configure(){
    cancelAnimationFrame(raf);paused=reduced.matches||document.hidden;state.paused=paused;
    lastTime=performance.now();qualityStart=lastTime;qualityFrames=0;
    if(!document.hidden&&!restore)raf=requestAnimationFrame(draw);
  }
  addEventListener('scroll',()=>{targetScroll=scrollY;requestStatic();},{passive:true});
  addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();pipeline?.resize(scale);requestStatic();});
  reduced.addEventListener('change',configure);document.addEventListener('visibilitychange',configure);
  canvas.addEventListener('webglcontextlost',event=>{
    event.preventDefault();restore=true;cancelAnimationFrame(raf);
    // Release old-context handles before Three rebuilds its GL caches on restore.
    // Deleting them after restoration raises INVALID_OPERATION against the new
    // context, including its texture, program and VAO state.
    pipeline?.dispose();pipeline=null;
    document.body.classList.remove('scene-ready');document.body.classList.add('scene-unavailable');
  });
  canvas.addEventListener('webglcontextrestored',()=>{
    if(disposed)return;
    pipeline=createPipeline(renderer,camera,{constrained});pipeline.resize(scale);state.hdr=pipeline.hdr;
    restore=false;document.body.classList.remove('scene-unavailable');document.body.classList.add('scene-ready');configure();
  });
  addEventListener('pagehide',event=>{cancelAnimationFrame(raf);if(!event.persisted){disposed=true;pipeline?.dispose();renderer.dispose();}});
  addEventListener('pageshow',()=>{if(!disposed)configure();});
  draw(performance.now());document.body.classList.add('scene-ready');configure();
}
