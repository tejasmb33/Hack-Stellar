import * as THREE from '../vendor/three.module.js';
import {screenVertex,blackHoleFragment,copyFragment,blurFragment,finishFragment} from './shaders.js';
import {createDust} from './particles.js';
import {createEnvironment} from './environment.js';

export function createPipeline(renderer,camera,{constrained=false}={}){
  const hdr=renderer.extensions.has('EXT_color_buffer_float');
  const type=hdr?THREE.HalfFloatType:THREE.UnsignedByteType;
  const target=()=>new THREE.WebGLRenderTarget(1,1,{type,depthBuffer:false,minFilter:THREE.LinearFilter,magFilter:THREE.LinearFilter});
  const rayTarget=target(),sceneTarget=target(),bloomA=target(),bloomB=target();
  const geometry=new THREE.PlaneGeometry(2,2),screenCamera=new THREE.Camera();
  const screenScene=new THREE.Scene(),screen=new THREE.Mesh(geometry);
  screen.frustumCulled=false;screenScene.add(screen);
  const material=(fragmentShader,uniforms={},defines={})=>new THREE.ShaderMaterial({vertexShader:screenVertex,fragmentShader,uniforms,defines,depthTest:false,depthWrite:false});
  function pass(shader,destination){screen.material=shader;renderer.setRenderTarget(destination);renderer.render(screenScene,screenCamera);}

  // Bake original, seamless polar turbulence once, rather than evaluating many
  // octaves at every volume sample on every animation frame. No external imagery.
  const matterTarget=new THREE.WebGLRenderTarget(1024,512,{depthBuffer:false,wrapS:THREE.RepeatWrapping,wrapT:THREE.RepeatWrapping,generateMipmaps:true,minFilter:THREE.LinearMipmapLinearFilter});
  const bake=material(/* glsl */`
  varying vec2 vUv;
  float hash(vec3 p){return fract(sin(dot(p,vec3(127.1,311.7,74.7)))*43758.5453);}
  float noise(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
    return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
    mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),mix(hash(i+vec3(0,1,1)),hash(i+1.),f.x),f.y),f.z);}
  void main(){float angle=vUv.x*6.2831853;
    vec3 p=vec3(cos(angle)*3.,sin(angle)*3.,vUv.y*16.);
    float n=noise(p)*.5+noise(p*2.03+5.)*.28+noise(p*4.1)*.15+noise(p*8.3)*.07;
    float fine=noise(p*vec3(6.,6.,3.)+n*2.);
    float filament=noise(vec3(cos(angle)*7.,sin(angle)*7.,vUv.y*145.+n*3.))*.65
      +noise(vec3(cos(angle)*13.,sin(angle)*13.,vUv.y*280.+fine*4.))*.35;
    gl_FragColor=vec4(n,fine,filament,1.);
  }`);
  pass(bake,matterTarget);bake.dispose();
  const environment=createEnvironment(renderer,constrained);
  const uniforms={uSky0:{value:environment.textures[0]},uSky1:{value:environment.textures[1]},uTime:{value:0},uInverseProjection:{value:camera.projectionMatrixInverse},uCameraWorld:{value:camera.matrixWorld},uMatter:{value:matterTarget.texture}};
  const raySteps=constrained?120:160;
  const rayMaterial=material(blackHoleFragment,uniforms,{RAY_STEPS:raySteps});
  const copy=material(copyFragment,{uSource:{value:rayTarget.texture}});
  const blur=material(blurFragment,{uSource:{value:sceneTarget.texture},uDirection:{value:new THREE.Vector2()},uThreshold:{value:1.}});
  const finish=material(finishFragment,{uSource:{value:sceneTarget.texture},uBloom:{value:bloomB.texture},uTexel:{value:new THREE.Vector2()}});
  const particleUniforms={uTime:uniforms.uTime,uTravel:{value:0},uViewport:{value:new THREE.Vector2()},uRayDepth:{value:rayTarget.texture}};
  const particleScene=new THREE.Scene();
  const particles=constrained?4000:10500;
  const dust=createDust(particles,particleUniforms);particleScene.add(dust);
  let width=1,height=1,scale=1;
  function resize(nextScale){
    scale=nextScale;renderer.setSize(innerWidth,innerHeight,false);
    const size=renderer.getDrawingBufferSize(new THREE.Vector2());width=size.x;height=size.y;
    // The heavy curved-ray volume is independent of the crisp particle/output resolution.
    const w=Math.max(1,Math.round(width*scale)),h=Math.max(1,Math.round(height*scale));
    rayTarget.setSize(w,h);sceneTarget.setSize(width,height);
    bloomA.setSize(Math.max(1,width>>2),Math.max(1,height>>2));bloomB.setSize(Math.max(1,width>>2),Math.max(1,height>>2));
    particleUniforms.uViewport.value.set(width,height);finish.uniforms.uTexel.value.set(1/width,1/height);
  }
  return {
    hdr,raySteps,particles,resize,
    get resolution(){return {output:[width,height],volume:[rayTarget.width,rayTarget.height],scale};},
    render(time,travel){
      uniforms.uTime.value=time;particleUniforms.uTravel.value=travel;
      renderer.info.reset();
      pass(rayMaterial,rayTarget);
      pass(copy,sceneTarget);
      renderer.autoClear=false;renderer.render(particleScene,camera);renderer.autoClear=true;
      blur.uniforms.uSource.value=sceneTarget.texture;blur.uniforms.uDirection.value.set(4/width,0);blur.uniforms.uThreshold.value=1.15;pass(blur,bloomA);
      blur.uniforms.uSource.value=bloomA.texture;blur.uniforms.uDirection.value.set(0,4/height);blur.uniforms.uThreshold.value=0;pass(blur,bloomB);
      pass(finish,null);
    },
    dispose(){environment.dispose();[rayTarget,sceneTarget,bloomA,bloomB,matterTarget].forEach(t=>t.dispose());[rayMaterial,copy,blur,finish,dust.material].forEach(m=>m.dispose());dust.geometry.dispose();geometry.dispose();}
  };
}
