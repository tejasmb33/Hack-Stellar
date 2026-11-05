import * as THREE from '../vendor/three.module.js';

// Analytic GPU advection: buffers stay on the GPU, no per-frame JS particle loop.
// Orbital grains, mid-distance clouds and close illuminated flecks share the
// camera and sample the packed depth produced by the curved-ray volume pass.
export function createDust(count, uniforms) {
  let seed=1907;
  const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
  const positions=new Float32Array(count*3),data=new Float32Array(count*4);
  for(let i=0;i<count;i++){
    const orbital=i<count*.54;
    const radius=2.7+Math.pow(random(),.7)*21;
    const angle=random()*Math.PI*2;
    if(orbital){
      positions.set([Math.cos(angle)*radius,(random()-.5)*(.2+radius*.17),Math.sin(angle)*radius],i*3);
    }else{
      positions.set([(random()-.38)*76,(random()-.45)*39,random()*78-30],i*3);
    }
    data.set([random(),random(),orbital?0:1,random()],i*4);
  }
  const geometry=new THREE.BufferGeometry();
  geometry.setAttribute('position',new THREE.BufferAttribute(positions,3));
  geometry.setAttribute('aData',new THREE.BufferAttribute(data,4));
  const material=new THREE.ShaderMaterial({
    uniforms,transparent:true,depthTest:false,depthWrite:false,blending:THREE.AdditiveBlending,
    vertexShader:/* glsl */`
    attribute vec4 aData;uniform float uTime,uTravel;uniform vec2 uViewport;
    varying vec3 vColour;varying float vDepth,vAlpha,vAngle,vStretch;
    void main(){
      vec3 p=position;
      float radius=length(p.xz);
      if(aData.z<.5){
        float angular=atan(p.z,p.x)+uTime*.65*pow(2.5/max(radius,2.),1.5);
        float inflow=sin(aData.x*6.283+uTime*.09)*.12;
        p.xz=vec2(cos(angular),sin(angular))*(radius+inflow);
        p.y+=sin(angular*3.+uTime*.13)*.08;
      }else{
        p+=vec3(sin(uTime*.05+aData.x*6.28)*.45,cos(uTime*.07+aData.y*6.28)*.27,sin(uTime*.04+aData.w*6.28)*.4);
      }
      vec4 mv=modelViewMatrix*vec4(p,1.);
      gl_Position=projectionMatrix*mv;
      float rare=step(.975,aData.w);
      float size=mix(.42,1.35,aData.y)+rare*3.;
      gl_PointSize=clamp(size*uViewport.y*.035/max(1.,-mv.z),.75,rare>0.?24.:6.);
      vDepth=-mv.z;
      vAlpha=(.35+aData.x*.55)*smoothstep(.6,2.,vDepth)*(1.-smoothstep(85.,140.,vDepth));
      float illumination=clamp(9./max(length(p),3.),.25,1.);
      vColour=mix(vec3(.34,.49,.72),vec3(1.,.70,.37),aData.z<.5?.88:aData.w)*(.9+illumination*1.7);
      vAngle=aData.x*6.283;
      vStretch=1.+min(2.,uTravel*.06);
    }`,
    fragmentShader:/* glsl */`
    uniform sampler2D uRayDepth;uniform vec2 uViewport;
    varying vec3 vColour;varying float vDepth,vAlpha,vAngle,vStretch;
    void main(){
      vec2 p=gl_PointCoord-.5;
      p=mat2(cos(vAngle),-sin(vAngle),sin(vAngle),cos(vAngle))*p;
      p.y*=vStretch;
      float r=length(p);
      if(r>.5)discard;
      float packed=texture2D(uRayDepth,gl_FragCoord.xy/uViewport).a;
      bool shadow=packed>.5001;
      float sceneDepth=(shadow?packed-.5:packed)*400.;
      float behind=smoothstep(sceneDepth-.2,sceneDepth+.2,vDepth);
      float occlusion=mix(1.,shadow?0.:.12,behind);
      float core=exp(-r*r*95.);
      float halo=exp(-r*r*18.)*.18;
      gl_FragColor=vec4(vColour,(core+halo)*vAlpha*occlusion);
    }`
  });
  const points=new THREE.Points(geometry,material);
  points.frustumCulled=false;
  return points;
}
