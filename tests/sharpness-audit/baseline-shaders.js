export const screenVertex = `varying vec2 vUv; void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}`;

// Curved-ray volume renderer in Schwarzschild-radius units. A visual central-force
// approximation, not the Kerr/GR solver used for the film.
export const blackHoleFragment = /* glsl */`
precision highp float;
varying vec2 vUv;
uniform float uTime;
uniform mat4 uInverseProjection, uCameraWorld;
uniform sampler2D uMatter;
const float PI=3.14159265359;
uniform sampler2D uSky0,uSky1;
vec2 skyUV(vec3 p){return vec2(atan(p.z,p.x)/6.2831853+.5,asin(clamp(p.y,-1.,1.))/PI+.5);}
vec3 shellPoint(vec3 origin,vec3 direction,float radius){
  float b=dot(origin,direction);
  float distance=-b+sqrt(max(0.,b*b+radius*radius-dot(origin,origin)));
  return normalize(origin+direction*distance);
}
vec3 environment(vec3 origin,vec3 direction){
  vec2 nearUV=skyUV(shellPoint(origin,direction,100.));
  vec2 farUV=skyUV(shellPoint(origin,direction,240.));
  vec4 nearSky=texture2D(uSky0,nearUV),farSky=texture2D(uSky1,farUV);
  // Only the gas density drifts. Stars retain fixed world coordinates.
  float gas=texture2D(uSky0,nearUV+vec2(uTime*.000012,0)).a;
  float farGas=texture2D(uSky1,farUV-vec2(0,uTime*.000008)).a;
  vec3 col=vec3(.0025,.0045,.008)+nearSky.rgb*.9+farSky.rgb*.65;
  col+=mix(vec3(.015,.035,.06),vec3(.23,.092,.022),smoothstep(.005,.15,gas))*(gas+farGas*.45)*1.7;
  return col;
}
// Only the pattern is advected twice. Geometric, thermal and Doppler terms
// remain shared, avoiding duplicate volume-shading work at every ray step.
uniform vec4 uAdvection; // previous age/anchor, current age/anchor
uniform float uFlowBlend;
vec2 advectedPattern(vec3 p,float radius,float flow){
  vec2 uv=vec2(flow/6.2831853, radius*.117+sin(flow*5.+uTime*.23)*.003);
  // Ray steps diverge per fragment: use a stable, explicit texture level.
  vec4 field=textureLod(uMatter,uv+vec2(p.y*.04,0),0.);
  float striation=field.g;
  float filaments=pow(smoothstep(.19,.80,field.r),2.)*2.7 + pow(smoothstep(.18,.82,field.b),2.)*1.4;
  float density=.045+filaments*.65+striation*.10;
  float textureLight=.25+pow(smoothstep(.23,.78,field.r),2.)*1.8+pow(smoothstep(.18,.82,field.b),1.4)*.8;
  // Keep the approved light lanes, texture and exact local orbital rate.
  float feedingLane=pow(.5+.5*sin(flow*3.+radius*1.8+field.g*2.8),5.);
  float fineStream=pow(.5+.5*sin(flow*9.+radius*5.1+field.r*4.),12.);
  float feedingKnot=exp(-pow(sin((flow+radius*.25)*.5),2.)*18.);
  float flowingLight=.45+feedingLane*.72+fineStream*.16+feedingKnot*.60;
  return vec2(textureLight*flowingLight,density*(.8+feedingLane*.4));
}
// Continuous finite-height matter, advected at the local orbital speed.
vec4 matter(vec3 p,vec3 direction){
  float radius=length(p.xz);
  float inner=smoothstep(1.78,2.12,radius);
  float outer=1.-smoothstep(7.,10.,radius);
  float angle=atan(p.z,p.x);
  float speed=1.28*pow(2.5/max(radius,1.8),1.5);
  vec2 pattern=advectedPattern(p,radius,angle-uAdvection.y-uAdvection.x*speed);
  if(uFlowBlend>0.){
    vec2 nextPattern=advectedPattern(p,radius,angle-uAdvection.w-uAdvection.z*speed);
    pattern=mix(pattern,nextPattern,uFlowBlend);
  }
  float hot=pow(2.1/max(radius,2.1),.73);
  vec3 colour=mix(vec3(.72,.20,.037),vec3(1.0,.65,.29),smoothstep(.22,.58,hot));
  colour=mix(colour,vec3(1.0,.94,.75),smoothstep(.54,.97,hot));
  vec3 velocity=normalize(vec3(-p.z,0.,p.x));
  float doppler=pow(clamp(1.+dot(velocity,-direction)*.24,.6,1.4),2.);
  return vec4(colour*pow(hot,2.8)*doppler*3.3*pattern.x,pattern.y*inner*outer);
}
float erfApprox(float x){float q=x*x;return sign(x)*sqrt(max(0.,1.-exp(-q*(1.27323954+.147*q)/(1.+.147*q))));}
float verticalAverage(float a,float b,float height){
  float k=1.30384048/height;
  if(abs(b-a)<.0001)return exp(-pow((a+b)*.5*k,2.));
  return max(0.,.886226925*(erfApprox(b*k)-erfApprox(a*k))/(k*(b-a)));
}
void main(){
  vec3 origin=uCameraWorld[3].xyz;
  vec4 view=uInverseProjection*vec4(vUv*2.-1.,1.,1.);
  vec3 ray=normalize(mat3(uCameraWorld)*view.xyz);
  vec3 pos=origin,dir=ray,light=vec3(0.);
  vec3 forward=-uCameraWorld[2].xyz;
  float momentum=dot(cross(pos,dir),cross(pos,dir));
  float transmittance=1., depth=200., minimum=100.;
  bool captured=false;
  // Skip distant empty space analytically; integrate only near emitting matter.
  float b=dot(origin,dir);
  float discriminant=b*b+144.-dot(origin,origin);
  float entry=discriminant>0.?max(0.,-b-sqrt(discriminant)):0.;
  pos+=dir*entry;
  for(int i=0;i<RAY_STEPS;i++){
    float radius=length(pos);minimum=min(minimum,radius);
    if(radius<1.025){captured=true;depth=-min(depth,dot(pos-origin,forward));break;}
    if(radius>38.&&dot(pos,dir)>0.)break;
    float stepSize=clamp((radius-1.)*.14,.035,2.8);
    stepSize=min(stepSize,mix(.28,2.8,smoothstep(.12,1.8,abs(pos.y))));
    float r2=radius*radius;
    vec3 acceleration=pos*(-1.5*momentum/(r2*r2*radius));
    vec3 next=pos+dir*stepSize+acceleration*(.5*stepSize*stepSize);
    float nextRadius=length(next);
    float nextR2=nextRadius*nextRadius;
    vec3 nextAcceleration=next*(-1.5*momentum/(nextR2*nextR2*nextRadius));
    vec3 nextDir=dir+(acceleration+nextAcceleration)*(.5*stepSize);
    // Integrate the segment inside the slab; never step over its entire height.
    float diskRadius=length((pos.xz+next.xz)*.5);
    float slab=.08+diskRadius*.025;
    float dy=next.y-pos.y;
    float a=abs(dy)>.00001?(-slab-pos.y)/dy:0.;
    float z=abs(dy)>.00001?( slab-pos.y)/dy:1.;
    float lo=max(0.,min(a,z)),hi=min(1.,max(a,z));
    if(hi>lo && diskRadius>1.7 && diskRadius<10.5 && min(abs(pos.y),abs(next.y))<slab+abs(dy)){
      vec3 samplePoint=mix(pos,next,(lo+hi)*.5);
      vec4 emission=matter(samplePoint,normalize(dir));
      float height=.025+length(samplePoint.xz)*.008;
      float vertical=verticalAverage(mix(pos.y,next.y,lo),mix(pos.y,next.y,hi),height);
      float segment=(hi-lo)*length(next-pos)*vertical;
      float opacity=1.-exp(-emission.a*segment*4.8);
      light+=emission.rgb*opacity*transmittance;
      if(opacity*transmittance>.025&&depth>199.)depth=dot(samplePoint-origin,forward);
      transmittance*=1.-opacity;
    }
    pos=next;dir=nextDir;
    if(transmittance<.008)break;
  }
  if(!captured)light+=environment(pos,normalize(dir))*transmittance;
  light+=vec3(1.,.78,.48)*exp(-abs(minimum-1.5)*65.)*.12;
  // Linear HDR RGB; packed view depth in alpha (upper half marks the shadow).
  float encodedDepth=depth<0.?.5+abs(depth)/400.:depth/400.;
  gl_FragColor=vec4(light,encodedDepth);
}`;

