import * as THREE from '../vendor/three.module.js';
import {screenVertex} from './shaders.js';

// Original procedural sky shells, baked once on the GPU. RGB holds stars and
// alpha holds gas density. Curved rays still sample them in world space.
export function createEnvironment(renderer,constrained){
  const width=constrained?1024:2048;
  const targets=[0,1].map(()=>new THREE.WebGLRenderTarget(width,width/2,{depthBuffer:false,wrapS:THREE.RepeatWrapping,generateMipmaps:true,minFilter:THREE.LinearMipmapLinearFilter}));
  const geometry=new THREE.PlaneGeometry(2,2),scene=new THREE.Scene(),camera=new THREE.Camera();
  const material=new THREE.ShaderMaterial({depthTest:false,depthWrite:false,vertexShader:screenVertex,uniforms:{uLayer:{value:0}},fragmentShader:/* glsl */`
    varying vec2 vUv;uniform float uLayer;
    float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
    float noise(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);vec2 q=i.xy+vec2(37.,17.)*i.z;
      return mix(mix(mix(hash(q),hash(q+vec2(1,0)),f.x),mix(hash(q+vec2(0,1)),hash(q+1.),f.x),f.y),mix(mix(hash(q+vec2(37,17)),hash(q+vec2(38,17)),f.x),mix(hash(q+vec2(37,18)),hash(q+vec2(38,18)),f.x),f.y),f.z);}
    void main(){
      float longitude=(vUv.x-.5)*6.2831853,latitude=(vUv.y-.5)*3.14159265;
      vec3 direction=vec3(cos(longitude)*cos(latitude),sin(latitude),sin(longitude)*cos(latitude));
      vec2 grid=vUv*vec2(920.,460.)*(1.+uLayer*.31);
      vec2 cell=floor(grid),f=fract(grid)-.5;
      float seed=hash(cell+uLayer*91.);
      vec2 offset=vec2(hash(cell+3.),hash(cell+71.))*.7-.35;
      float size=mix(.07,.19,pow(hash(cell+19.),6.));
      float star=exp(-dot(f-offset,f-offset)/(size*size))*step(.974,seed);
      vec3 colour=mix(vec3(.48,.65,.95),vec3(1.,.82,.57),hash(cell+41.))*star;
      vec3 p=direction*4.+uLayer*17.;
      float n=noise(p),fine=noise(p*2.7+9.);
      float cloud=pow(max(0.,n*.7+fine*.3-.3),1.7);
      float lane=smoothstep(.14,.73,noise(p*1.8-11.));
      gl_FragColor=vec4(colour,cloud*lane);
    }`});
  const mesh=new THREE.Mesh(geometry,material);mesh.frustumCulled=false;scene.add(mesh);
  targets.forEach((target,i)=>{material.uniforms.uLayer.value=i;renderer.setRenderTarget(target);renderer.render(scene,camera);});
  renderer.setRenderTarget(null);geometry.dispose();material.dispose();
  return {textures:targets.map(t=>t.texture),dispose(){targets.forEach(t=>t.dispose());}};
}
