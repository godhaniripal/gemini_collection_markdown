# Component Name
Mesh Gradients

# Library/Framework
React, Three.js (@react-three/fiber)

# Component Type
React Component, GLSL Shader

# Core Purpose
Animated mesh gradients for developers. Features customizable colors, speed controls, and interactive animations.

# Installation
```bash
npm install @shadergradient/react
```
```bash
npm install three @react-three/fiber @react-three/drei
npm install -D @types/three
```
```bash
npm install @react-three/postprocessing postprocessing
```

# Syntax & Parameters
### `@shadergradient/react` Components

**`<ShaderGradientCanvas>` Props:**
- `style`: `object` - CSS styles for the canvas container.
- `lazyLoad`: `undefined` - (Value provided in example).
- `fov`: `undefined` - (Value provided in example).
- `pixelDensity`: `number` - The pixel density of the canvas.
- `pointerEvents`: `string` - CSS pointer-events property.

**`<ShaderGradient>` Props:**
- `animate`: `'on' | 'off'` - Controls the animation state.
- `type`: `'sphere'` - The shape of the gradient mesh.
- `wireframe`: `boolean` - Toggles wireframe view.
- `shader`: `'defaults'` - The shader to use.
- `uTime`: `number` - Uniform for time.
- `uSpeed`: `number` - Controls animation speed.
- `uStrength`: `number` - Controls gradient strength.
- `uDensity`: `number` - Controls gradient density.
- `uFrequency`: `number` - Controls noise frequency.
- `uAmplitude`: `number` - Controls noise amplitude.
- `positionX`, `positionY`, `positionZ`: `number` - Position coordinates of the mesh.
- `rotationX`, `rotationY`, `rotationZ`: `number` - Rotation values of the mesh.
- `color1`, `color2`, `color3`: `string` - Hex color codes for the gradient.
- `reflection`: `number` - Controls the reflection amount.
- `cAzimuthAngle`: `number` - Camera azimuth angle.
- `cPolarAngle`: `number` - Camera polar angle.
- `cDistance`: `number` - Camera distance from the object.
- `cameraZoom`: `number` - Camera zoom level.
- `lightType`: `'env'` - Type of lighting.
- `brightness`: `number` - Brightness of the light.
- `envPreset`: `'city'` - Environment preset from drei.
- `grain`: `'on' | 'off'` - Toggles a grain effect.
- `toggleAxis`: `boolean` - Toggles visibility of axes helper.
- `zoomOut`: `boolean` - Controls camera zoom state.
- `hoverState`: `string` - (Value provided in example).
- `enableTransition`: `boolean` - Enables transition features.

### Custom `Blob` Component

**`<Blob>` Props:**
- `color`: `string` - Optional hex color string for the blob. Defaults to `'#ffd717'` or `'#2cb978'`.

**Shader Uniforms:**
- `u_time`: `{ value: number }` - Time uniform for animation.
- `u_intensity`: `{ value: number }` - Intensity of the displacement effect.
- `u_color`: `{ value: THREE.Color }` - The base color of the blob.

# Code Examples
### Crazy
```javascript
'use client';
import React from 'react';
import { ShaderGradientCanvas, ShaderGradient } from '@shadergradient/react';

function index() {
  return (
    <>
      <div className='relative h-screen w-screen'>
        <ShaderGradientCanvas
          style={{
            width: '100%',
            height: '100%',
          }}
          lazyLoad={undefined}
          fov={undefined}
          pixelDensity={1}
          pointerEvents='none'
        >
          <ShaderGradient
            animate='on'
            type='sphere'
            wireframe={false}
            shader='defaults'
            uTime={0}
            uSpeed={0.3}
            uStrength={0.3}
            uDensity={0.8}
            uFrequency={5.5}
            uAmplitude={3.2}
            positionX={-0.1}
            positionY={0}
            positionZ={0}
            rotationX={0}
            rotationY={130}
            rotationZ={70}
            color1='#73bfc4'
            color2='#ff810a'
            color3='#8da0ce'
            reflection={0.4}
            // View (camera) props
            cAzimuthAngle={270}
            cPolarAngle={180}
            cDistance={0.5}
            cameraZoom={15.1}
            // Effect props
            lightType='env'
            brightness={0.8}
            envPreset='city'
            grain='on'
            // Tool props
            toggleAxis={false}
            zoomOut={false}
            hoverState=''
            // Optional - if using transition features
            enableTransition={false}
          />
        </ShaderGradientCanvas>
      </div>
    </>
  );
}

export default index;
```

