import React, { useEffect, useRef } from "react";
import * as THREE from "three";

var hsvToRgb = function (h, s, v) {
  var r, g, b;
  var i;
  var f, p, q, t;

  // Make sure our arguments stay in-range
  h = Math.max(0, Math.min(360, h));
  s = Math.max(0, Math.min(100, s));
  v = Math.max(0, Math.min(100, v));

  // We accept saturation and value arguments from 0 to 100 because that's
  // how Photoshop represents those values. Internally, however, the
  // saturation and value are calculated from a range of 0 to 1. We make
  // That conversion here.
  s /= 100;
  v /= 100;

  if (s == 0) {
    // Achromatic (grey)
    r = g = b = v;
    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
  }

  h /= 60; // sector 0 to 5
  i = Math.floor(h);
  f = h - i; // factorial part of h
  p = v * (1 - s);
  q = v * (1 - s * f);
  t = v * (1 - s * (1 - f));

  switch (i) {
    case 0:
      r = v;
      g = t;
      b = p;
      break;

    case 1:
      r = q;
      g = v;
      b = p;
      break;

    case 2:
      r = p;
      g = v;
      b = t;
      break;

    case 3:
      r = p;
      g = q;
      b = v;
      break;

    case 4:
      r = t;
      g = p;
      b = v;
      break;

    default: // case 5:
      r = v;
      g = p;
      b = q;
  }

  return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
};

function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length == 1 ? "0" + hex : hex;
}

function assignColorsToAtoms(moleculeJson) {
  const elementSet = new Set();
  const atoms = moleculeJson.atoms;
  atoms.forEach((atom) => elementSet.add(atom.element));
  const numberOfUniqueElements = elementSet.size;

  let i = 360 / (numberOfUniqueElements - 1); // distribute the colors evenly on the hue range
  let r = []; // hold the generated colors
  let sv = 70;
  for (var x = 0; x < numberOfUniqueElements; x++) {
    sv = sv > 90 ? 70 : sv + 10;
    r.push(hsvToRgb(i * x, sv, sv)); // you can also alternate the saturation and value for even more contrast between the colors
  }

  const mapping = {};
  let n = 0;
  for (const element of elementSet.keys()) {
    mapping[element] = `#${componentToHex(r[n][0])}${componentToHex(
      r[n][1]
    )}${componentToHex(r[n][2])}`;
    n++;
  }

  return mapping;
}

function ColorIndex({ colorMapping }) {
  const ret = [];
  for (const element in colorMapping) {
    ret.push(
      <div
        className="centeredDiv"
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          margin: 10,
        }}
      >
        <div
          style={{
            background: colorMapping[element],
            width: 50,
            height: 50,
            borderRadius: 25,
            marginRight: 10,
          }}
        />
        {`    ${element}`}
      </div>
    );
  }

  return ret;
}

function MoleculeRenderer({ moleculeJSON }) {
  const mountRef = useRef();
  const colorMapping = assignColorsToAtoms(moleculeJSON);
  useEffect(() => {
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.45, window.innerHeight / 2);

    if (mountRef.current) {
      mountRef.current.appendChild(renderer.domElement);
    }

    moleculeJSON.atoms.forEach((atom) => {
      const geometry = new THREE.SphereGeometry(0.2);
      const material = new THREE.MeshBasicMaterial({
        color: colorMapping[atom.element],
      });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.set(...atom.position);
      scene.add(sphere);
    });

    moleculeJSON.bonds.forEach((bond) => {
      const from = moleculeJSON.atoms[bond.atoms[0]].position;
      const to = moleculeJSON.atoms[bond.atoms[1]].position;
      const dir = new THREE.Vector3(...to).sub(new THREE.Vector3(...from));
      const bondLength = dir.length();
      const bondGeometry = new THREE.CylinderGeometry(
        0.05,
        0.05,
        bondLength,
        32
      );
      const bondMaterial = new THREE.MeshBasicMaterial({ color: "white" });
      const bondMesh = new THREE.Mesh(bondGeometry, bondMaterial);
      bondMesh.position.copy(
        new THREE.Vector3(...from).add(dir.multiplyScalar(0.5))
      );
      bondMesh.quaternion.setFromUnitVectors(
        new THREE.Vector3(0, 1, 0),
        dir.clone().normalize()
      );
      scene.add(bondMesh);

      const animate = () => {
        requestAnimationFrame(animate);
        if (scene) {
          scene.rotation.x += 0.005;
          scene.rotation.y += 0.005;
        }
        renderer.render(scene, camera);
      };

      // Start the animation
      animate();
    });

    return () => {
      mountRef.current = null;
    };
  }, []);

  return (
    <div>
      <div ref={mountRef} />
      <ColorIndex colorMapping={colorMapping} />
    </div>
  );
}

export default MoleculeRenderer;
