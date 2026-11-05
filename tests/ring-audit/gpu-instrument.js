(()=>{
 const locations=new WeakMap(),programs=new Map();let nextId=1;
 const proto=WebGL2RenderingContext.prototype;
 const get=proto.getUniformLocation,set=proto.uniform1f;
 proto.getUniformLocation=function(program,name){const location=get.call(this,program,name);if(location&&name==='uTime'){if(!programs.has(program))programs.set(program,{id:nextId++,program,gl:this,location,uploads:0,last:null});locations.set(location,programs.get(program));}return location;};
 proto.uniform1f=function(location,value){const entry=locations.get(location);if(entry){entry.last=value;entry.uploads++;}return set.call(this,location,value);};
 window.readAnimationUniforms=()=>[...programs.values()].filter(p=>p.gl.isProgram(p.program)).map(p=>({id:p.id,role:p.gl.getAttachedShaders(p.program).some(s=>p.gl.getShaderSource(s).includes('feedingKnot'))?'disk':'dust',uploaded:p.last,gpu:p.gl.getUniform(p.program,p.location),uploads:p.uploads}));
})();