### Fresh
```javascript
'use client';
import React, { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { extend } from '@react-three/fiber';
import { MathUtils, Vector3, Color } from 'three';
import * as THREE from 'three';
import { Environment } from '@react-three/drei';
extend({ IcosahedronGeometry: THREE.IcosahedronGeometry });

const vertexShader = `
uniform float u_intensity;
uniform float u_time;

varying vec2 vUv;
varying float vDisplacement;

// Classic Perlin 3D Noise functions
vec4 permute(vec4 x) {
    return mod(((x*34.0)+1.0)*x, 289.0);
}

vec4 taylorInvSqrt(vec4 r) {
    return 1.79284291400159 - 0.85373472095314 * r;
}

vec3 fade(vec3 t) {
    return t*t*t*(t*(t*6.0-15.0)+10.0);
}

float cnoise(vec3 P) {
    vec3 Pi0 = floor(P);
    vec3 Pi1 = Pi0 + vec3(1.0);
    Pi0 = mod(Pi0, 289.0);
    Pi1 = mod(Pi1, 289.0);
    vec3 Pf0 = fract(P);
    vec3 Pf1 = Pf0 - vec3(1.0);
    vec4 ix = vec4(Pi0.x, Pi1.x, Pi0.x, Pi1.x);
    vec4 iy = vec4(Pi0.yy, Pi1.yy);
    vec4 iz0 = Pi0.zzzz;
    vec4 iz1 = Pi1.zzzz;

    vec4 ixy = permute(permute(ix) + iy);
    vec4 ixy0 = permute(ixy + iz0);
    vec4 ixy1 = permute(ixy + iz1);

    vec4 gx0 = ixy0 / 7.0;
    vec4 gy0 = fract(floor(gx0) / 7.0) - 0.5;
    gx0 = fract(gx0);
    vec4 gz0 = vec4(0.5) - abs(gx0) - abs(gy0);
    vec4 sz0 = step(gz0, vec4(0.0));
    gx0 -= sz0 * (step(0.0, gx0) - 0.5);
    gy0 -= sz0 * (step(0.0, gy0) - 0.5);

    vec4 gx1 = ixy1 / 7.0;
    vec4 gy1 = fract(floor(gx1) / 7.0) - 0.5;
    gx1 = fract(gx1);
    vec4 gz1 = vec4(0.5) - abs(gx1) - abs(gy1);
    vec4 sz1 = step(gz1, vec4(0.0));
    gx1 -= sz1 * (step(0.0, gx1) - 0.5);
    gy1 -= sz1 * (step(0.0, gy1) - 0.5);

    vec3 g000 = vec3(gx0.x,gy0.x,gz0.x);
    vec3 g100 = vec3(gx0.y,gy0.y,gz0.y);
    vec3 g010 = vec3(gx0.z,gy0.z,gz0.z);
    vec3 g110 = vec3(gx0.w,gy0.w,gz0.w);
    vec3 g001 = vec3(gx1.x,gy1.x,gz1.x);
    vec3 g101 = vec3(gx1.y,gy1.y,gz1.y);
    vec3 g011 = vec3(gx1.z,gy1.z,gz1.z);
    vec3 g111 = vec3(gx1.w,gy1.w,gz1.w);

    vec4 norm0 = taylorInvSqrt(vec4(dot(g000, g000), dot(g010, g010), dot(g100, g100), dot(g110, g110)));
    g000 *= norm0.x;
    g010 *= norm0.y;
    g100 *= norm0.z;
    g110 *= norm0.w;
    vec4 norm1 = taylorInvSqrt(vec4(dot(g001, g001), dot(g011, g011), dot(g101, g101), dot(g111, g111)));
    g001 *= norm1.x;
    g011 *= norm1.y;
    g101 *= norm1.z;
    g111 *= norm1.w;

    float n000 = dot(g000, Pf0);
    float n100 = dot(g100, vec3(Pf1.x, Pf0.yz));
    float n010 = dot(g010, vec3(Pf0.x, Pf1.y, Pf0.z));
    float n110 = dot(g110, vec3(Pf1.xy, Pf0.z));
    float n001 = dot(g001, vec3(Pf0.xy, Pf1.z));
    float n101 = dot(g101, vec3(Pf1.x, Pf0.y, Pf1.z));
    float n011 = dot(g011, vec3(Pf0.x, Pf1.yz));
    float n111 = dot(g111, Pf1);

    vec3 fade_xyz = fade(Pf0);
    vec4 n_z = mix(vec4(n000, n100, n010, n110), vec4(n001, n101, n011, n111), fade_xyz.z);
    vec2 n_yz = mix(n_z.xy, n_z.zw, fade_xyz.y);
    float n_xyz = mix(n_yz.x, n_yz.y, fade_xyz.x); 
    return 2.2 * n_xyz;
}

