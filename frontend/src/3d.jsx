import React, { useEffect } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import './App.css'

// MODEL CREDITS: "Segmentation_Lungs" (https://skfb.ly/owpzR) by blanen is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).

const ThreeDScene = () => {
  useEffect(() => {
    // Set up the scene, camera, and renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
    const renderer = new THREE.WebGLRenderer({ alpha: true }); // Alpha allows transparency
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.domElement.style.position = 'fixed'; // Use fixed positioning
    renderer.domElement.style.top = '0';
    renderer.domElement.style.left = '0';
    renderer.domElement.style.width = '100%';
    renderer.domElement.style.height = '100%';
    renderer.domElement.style.zIndex = '0'; // Place it above the gradient but below other components

    const container = document.getElementById('three-container');
    console.log(container);
    container.appendChild(renderer.domElement);

    // Variables for mouse interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetRotationY = 0;
    let model = null;

    // Load the GLTF model
    const loader = new GLTFLoader();
    loader.load('/scene.glb', (gltf) => {
      model = gltf.scene;

      const textureLoader = new THREE.TextureLoader();

      model.traverse((child) => {
        if (child.isMesh) {
            console.log('Material:', child.material);
            child.material.wireframe = true;
            child.material.roughness = 0.5;
            
        }
      });

      model.scale.set(5, 5, 5); // Adjust the scale of the model
      model.position.set(-100, -500, 0); // Adjust the position of the model
      scene.add(model);
    });


    // Add lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.3); // Soft white light
    scene.add(ambientLight);


    // Add a directional light to highlight the model
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.5); // Bright white light
    directionalLight.position.set(10, 10, 10); // Position the light above and to the side
    scene.add(directionalLight);

    // Add a point light for additional illumination
    const pointLight = new THREE.PointLight(0xffffff, 54351.413, 1000, 2); // Bright white light
    pointLight.position.set(0, 200, 200); // Position the light above and in front of the model
    scene.add(pointLight);

    // Add a spotlight for a focused beam
    const spotLight = new THREE.SpotLight(0xff00ff, 1.5); // Magenta light
    spotLight.position.set(-200, 200, 200);
    spotLight.angle = Math.PI / 6;
    spotLight.penumbra = 0.5;
    scene.add(spotLight);

    // Add mousemove event listener
    window.addEventListener('mousemove', (event) => {
      const windowHalfX = window.innerWidth / 2;
      const windowHalfY = window.innerHeight / 2;

      mouseX = (event.clientX - windowHalfX) / windowHalfX;
      mouseY = (event.clientY - windowHalfY) / windowHalfY;
    });

    // Position the camera
    camera.position.set(0, 0, 500); // Center the camera and move it back
    camera.position.z = 500;
    
    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);

      //  mouseX * 0.5 -> adjust sensitivity so it's smoother and not too fast
            // * 0.05 = slows/smooths out rotation 
      targetRotationY += (mouseX * 0.5 - targetRotationY) * 0.05;  // taretRotationY = rotates around y-axis = rotate horizontally


      if (model) {
        model.rotation.y = targetRotationY;
      }

      renderer.render(scene, camera);
    };
    animate();

    // Handle window resizing
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', null);
      renderer.dispose();
      container.removeChild(renderer.domElement);
    };
  }, []);

  return null; // No visible React elements; everything is rendered in the background
};

export default ThreeDScene;