export const copyFragment = `varying vec2 vUv;uniform sampler2D uSource;void main(){gl_FragColor=vec4(texture2D(uSource,vUv).rgb,1.);}`;
export const blurFragment = /* glsl */`
varying vec2 vUv;uniform sampler2D uSource;uniform vec2 uDirection;uniform float uThreshold;
vec3 sampleLight(vec2 uv){vec3 c=texture2D(uSource,uv).rgb;float l=max(c.r,max(c.g,c.b));return c*max(0.,l-uThreshold)/max(l,.001);}
void main(){vec3 c=sampleLight(vUv)*.227027;
 c+=(sampleLight(vUv+uDirection*1.384615)+sampleLight(vUv-uDirection*1.384615))*.316216;
 c+=(sampleLight(vUv+uDirection*3.230769)+sampleLight(vUv-uDirection*3.230769))*.070270;
 gl_FragColor=vec4(c,1.);
}`;
export const finishFragment = /* glsl */`
varying vec2 vUv;uniform sampler2D uSource,uBloom;uniform vec2 uTexel;
float luma(vec3 c){return dot(c,vec3(.299,.587,.114));}
vec3 aces(vec3 x){return clamp((x*(2.51*x+.03))/(x*(2.43*x+.59)+.14),0.,1.);}
void main(){
 vec3 c=texture2D(uSource,vUv).rgb;
 vec3 n=texture2D(uSource,vUv+vec2(0,uTexel.y)).rgb,s=texture2D(uSource,vUv-vec2(0,uTexel.y)).rgb;
 vec3 e=texture2D(uSource,vUv+vec2(uTexel.x,0)).rgb,w=texture2D(uSource,vUv-vec2(uTexel.x,0)).rgb;
 float edge=abs(luma(n)-luma(s))+abs(luma(e)-luma(w));
 c=mix(c,(c*2.+n+s+e+w)/6.,clamp(edge*.2,0.,.32));
 c+=texture2D(uBloom,vUv).rgb*.15;
 c=aces(c*.95);
 float vignette=1.-smoothstep(.28,.9,length((vUv-.5)*vec2(1.,.8)))*.18;
 c*=vignette;
 gl_FragColor=vec4(c,1.);
 #include <colorspace_fragment>
 float dither=(fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5)/255.;
 gl_FragColor.rgb=max(vec3(0.),gl_FragColor.rgb+dither);
}`;