void main() {
    vUv = uv;

    vDisplacement = cnoise(position + vec3(2.0 * u_time));
  
    vec3 newPosition = position + normal * (u_intensity * vDisplacement);
  
    vec4 modelPosition = modelMatrix * vec4(newPosition, 1.0);
    vec4 viewPosition = viewMatrix * modelPosition;
    vec4 projectedPosition = projectionMatrix * viewPosition;
  
    gl_Position = projectedPosition;
}
`;

const fragmentShader = `
uniform float u_intensity;
uniform float u_time;
uniform vec3 u_color;

varying vec2 vUv;
varying float vDisplacement;

// Function to generate random noise
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main() {
  float distort = 2.0 * vDisplacement * u_intensity * sin(vUv.y * 10.0 + u_time);
  vec3 color = mix(u_color, vec3(1.0, 1.0, 1.0), distort);

  // Add screen-space random noise
  float noise = random(gl_FragCoord.xy * u_time * 0.05) * 0.05; // tweak strength
  color += noise;

  gl_FragColor = vec4(color, 1.0);
}
`;

interface BlobProps {
  color?: string;
}

const Blob: React.FC<BlobProps> = ({ color = '#ffd717' }) => {
  const mesh = useRef<THREE.Mesh>(null);
  const hover = useRef(false);

  const uniforms = useMemo(
    () => ({
      u_time: { value: 0 },
      u_intensity: { value: 0.3 },
      u_color: { value: new Color(color) },
    }),
    []
  );

  const targetPosition = useRef(new Vector3(0, 0, 0));
  const currentPosition = useRef(new Vector3(0, 0, 0));

  useFrame((state) => {
    const { clock, mouse } = state;

    if (mesh.current) {
      const material = mesh.current.material as THREE.ShaderMaterial;

      material.uniforms.u_time.value = 0.4 * clock.getElapsedTime();

      material.uniforms.u_intensity.value = MathUtils.lerp(
        material.uniforms.u_intensity.value,
        hover.current ? 0.7 : 1,
        0.02
      );

      // Update target position based on mouse
      targetPosition.current.set(mouse.x * 0.3, mouse.y * 0.3, 0);
      currentPosition.current.lerp(targetPosition.current, 0.1);

      mesh.current.position.copy(currentPosition.current);
    }
  });

  return (
    <mesh
      ref={mesh}
      scale={1.5}
      position={[0, 0, 0]}
      onPointerOver={() => (hover.current = true)}
      onPointerOut={() => (hover.current = false)}
    >
      <icosahedronGeometry args={[2, 20]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
      />
    </mesh>
  );
};

const Home: React.FC = () => {
  return (
    <div className='h-screen w-screen flex justify-center items-center'>
      <Canvas camera={{ position: [0.0, 0.0, 8.0], fov: 15 }}>
        <Environment preset='studio' environmentIntensity={0.5} />
        <Blob color='#ff0055' />
      </Canvas>
    </div>
  );
};

export default Home;
```

