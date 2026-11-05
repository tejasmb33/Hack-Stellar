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
    let radius=2.7+Math.pow(random(),.7)*21;
    let angle=random()*Math.PI*2;
    // Some matter starts in curved feeding streams. A compact, co-orbiting
    // part of the same flow occasionally passes closer to the camera.
    if(orbital&&i%9<3)angle=(i%3)*Math.PI*2/3+radius*.37+(random()-.5)*.45;
    if(orbital&&i%47===0){radius=7.5+random()*1.8;angle=1.02+(random()-.5)*.32;}
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
      vec3 p=position,velocity=vec3(0.);
      float radius=length(p.xz);
      if(aData.z<.5){
        float speed=1.14*pow(2.5/max(radius,2.),1.5);
        float angular=atan(p.z,p.x)+uTime*speed;
        float inflow=sin(aData.x*6.283+uTime*.09)*.12;
        p.xz=vec2(cos(angular),sin(angular))*(radius+inflow);
        p.y+=sin(angular*3.+uTime*.13)*.08;
        velocity=vec3(-sin(angular),0.,cos(angular))*radius*speed;
      }else{
        float drift=.10+aData.x*.27;
        // Wrap only at the distant bounds of the world volume, outside the
        // near camera frustum. Different depths turn modest velocities into
        // clearly different apparent foreground/background speeds.
        p.x=mod(p.x+uTime*drift+38.,76.)-38.;
        p.y+=sin(uTime*.19+aData.y*6.28)*.6;
        p.z+=sin(uTime*.12+aData.w*6.28)*.65;
        velocity=vec3(drift,cos(uTime*.19+aData.y*6.28)*.114,cos(uTime*.12+aData.w*6.28)*.078);
      }
      vec4 mv=modelViewMatrix*vec4(p,1.);
      gl_Position=projectionMatrix*mv;
      float rare=step(.975,aData.w);
      float size=mix(.42,1.35,aData.y)+rare*3.;
      float selected=step(.92,aData.w);
      vStretch=1.+selected*min(1.8,length(velocity)*.7+uTravel*.07);
      gl_PointSize=clamp(size*uViewport.y*.035/max(1.,-mv.z),.75,rare>0.?24.:6.)*vStretch;
      vDepth=-mv.z;
      vAlpha=(.35+aData.x*.55)*smoothstep(.6,2.,vDepth)*(1.-smoothstep(85.,140.,vDepth));
      float illumination=clamp(9./max(length(p),3.),.25,1.);
      vColour=mix(vec3(.34,.49,.72),vec3(1.,.70,.37),aData.z<.5?.88:aData.w)*(.9+illumination*1.7);
      vec3 viewVelocity=mat3(modelViewMatrix)*velocity;
      vAngle=atan(viewVelocity.y,viewVelocity.x);
    }`,
    fragmentShader:/* glsl */`
    uniform sampler2D uRayDepth;uniform vec2 uViewport;uniform float uShadowThreshold;
    varying vec3 vColour;varying float vDepth,vAlpha,vAngle,vStretch;
    void main(){
      vec2 p=gl_PointCoord-.5;
      p=mat2(cos(vAngle),-sin(vAngle),sin(vAngle),cos(vAngle))*p;
      p.y*=vStretch;
      float r=length(p);
      if(r>.5)discard;
      float packed=texture2D(uRayDepth,gl_FragCoord.xy/uViewport).a;
      bool shadow=packed>uShadowThreshold;
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
