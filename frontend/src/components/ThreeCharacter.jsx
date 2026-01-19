import React, { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Sphere, Cylinder, Float, Trail } from "@react-three/drei";
const BotAvatar = () => {
  const group = useRef();
  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    group.current.rotation.y = Math.sin(t / 2) * 0.1; 
  });
  return (
    <group ref={group} rotation={[0, Math.PI, 0]} scale={2.2}>
      <Float speed={2} rotationIntensity={0.2} floatIntensity={0.5}>
        {}
        <Sphere args={[0.35, 32, 32]} position={[0, 0.4, 0]}>
          <meshStandardMaterial 
            color="#0ea5e9" 
            metalness={0.8} 
            roughness={0.2} 
            emissive="#0ea5e9"
            emissiveIntensity={0.2}
          />
        </Sphere>
        {}
        <Sphere args={[0.25, 32, 32]} position={[0, 0.45, 0.2]} scale={[1, 0.3, 0.5]}>
           <meshStandardMaterial color="#ffffff" emissive="#ffffff" emissiveIntensity={2} />
        </Sphere>
        {}
        <Cylinder args={[0.25, 0.15, 0.6, 32]} position={[0, -0.2, 0]}>
          <meshStandardMaterial color="#ffffff" metalness={0.6} roughness={0.3} />
        </Cylinder>
        {}
        <Sphere args={[0.1, 32, 32]} position={[-0.35, -0.1, 0]}>
          <meshStandardMaterial color="#0ea5e9" emissive="#0ea5e9" emissiveIntensity={0.5} />
        </Sphere>
        <Sphere args={[0.1, 32, 32]} position={[0.35, -0.1, 0]}>
          <meshStandardMaterial color="#0ea5e9" emissive="#0ea5e9" emissiveIntensity={0.5} />
        </Sphere>
        {}
        <Cylinder args={[0.15, 0.2, 0.4, 32]} position={[0, 0, -0.25]} rotation={[0.5, 0, 0]}>
           <meshStandardMaterial color="#334155" />
        </Cylinder>
        {}
        <Sphere args={[0.08, 16, 16]} position={[0, -0.3, -0.35]}>
           <meshBasicMaterial color="#f59e0b" />
        </Sphere>
      </Float>
    </group>
  );
};
export default function ThreeCharacter() {
  return (
    <Canvas camera={{ position: [0, 1, 3], fov: 45 }} style={{ background: 'transparent', height: '100%', width: '100%' }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <pointLight position={[-10, -10, -10]} color="blue" intensity={1} />
      <BotAvatar />
    </Canvas>
  );
}