### Berries
```javascript
'use client';
import React, { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { extend } from '@react-three/fiber';
import { MathUtils, Vector3, Color } from 'three';
import * as THREE from 'three';
import { Environment } from '@react-three/drei';
extend({ IcosahedronGeometry: THREE.IcosahedronGeometry });

const vertexShader = `
uniform float u_intensity;
uniform float u_time;

varying vec2 vUv;
varying float vDisplacement;

// Classic Perlin 3D Noise functions
vec4 permute(vec4 x) {
    return mod(((x*34.0)+1.0)*x, 289.0);
}

vec4 taylorInvSqrt(vec4 r) {
    return 1.79284291400159 - 0.85373472095314 * r;
}

vec3 fade(vec3 t) {
    return t*t*t*(t*(t*6.0-15.0)+10.0);
}

float cnoise(vec3 P) {
    vec3 Pi0 = floor(P);
    vec3 Pi1 = Pi0 + vec3(1.0);
    Pi0 = mod(Pi0, 289.0);
    Pi1 = mod(Pi1, 289.0);
    vec3 Pf0 = fract(P);
    vec3 Pf1 = Pf0 - vec3(1.0);
    vec4 ix = vec4(Pi0.x, Pi1.x, Pi0.x, Pi1.x);
    vec4 iy = vec4(Pi0.yy, Pi1.yy);
    vec4 iz0 = Pi0.zzzz;
    vec4 iz1 = Pi1.zzzz;

    vec4 ixy = permute(permute(ix) + iy);
    vec4 ixy0 = permute(ixy + iz0);
    vec4 ixy1 = permute(ixy + iz1);

    vec4 gx0 = ixy0 / 7.0;
    vec4 gy0 = fract(floor(gx0) / 7.0) - 0.5;
    gx0 = fract(gx0);
    vec4 gz0 = vec4(0.5) - abs(gx0) - abs(gy0);
    vec4 sz0 = step(gz0, vec4(0.0));
    gx0 -= sz0 * (step(0.0, gx0) - 0.5);
    gy0 -= sz0 * (step(0.0, gy0) - 0.5);

    vec4 gx1 = ixy1 / 7.0;
    vec4 gy1 = fract(floor(gx1) / 7.0) - 0.5;
    gx1 = fract(gx1);
    vec4 gz1 = vec4(0.5) - abs(gx1) - abs(gy1);
    vec4 sz1 = step(gz1, vec4(0.0));
    gx1 -= sz1 * (step(0.0, gx1) - 0.5);
    gy1 -= sz1 * (step(0.0, gy1) - 0.5);

    vec3 g000 = vec3(gx0.x,gy0.x,gz0.x);
    vec3 g100 = vec3(gx0.y,gy0.y,gz0.y);
    vec3 g010 = vec3(gx0.z,gy0.z,gz0.z);
    vec3 g110 = vec3(gx0.w,gy0.w,gz0.w);
    vec3 g001 = vec3(gx1.x,gy1.x,gz1.x);
    vec3 g101 = vec3(gx1.y,gy1.y,gz1.y);
    vec3 g011 = vec3(gx1.z,gy1.z,gz1.z);
    vec3 g111 = vec3(gx1.w,gy1.w,gz1.w);

    vec4 norm0 = taylorInvSqrt(vec4(dot(g000, g000), dot(g010, g010), dot(g100, g100), dot(g110, g110)));
    g000 *= norm0.x;
    g010 *= norm0.y;
    g100 *= norm0.z;
    g110 *= norm0.w;
    vec4 norm1 = taylorInvSqrt(vec4(dot(g001, g001), dot(g011, g011), dot(g101, g101), dot(g111, g111)));
    g001 *= norm1.x;
    g011 *= norm1.y;
    g101 *= norm1.z;
    g111 *= norm1.w;

    float n000 = dot(g000, Pf0);
    float n100 = dot(g100, vec3(Pf1.x, Pf0.yz));
    float n010 = dot(g010, vec3(Pf0.x, Pf1.y, Pf0.z));
    float n110 = dot(g110, vec3(Pf1.xy, Pf0.z));
    float n001 = dot(g001, vec3(Pf0.xy, Pf1.z));
    float n101 = dot(g101, vec3(Pf1.x, Pf0.y, Pf1.z));
    float n011 = dot(g011, vec3(Pf0.x, Pf1.yz));
    float n111 = dot(g111, Pf1);

    vec3 fade_xyz = fade(Pf0);
    vec4 n_z = mix(vec4(n000, n100, n010, n110), vec4(n001, n101, n011, n111), fade_xyz.z);
    vec2 n_yz = mix(n_z.xy, n_z.zw, fade_xyz.y);
    float n_xyz = mix(n_yz.x, n_yz.y, fade_xyz.x); 
    return 2.2 * n_xyz;
}

