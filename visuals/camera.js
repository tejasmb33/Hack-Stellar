import * as THREE from '../vendor/three.module.js';

// One physical camera drives ray directions, particle projection and depth.
// No view offsets, animated screen centres, CSS transforms or model scaling.
export function createFlight(camera) {
  const positions = new THREE.CatmullRomCurve3([
    new THREE.Vector3(.3, .55, 11.7),
    new THREE.Vector3(2.3, 1.0, 10.9),
    new THREE.Vector3(6.4, 2.1, 13.6),
    new THREE.Vector3(12.5, 4.4, 19.8),
    new THREE.Vector3(20.5, 7.4, 29),
    new THREE.Vector3(30, 11, 42)
  ], false, 'centripetal');
  const targets = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-3.6, 1.4, 0),
    new THREE.Vector3(-3.6, -1.0, 0),
    new THREE.Vector3(-3.4, -2.0, 0),
    new THREE.Vector3(-3.0, -3.0, 0),
    new THREE.Vector3(-2.0, -2.0, 0),
    new THREE.Vector3(0, -1.5, 0)
  ], false, 'centripetal');
  const target = new THREE.Vector3();
  return (progress, time, narrow) => {
    positions.getPoint(progress, camera.position);
    targets.getPoint(progress, target);
    target.x *= narrow ? .17 : 1;
    if (narrow) { camera.position.z += 3.3 * (1 - progress); target.y += .25; }
    camera.position.x += Math.sin(time * .09) * .12;
    camera.position.y += Math.sin(time * .11) * .055;
    const bank = .14 + progress * .15 + Math.sin(time * .045) * .008;
    camera.up.set(Math.sin(bank), Math.cos(bank), 0);
    camera.lookAt(target);
    camera.updateMatrixWorld();
  };
}
