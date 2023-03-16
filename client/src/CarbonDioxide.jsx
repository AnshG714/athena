import React, { useEffect, useRef } from "react";
import * as THREE from "three";

const methane = {
  atoms: [
    {
      element: "C",
      position: [0, 0, 0],
    },
    {
      element: "H",
      position: [1.2, 0, 0],
    },
    {
      element: "H",
      position: [0, 1.2, 0],
    },
    {
      element: "H",
      position: [0, -1.2, 0],
    },
    {
      element: "H",
      position: [-1.2, 0, 0],
    },
  ],
  bonds: [
    {
      atoms: [0, 1],
    },
    {
      atoms: [0, 2],
    },
    {
      atoms: [0, 3],
    },
    {
      atoms: [0, 4],
    },
  ],
};

function CarbonDioxide() {
  const mountRef = useRef();
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
    renderer.setSize(window.innerWidth / 3, window.innerHeight / 3);

    if (mountRef.current) {
      mountRef.current.appendChild(renderer.domElement);
    }

    let CO2 = {
      atoms: [
        { element: "C", position: [-0.75, 0, 0] },
        { element: "O", position: [0.75, 0.866, 0] },
        { element: "O", position: [0.75, -0.866, 0] },
      ],
      bonds: [{ atoms: [0, 1] }, { atoms: [0, 2] }],
    };

    CO2 = methane;

    CO2.atoms.forEach((atom) => {
      const geometry = new THREE.SphereGeometry(0.2);
      const material = new THREE.MeshBasicMaterial({ color: "white" });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.set(...atom.position);
      scene.add(sphere);
    });

    CO2.bonds.forEach((bond) => {
      const from = CO2.atoms[bond.atoms[0]].position;
      const to = CO2.atoms[bond.atoms[1]].position;
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

  return <div ref={mountRef} />;
}

export default CarbonDioxide;