void main() {
    vUv = uv;

    vDisplacement = cnoise(position + vec3(2.0 * u_time));
  
    vec3 newPosition = position + normal * (u_intensity * vDisplacement);
  
    vec4 modelPosition = modelMatrix * vec4(newPosition, 1.0);
    vec4 viewPosition = viewMatrix * modelPosition;
    vec4 projectedPosition = projectionMatrix * viewPosition;
  
    gl_Position = projectedPosition;
}
`;

const fragmentShader = `
uniform float u_intensity;
uniform float u_time;
uniform vec3 u_color;

varying vec2 vUv;
varying float vDisplacement;

// Function to generate random noise
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main() {
  float distort = 2.0 * vDisplacement * u_intensity * sin(vUv.y * 10.0 + u_time);
  vec3 color = mix(u_color, vec3(1.0, 1.0, 1.0), distort);

  // Add screen-space random noise
  float noise = random(gl_FragCoord.xy * u_time * 0.05) * 0.05; // tweak strength
  color += noise;

  gl_FragColor = vec4(color, 1.0);
}
`;

interface BlobProps {
  color?: string;
}

const Blob: React.FC<BlobProps> = ({ color = '#ffd717' }) => {
  const mesh = useRef<THREE.Mesh>(null);
  const hover = useRef(false);

  const uniforms = useMemo(
    () => ({
      u_time: { value: 0 },
      u_intensity: { value: 0.3 },
      u_color: { value: new Color(color) },
    }),
    []
  );

  const targetPosition = useRef(new Vector3(0, 0, 0));
  const currentPosition = useRef(new Vector3(0, 0, 0));

  useFrame((state) => {
    const { clock, mouse } = state;

    if (mesh.current) {
      const material = mesh.current.material as THREE.ShaderMaterial;

      material.uniforms.u_time.value = 0.4 * clock.getElapsedTime();

      material.uniforms.u_intensity.value = MathUtils.lerp(
        material.uniforms.u_intensity.value,
        hover.current ? 0.7 : 1,
        0.02
      );

      // Update target position based on mouse
      targetPosition.current.set(mouse.x * 0.3, mouse.y * 0.3, 0);
      currentPosition.current.lerp(targetPosition.current, 0.1);

      mesh.current.position.copy(currentPosition.current);
    }
  });

  return (
    <mesh
      ref={mesh}
      scale={1.5}
      position={[0, 0, 0]}
      onPointerOver={() => (hover.current = true)}
      onPointerOut={() => (hover.current = false)}
    >
      <icosahedronGeometry args={[2, 20]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
      />
    </mesh>
  );
};

const Home: React.FC = () => {
  return (
    <div className='h-screen w-screen flex justify-center items-center'>
      <Canvas camera={{ position: [0.0, 0.0, 8.0], fov: 15 }}>
        <Environment preset='studio' environmentIntensity={0.5} />
        <Blob color='#ff0055' />
      </Canvas>
    </div>
  );
};

export default Home;
```

### orange
```javascript
// @ts-nocheck
'use client';
import React, { useMemo, useRef } from 'react';
import { useFrame, ThreeElements, Canvas } from '@react-three/fiber';
import { extend } from '@react-three/fiber';
import { MathUtils, Vector3, Color, IcosahedronGeometry, Mesh } from 'three';
import { Environment, OrbitControls, useEnvironment } from '@react-three/drei';
import {
  EffectComposer,
  Bloom,
  N8AO,
  ToneMapping,
  Noise,
} from '@react-three/postprocessing';
import { BlendFunction } from 'postprocessing';
// Extend the geometry to resolve the R3F warning
extend({ IcosahedronGeometry });
const vertexShader = `
uniform float u_intensity;
uniform float u_time;

varying vec2 vUv;
varying float vDisplacement;

// Classic Perlin 3D Noise functions
vec4 permute(vec4 x) {
    return mod(((x*34.0)+1.0)*x, 289.0);
}

vec4 taylorInvSqrt(vec4 r) {
    return 1.79284291400159 - 0.85373472095314 * r;
}

vec3 fade(vec3 t) {
    return t*t*t*(t*(t*6.0-15.0)+10.0);
}

float cnoise(vec3 P) {
    vec3 Pi0 = floor(P);
    vec3 Pi1 = Pi0 + vec3(1.0);
    Pi0 = mod(Pi0, 289.0);
    Pi1 = mod(Pi1, 289.0);
    vec3 Pf0 = fract(P);
    vec3 Pf1 = Pf0 - vec3(1.0);
    vec4 ix = vec4(Pi0.x, Pi1.x, Pi0.x, Pi1.x);
    vec4 iy = vec4(Pi0.yy, Pi1.yy);
    vec4 iz0 = Pi0.zzzz;
    vec4 iz1 = Pi1.zzzz;

    vec4 ixy = permute(permute(ix) + iy);
    vec4 ixy0 = permute(ixy + iz0);
    vec4 ixy1 = permute(ixy + iz1);

    vec4 gx0 = ixy0 / 7.0;
    vec4 gy0 = fract(floor(gx0) / 7.0) - 0.5;
    gx0 = fract(gx0);
    vec4 gz0 = vec4(0.5) - abs(gx0) - abs(gy0);
    vec4 sz0 = step(gz0, vec4(0.0));
    gx0 -= sz0 * (step(0.0, gx0) - 0.5);
    gy0 -= sz0 * (step(0.0, gy0) - 0.5);

    vec4 gx1 = ixy1 / 7.0;
    vec4 gy1 = fract(floor(gx1) / 7.0) - 0.5;
    gx1 = fract(gx1);
    vec4 gz1 = vec4(0.5) - abs(gx1) - abs(gy1);
    vec4 sz1 = step(gz1, vec4(0.0));
    gx1 -= sz1 * (step(0.0, gx1) - 0.5);
    gy1 -= sz1 * (step(0.0, gy1) - 0.5);

    vec3 g000 = vec3(gx0.x,gy0.x,gz0.x);
    vec3 g100 = vec3(gx0.y,gy0.y,gz0.y);
    vec3 g010 = vec3(gx0.z,gy0.z,gz0.z);
    vec3 g110 = vec3(gx0.w,gy0.w,gz0.w);
    vec3 g001 = vec3(gx1.x,gy1.x,gz1.x);
    vec3 g101 = vec3(gx1.y,gy1.y,gz1.y);
    vec3 g011 = vec3(gx1.z,gy1.z,gz1.z);
    vec3 g111 = vec3(gx1.w,gy1.w,gz1.w);

    vec4 norm0 = taylorInvSqrt(vec4(dot(g000, g000), dot(g010, g010), dot(g100, g100), dot(g110, g110)));
    g000 *= norm0.x;
    g010 *= norm0.y;
    g100 *= norm0.z;
    g110 *= norm0.w;
    vec4 norm1 = taylorInvSqrt(vec4(dot(g001, g001), dot(g011, g011), dot(g101, g101), dot(g111, g111)));
    g001 *= norm1.x;
    g011 *= norm1.y;
    g101 *= norm1.z;
    g111 *= norm1.w;

    float n000 = dot(g000, Pf0);
    float n100 = dot(g100, vec3(Pf1.x, Pf0.yz));
    float n010 = dot(g010, vec3(Pf0.x, Pf1.y, Pf0.z));
    float n110 = dot(g110, vec3(Pf1.xy, Pf0.z));
    float n001 = dot(g001, vec3(Pf0.xy, Pf1.z));
    float n101 = dot(g101, vec3(Pf1.x, Pf0.y, Pf1.z));
    float n011 = dot(g011, vec3(Pf0.x, Pf1.yz));
    float n111 = dot(g111, Pf1);

    vec3 fade_xyz = fade(Pf0);
    vec4 n_z = mix(vec4(n000, n100, n010, n110), vec4(n001, n101, n011, n111), fade_xyz.z);
    vec2 n_yz = mix(n_z.xy, n_z.zw, fade_xyz.y);
    float n_xyz = mix(n_yz.x, n_yz.y, fade_xyz.x); 
    return 2.2 * n_xyz;
}

void main() {
    vUv = uv;

    vDisplacement = cnoise(position + vec3(2.0 * u_time));
  
    vec3 newPosition = position + normal * (u_intensity * vDisplacement);
  
    vec4 modelPosition = modelMatrix * vec4(newPosition, 1.0);
    vec4 viewPosition = viewMatrix * modelPosition;
    vec4 projectedPosition = projectionMatrix * viewPosition;
  
    gl_Position = projectedPosition;
}
`;

const fragmentShader = `
uniform float u_intensity;
uniform float u_time;
uniform vec3 u_color;

varying vec2 vUv;
varying float vDisplacement;

void main() {
    float distort = 2.0 * vDisplacement * u_intensity * sin(vUv.y * 10.0 + u_time);
    vec3 color = mix(u_color, vec3(1.0, 1.0, 1.0), distort);
    gl_FragColor = vec4(color, 1.0);
}
`;

interface BlobProps {
  color?: string;
}

const Blob: React.FC<BlobProps> = ({ color = '#2cb978' }) => {
  const mesh = useRef<THREE.Mesh>(null);
  const hover = useRef(false);

  const uniforms = useMemo(
    () => ({
      u_time: { value: 0 },
      u_intensity: { value: 0.3 },
      u_color: { value: new Color(color) },
    }),
    []
  );

  const targetPosition = useRef(new Vector3(0, 0, 0));
  const currentPosition = useRef(new Vector3(0, 0, 0));

  useFrame((state) => {
    const { clock, mouse } = state;

    if (mesh.current) {
      const material = mesh.current.material as THREE.ShaderMaterial;

      material.uniforms.u_time.value = 0.4 * clock.getElapsedTime();

      material.uniforms.u_intensity.value = MathUtils.lerp(
        material.uniforms.u_intensity.value,
        hover.current ? 0.3 : 0.5,
        0.02
      );

      //   Update target position based on mouse
      targetPosition.current.set(mouse.x * 0.5, mouse.y * 0.5, 0);
      currentPosition.current.lerp(targetPosition.current, 0.05);

      mesh.current.position.copy(currentPosition.current);
    }
  });
  return (
    <mesh
      ref={mesh}
      scale={1.5}
      position={[0, 0, 0]}
      onPointerOver={() => (hover.current = true)}
      onPointerOut={() => (hover.current = false)}
    >
      {/* <icosahedronGeometry args={[2, 20]} /> */}

      <icosahedronGeometry args={[2, 20]} />

      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
      />
    </mesh>
  );
};

// Updated index page
const Home: React.FC = () => {
  return (
    <div className='relative flex items-center justify-center w-screen h-screen overflow-auto bg-[#22ff7e]'>
      <article className=' relative z-[2]'>
        <h1 className=' text-[9vw] w-full text-center text-white'>
          It's Lemon's Time
        </h1>
      </article>
      <Canvas
        camera={{ position: [0.0, 0.0, 8.0], fov: 15 }}
        className=' !absolute top-0 left-0 w-screen h-screen'
      >
        <spotLight
          position={[10, 10, 10]}
          angle={0.15}
          penumbra={1}
          decay={0}
          intensity={Math.PI}
        />
        <OrbitControls />
        <Environment preset='city' environmentIntensity={0.5} />
        <directionalLight intensity={2} position={[0, 2, 3]} />

        <Blob />
        <EffectComposer>
          <Noise premultiply blendFunction={BlendFunction.ADD} />
        </EffectComposer>
      </Canvas>
    </div>
  );
};

export default Home;
```

# Variations & Tweaks
- **Library vs. Custom**: The "Crazy" example uses the `@shadergradient/react` library for a high-level, prop-driven approach. The "Fresh", "Berries", and "orange" examples show a from-scratch implementation using `@react-three/fiber` and custom GLSL shaders for more control.
- **Interactivity**: The custom shader examples ("Fresh", "Berries", "orange") implement mouse-follow and hover effects. The blob's position smoothly follows the cursor, and the displacement intensity changes on hover.
- **Post-processing**: The "orange" example adds post-processing effects like `Noise` using `@react-three/postprocessing` to enhance the visual style.
- **Lighting & Environment**: The examples use different lighting setups. The "Crazy" example uses `lightType='env'`, while the "orange" example uses a combination of `<spotLight>`, `<directionalLight>`, and `<Environment preset='city'>`.
- **Fragment Shader Effects**: The "Fresh" and "Berries" fragment shaders include an additional screen-space random noise effect for a grainy texture, which is absent in the "orange" example's fragment shader (which instead uses a post-processing `Noise` effect).

# Common Patterns
- **`useFrame` for Animation**: The `useFrame` hook from `@react-three/fiber` is consistently used to update shader uniforms (`u_time`, `u_intensity`) on every frame, creating the animation.
- **Custom Shaders with `<shaderMaterial>`**: A common pattern is to define GLSL vertex and fragment shaders as strings and pass them to a `<shaderMaterial>` along with `uniforms`.
- **Perlin Noise for Displacement**: The vertex shaders use a `cnoise` function (Classic Perlin Noise) to displace the vertices of the geometry, creating an organic, blob-like shape.
- **Mouse Interaction**: Mouse coordinates from the `useFrame` state are used to update a target position, which the mesh then smoothly interpolates towards using `lerp` for a follow effect.
- **Component Abstraction**: The core 3D object logic is encapsulated within a reusable React component (`<Blob>`), which can then be easily placed within a `<Canvas>`.

# Related Components
- **`@shadergradient/react`**: `ShaderGradientCanvas`, `ShaderGradient`
- **`@react-three/fiber`**: `Canvas`, `useFrame`, `extend`
- **`@react-three/drei`**: `Environment`, `OrbitControls`, `useEnvironment`
- **`@react-three/postprocessing`**: `EffectComposer`, `Bloom`, `N8AO`, `ToneMapping`, `Noise`
- **`three`**: `MathUtils`, `Vector3`, `Color`, `IcosahedronGeometry`, `Mesh`, `ShaderMaterial`

# Additional Notes
- All examples use the `'use client';` directive, indicating they are designed to run in a client-side environment, which is necessary for React components with hooks and interactivity (e.g., in Next.js App Router).
- The line `extend({ IcosahedronGeometry: THREE.IcosahedronGeometry });` is used to make the `THREE.IcosahedronGeometry` class available as a declarative JSX component (`<icosahedronGeometry>`) within the `@react-three/fiber` canvas.
- The "orange" example includes a `// @ts-nocheck` comment to disable TypeScript checking for that file.

# RAG Keywords
Mesh Gradient, ShaderGradient, ShaderGradientCanvas, @shadergradient/react, React, Three.js, @react-three/fiber, @react-three/drei, GLSL, Vertex Shader, Fragment Shader, Perlin Noise, cnoise, useFrame, shaderMaterial, uniforms, u_time, u_intensity, IcosahedronGeometry, post-processing, @react-three/postprocessing, EffectComposer, Bloom, Noise, Interactive Animation, Blob, WebGL, lerp, mouse follow