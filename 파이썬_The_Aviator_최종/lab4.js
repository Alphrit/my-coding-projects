import * as THREE from 'three';
import * as BufferGeometryUtils from './node_modules/three/examples/jsm/utils/BufferGeometryUtils.js';

//COLORS
var Colors = {
    red:0xf25346,
    white:0xd8d0d1,
    brown:0x59332e,
    brownDark:0x23190f,
    pink:0xF5986E,
    yellow:0xf4ce93,
    blue:0x68c3c0,

};

///////////////

// GAME VARIABLES
var game;
var deltaTime = 0;
var newTime = new Date().getTime();
var oldTime = new Date().getTime();
var ennemiesPool = [];
var particlesPool = [];
var particlesInUse = [];

function resetGame(){
  game = {speed:0,
          initSpeed:.00035,
          baseSpeed:.00035,
          targetBaseSpeed:.00035,
          incrementSpeedByTime:.0000025,
          incrementSpeedByLevel:.000005,
          distanceForSpeedUpdate:100,
          speedLastUpdate:0,

          distance:0,
          ratioSpeedDistance:50,
          energy:100,
          ratioSpeedEnergy:3,

          level:1,
          levelLastUpdate:0,
          distanceForLevelUpdate:1000,

          planeDefaultHeight:100,
          planeAmpHeight:80,
          planeAmpWidth:75,
          planeMoveSensivity:0.005,
          planeRotXSensivity:0.0008,
          planeRotZSensivity:0.0004,
          planeFallSpeed:.001,
          planeMinSpeed:1.2,
          planeMaxSpeed:1.6,
          planeSpeed:0,
          planeCollisionDisplacementX:0,
          planeCollisionSpeedX:0,

          planeCollisionDisplacementY:0,
          planeCollisionSpeedY:0,

          seaRadius:600,
          seaLength:800,
          //seaRotationSpeed:0.006,
          wavesMinAmp : 5,
          wavesMaxAmp : 20,
          wavesMinSpeed : 0.001,
          wavesMaxSpeed : 0.003,

          cameraFarPos:500,
          cameraNearPos:150,
          cameraSensivity:0.002,

          coinDistanceTolerance:15,
          coinValue:3,
          coinsSpeed:.5,
          coinLastSpawn:0,
          distanceForCoinsSpawn:100,

          ennemyDistanceTolerance:10,
          ennemyValue:10,
          ennemiesSpeed:.6,
          ennemyLastSpawn:0,
          distanceForEnnemiesSpawn:50,

          status : "playing",
         };
  fieldLevel.innerHTML = Math.floor(game.level);
}

//THREEJS RELATED VARIABLES

var scene,
    camera, fieldOfView, aspectRatio, nearPlane, farPlane,
    renderer,
    container,
    controls;

//SCREEN VARIABLES

var HEIGHT, WIDTH,
    mousePos = { x: 0, y: 0 };

//INIT THREE JS, SCREEN EVENTS

function createScene() {

  HEIGHT = window.innerHeight;
  WIDTH = window.innerWidth;

  scene = new THREE.Scene();
  aspectRatio = WIDTH / HEIGHT;
  fieldOfView = 50;
  nearPlane = .1;
  farPlane = 10000;
  camera = new THREE.PerspectiveCamera(
    fieldOfView,
    aspectRatio,
    nearPlane,
    farPlane
    );
  scene.fog = new THREE.Fog(0xf7d9aa, 100, 10000);
  camera.position.set(-300, game.planeDefaultHeight+800, 0);
  camera.lookAt(new THREE.Vector3(0, 700, 0));
  camera.applyMatrix4(new THREE.Matrix4().makeTranslation(0, 0, 0));
  camera.applyMatrix4(new THREE.Matrix4().makeRotationY(0));
  camera.up.set(0, 1, 0);
  //camera.lookAt(new THREE.Vector3(0, 400, 0));

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(WIDTH, HEIGHT);

  renderer.shadowMap.enabled = true;

  container = document.getElementById('world');
  container.appendChild(renderer.domElement);

  window.addEventListener('resize', handleWindowResize, false);

  /*
  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.minPolarAngle = -Math.PI / 2;
  controls.maxPolarAngle = Math.PI ;

  //controls.noZoom = true;
  //controls.noPan = true;
  //*/
}

function handleMouseMove(event) {
  var tx = -1 + (event.clientX / WIDTH)*2;
  var ty = 1 - (event.clientY / HEIGHT)*2;
  mousePos = {x:tx, y:ty};
}

function handleTouchMove(event) {
    event.preventDefault();
    var tx = -1 + (event.touches[0].pageX / WIDTH)*2;
    var ty = 1 - (event.touches[0].pageY / HEIGHT)*2;
    mousePos = {x:tx, y:ty};
}

function handleMouseUp(event){
  if (game.status == "waitingReplay"){
    resetGame();
    hideReplay();
  }
}


function handleTouchEnd(event){
  if (game.status == "waitingReplay"){
    resetGame();
    hideReplay();
  }
}


// SCREEN EVENTS

function handleWindowResize() {
  HEIGHT = window.innerHeight;
  WIDTH = window.innerWidth;
  renderer.setSize(WIDTH, HEIGHT);
  camera.aspect = WIDTH / HEIGHT;
  camera.updateProjectionMatrix();
}

// LIGHTS

var ambientLight, hemisphereLight, shadowLight;

function createLights() {

  hemisphereLight = new THREE.HemisphereLight(0xaaaaaa,0x000000, .9)

  ambientLight = new THREE.AmbientLight(0xdc8874, .5);

  shadowLight = new THREE.DirectionalLight(0xffffff, .9);
  shadowLight.position.set(150, 350, 350);
  shadowLight.castShadow = true;
  shadowLight.shadow.camera.left = -400;
  shadowLight.shadow.camera.right = 400;
  shadowLight.shadow.camera.top = 400;
  shadowLight.shadow.camera.bottom = -400;
  shadowLight.shadow.camera.near = 1;
  shadowLight.shadow.camera.far = 1000;
  shadowLight.shadow.mapSize.width = 4096;
  shadowLight.shadow.mapSize.height = 4096;

  var ch = new THREE.CameraHelper(shadowLight.shadow.camera);

  //scene.add(ch);
  scene.add(hemisphereLight);
  scene.add(shadowLight);
  scene.add(ambientLight);

}

class Pilot {
    constructor() {
      this.mesh = new THREE.Object3D();
      this.mesh.name = "pilot";
      this.angleHairs = 0;
  
      // Body
      const bodyGeom = new THREE.BoxGeometry(15, 15, 15);
      const bodyMat = new THREE.MeshPhongMaterial({ color: Colors.brown, flatShading: true });
      const body = new THREE.Mesh(bodyGeom, bodyMat);
      body.position.set(2, -12, 0);
      this.mesh.add(body);
  
      // Face
      const faceGeom = new THREE.BoxGeometry(10, 10, 10);
      const faceMat = new THREE.MeshLambertMaterial({ color: Colors.pink });
      const face = new THREE.Mesh(faceGeom, faceMat);
      this.mesh.add(face);
  
      // Hair
      const hairGeom = new THREE.BoxGeometry(4, 4, 4);
      const hairMat = new THREE.MeshLambertMaterial({ color: Colors.brown });
      const hair = new THREE.Mesh(hairGeom, hairMat);
      hair.geometry.applyMatrix4(new THREE.Matrix4().makeTranslation(0, 2, 0));
      const hairs = new THREE.Object3D();
  
      this.hairsTop = new THREE.Object3D();
  
      for (let i = 0; i < 12; i++) {
        const h = hair.clone();
        const col = i % 3;
        const row = Math.floor(i / 3);
        const startPosZ = -4;
        const startPosX = -4;
        h.position.set(startPosX + row * 4, 0, startPosZ + col * 4);
        h.geometry.applyMatrix4(new THREE.Matrix4().makeScale(1, 1, 1));
        this.hairsTop.add(h);
      }
  
      hairs.add(this.hairsTop);
  
      const hairSideGeom = new THREE.BoxGeometry(12, 4, 2);
      hairSideGeom.applyMatrix4(new THREE.Matrix4().makeTranslation(-6, 0, 0));
      const hairSideR = new THREE.Mesh(hairSideGeom, hairMat);
      const hairSideL = hairSideR.clone();
      hairSideR.position.set(8, -2, 6);
      hairSideL.position.set(8, -2, -6);
      hairs.add(hairSideR);
      hairs.add(hairSideL);
  
      const hairBackGeom = new THREE.BoxGeometry(2, 8, 10);
      const hairBack = new THREE.Mesh(hairBackGeom, hairMat);
      hairBack.position.set(-1, -4, 0);
      hairs.add(hairBack);
      hairs.position.set(-5, 5, 0);
  
      this.mesh.add(hairs);
  
      // Glasses
      const glassGeom = new THREE.BoxGeometry(5, 5, 5);
      const glassMat = new THREE.MeshLambertMaterial({ color: Colors.brown });
      const glassR = new THREE.Mesh(glassGeom, glassMat);
      glassR.position.set(6, 0, 3);
      const glassL = glassR.clone();
      glassL.position.z = -glassR.position.z;
  
      const glassAGeom = new THREE.BoxGeometry(11, 1, 11);
      const glassA = new THREE.Mesh(glassAGeom, glassMat);
      this.mesh.add(glassR);
      this.mesh.add(glassL);
      this.mesh.add(glassA);
  
      // Ears
      const earGeom = new THREE.BoxGeometry(2, 3, 2);
      const earL = new THREE.Mesh(earGeom, faceMat);
      earL.position.set(0, 0, -6);
      const earR = earL.clone();
      earR.position.set(0, 0, 6);
      this.mesh.add(earL);
      this.mesh.add(earR);
    }
  
    updateHairs() {
      const hairs = this.hairsTop.children;
      const l = hairs.length;
  
      for (let i = 0; i < l; i++) {
        const h = hairs[i];
        h.scale.y = 0.75 + Math.cos(this.angleHairs + i / 3) * 0.25;
      }
  
      this.angleHairs += game.speed * deltaTime * 40;
    }
}

class AirPlane{ 
    constructor() {
    
    this.mesh = new THREE.Object3D();
    
    // Create the cabin 60,50,50,1,1,1
    var geomCockpit = new THREE.BoxGeometry(80,50,50,1,1,1);
    const position = geomCockpit.getAttribute('position'); //Object를 줌.(Float32Array) geomCockpit.index 써보자
    var matCockpit = new THREE.MeshPhongMaterial({color:Colors.red, flatShading:true});
    // 정점 위치를 변경
    geomCockpit.attributes.position.array[13] -= 10; // 4번째 정점의 y 값을 10만큼 감소
    geomCockpit.attributes.position.array[25] -= 10;
    geomCockpit.attributes.position.array[64] -= 10;
    
    geomCockpit.attributes.position.array[14] += 20; // 4번째 정점의 z 값을 20만큼 증가
    geomCockpit.attributes.position.array[26] += 20;
    geomCockpit.attributes.position.array[65] += 20;

    geomCockpit.attributes.position.array[16] -= 10; // 5번째 정점의 y 값을 10만큼 감소
    geomCockpit.attributes.position.array[31] -= 10;
    geomCockpit.attributes.position.array[49] -= 10;    
    
    
    geomCockpit.attributes.position.array[17] -= 20; // 5번째 정점의 z 값을 20만큼 감소
    geomCockpit.attributes.position.array[32] -= 20;
    geomCockpit.attributes.position.array[50] -= 20;

    geomCockpit.attributes.position.array[19] += 30; // 6번째 정점의 y 값을 30만큼 증가
    geomCockpit.attributes.position.array[43] += 30;
    geomCockpit.attributes.position.array[70] += 30;

    geomCockpit.attributes.position.array[20] += 20; // 6번째 정점의 z 값을 20만큼 증가
    geomCockpit.attributes.position.array[44] += 20;
    geomCockpit.attributes.position.array[71] += 20;

    geomCockpit.attributes.position.array[22] += 30; // 7번째 정점의 y 값을 30만큼 증가
    geomCockpit.attributes.position.array[37] += 30;
    geomCockpit.attributes.position.array[55] += 30;

    geomCockpit.attributes.position.array[23] -= 20; // 7번째 정점의 z 값을 20만큼 감소
    geomCockpit.attributes.position.array[38] -= 20;
    geomCockpit.attributes.position.array[56] -= 20;

    // 업데이트
    geomCockpit.attributes.position.needsUpdate = true;

    var cockpit = new THREE.Mesh(geomCockpit, matCockpit);
    cockpit.castShadow = true;
    cockpit.receiveShadow = true;
    this.mesh.add(cockpit);
    
    // Create the engine
    var geomEngine = new THREE.BoxGeometry(20,50,50,1,1,1);
    var matEngine = new THREE.MeshPhongMaterial({color:Colors.white, flatShading:true});
    var engine = new THREE.Mesh(geomEngine, matEngine);
    engine.position.x = 40;
    engine.castShadow = true;
    engine.receiveShadow = true;
    this.mesh.add(engine);
    
    // Create the tail
    var geomTailPlane = new THREE.BoxGeometry(15,20,5,1,1,1);
    var matTailPlane = new THREE.MeshPhongMaterial({color:Colors.red, flatShading:true});
    var tailPlane = new THREE.Mesh(geomTailPlane, matTailPlane);
    tailPlane.position.set(-35,25,0);
    tailPlane.castShadow = true;
    tailPlane.receiveShadow = true;
    this.mesh.add(tailPlane);
    
    // 날개 생성
    const textureLoader = new THREE.TextureLoader();
    const texture = textureLoader.load('./Cat.jpeg', () => {

        // 날개 geometry 생성
        var geomSideWing = new THREE.BoxGeometry(40, 8, 150, 1, 1, 1);

        // 이미지 비율 계산
        let imageAspectRatio = 761 / 760; // 가로 / 세로

        // 텍스처 크기를 줄이기 위한 반복 값 설정
        let repeatX = 2; // 텍스처를 x 방향으로 2번 반복
        let repeatY = 1 * imageAspectRatio; // 텍스처를 y 방향으로 1번 반복 (비율 유지)

        // 텍스처 UV 초기화 및 설정
        let uv = geomSideWing.attributes.uv.array;
        
        // 텍스처 회전을 위한 UV 좌표 조정
        // 윗면
        uv[16] = 0; uv[17] = 0;
        uv[18] = 0; uv[19] = repeatY;
        uv[20] = repeatX; uv[21] = 0;
        uv[22] = repeatX; uv[23] = repeatY;

        // 아랫면
        uv[30] = 0; uv[31] = repeatY;
        uv[28] = 0; uv[29] = 0;
        uv[26] = repeatX; uv[27] = repeatY;
        uv[24] = repeatX; uv[25] = 0;

        geomSideWing.attributes.uv.needsUpdate = true;

        // 재질 생성
        var matTexture = new THREE.MeshPhongMaterial({ map: texture, flatShading: true });

        // BoxGeometry의 각 면에 대한 재질 배열 생성
        var materials = [
            new THREE.MeshPhongMaterial({ color: Colors.blue, flatShading: true }), // 오른쪽 면
            new THREE.MeshPhongMaterial({ color: Colors.blue, flatShading: true }), // 왼쪽 면
            matTexture, // 윗면
            matTexture, // 아랫면
            new THREE.MeshPhongMaterial({ color: Colors.blue, flatShading: true }), // 앞면
            new THREE.MeshPhongMaterial({ color: Colors.blue, flatShading: true })  // 뒷면
        ];

        // 텍스처 반복 설정
        texture.wrapS = THREE.MirroredRepeatWrapping;
        texture.wrapT = THREE.MirroredRepeatWrapping;

        // 텍스처 필터링 설정
        texture.minFilter = THREE.LinearMipmapLinearFilter; // 축소 필터링
        texture.anisotropy = 64; // 안티소트로픽 레벨 설정

        // 텍스처 비율 설정
        texture.repeat.set(repeatX, repeatY);

        var sideWing = new THREE.Mesh(geomSideWing, materials);
        sideWing.castShadow = true;
        sideWing.receiveShadow = true;
        this.mesh.add(sideWing);
    });

    // Create the LeftGun
    var geomLeftGun = new THREE.CylinderGeometry(10,10,80,40,10);
    geomLeftGun.applyMatrix4(new THREE.Matrix4().makeRotationZ(-Math.PI/2));
    var matLeftGun = new THREE.MeshPhongMaterial({color:Colors.red, flatShading:true});
    this.LeftGun = new THREE.Mesh(geomLeftGun, matLeftGun);
    this.LeftGun.position.z = 60;
    this.LeftGun.position.y = -10;
    this.LeftGun.castShadow = true;
    this.LeftGun.receiveShadow = true;
    this.mesh.add(this.LeftGun);

    // Create the RightGun
    var geomRightGun = new THREE.CylinderGeometry(10,10,80,40,10);
    geomRightGun.applyMatrix4(new THREE.Matrix4().makeRotationZ(-Math.PI/2));
    var matRightGun = new THREE.MeshPhongMaterial({color:Colors.red, flatShading:true});
    this.RightGun = new THREE.Mesh(geomRightGun, matRightGun);
    this.RightGun.position.z = -60;
    this.RightGun.position.y = -10;
    this.RightGun.castShadow = true;
    this.RightGun.receiveShadow = true;
    this.mesh.add(this.RightGun);
    
    // propeller
    var geomPropeller = new THREE.BoxGeometry(20,10,10,1,1,1);
    var matPropeller = new THREE.MeshPhongMaterial({color:Colors.brown, flatShading:true});
    this.propeller = new THREE.Mesh(geomPropeller, matPropeller);
    this.propeller.castShadow = true;
    this.propeller.receiveShadow = true;
    
    // blades
    var geomBlade = new THREE.BoxGeometry(1,100,20,1,1,1);
    var matBlade = new THREE.MeshPhongMaterial({color:Colors.brownDark, flatShading:true});
    
    var blade = new THREE.Mesh(geomBlade, matBlade);
    blade.position.set(8,0,0);
    blade.castShadow = true;
    blade.receiveShadow = true;
    this.propeller.add(blade);
    this.propeller.position.set(50,0,0);
    this.mesh.add(this.propeller);

    var wheelProtecGeom = new THREE.BoxGeometry(30,15,10,1,1,1);
    var wheelProtecMat = new THREE.MeshPhongMaterial({color:Colors.red, flatShading:true});
    var wheelProtecR = new THREE.Mesh(wheelProtecGeom,wheelProtecMat);
    wheelProtecR.position.set(25,-20,25);
    this.mesh.add(wheelProtecR);
  
    var wheelTireGeom = new THREE.BoxGeometry(24,24,4);
    var wheelTireMat = new THREE.MeshPhongMaterial({color:Colors.brownDark, flatShading:true});
    var wheelTireR = new THREE.Mesh(wheelTireGeom,wheelTireMat);
    wheelTireR.position.set(25,-28,25);
  
    var wheelAxisGeom = new THREE.BoxGeometry(10,10,6);
    var wheelAxisMat = new THREE.MeshPhongMaterial({color:Colors.brown, flatShading:true});
    var wheelAxis = new THREE.Mesh(wheelAxisGeom,wheelAxisMat);
    wheelTireR.add(wheelAxis);
  
    this.mesh.add(wheelTireR);
  
    var wheelProtecL = wheelProtecR.clone();
    wheelProtecL.position.z = -wheelProtecR.position.z ;
    this.mesh.add(wheelProtecL);
  
    var wheelTireL = wheelTireR.clone();
    wheelTireL.position.z = -wheelTireR.position.z;
    this.mesh.add(wheelTireL);
  
    var wheelTireB = wheelTireR.clone();
    wheelTireB.scale.set(.5,.5,.5);
    wheelTireB.position.set(-35,-5,0);
    this.mesh.add(wheelTireB);
  
    var suspensionGeom = new THREE.BoxGeometry(4,20,4);
    suspensionGeom.applyMatrix4(new THREE.Matrix4().makeTranslation(0,10,0))
    var suspensionMat = new THREE.MeshPhongMaterial({color:Colors.red, flatShading:true});
    var suspension = new THREE.Mesh(suspensionGeom,suspensionMat);
    suspension.position.set(-35,-5,0);
    suspension.rotation.z = -.3;
    this.mesh.add(suspension);
   }
}

class Sphere { 
  constructor() {
      this.mesh = new THREE.Object3D(); // sphere 클래스의 mesh 속성을 Object3D로 초기화
      // Sphere를 나타내는 geometry 생성
      var sphere1 = new THREE.SphereGeometry(15, 32, 16);
      var sphere2 = new THREE.MeshBasicMaterial({ color: 0x00ff00, transparent: true, opacity: 0 });
      var sphere = new THREE.Mesh(sphere1, sphere2);
      sphere.castShadow = false;
      sphere.receiveShadow = false;
      // 생성된 sphere를 sphere의 mesh에 추가
      this.mesh.add(sphere);
  }
}


class Sky {
    constructor() {
    // Create an empty container
    this.mesh = new THREE.Object3D();
    
    // choose a number of clouds to be scattered in the sky
    this.nClouds = 20;
    
    // To distribute the clouds consistently,
    // we need to place them according to a uniform angle
    var stepAngle = Math.PI*2 / this.nClouds;
    
    // create the clouds
    for(var i=0; i<this.nClouds; i++){
        var c = new Cloud();
        var C = new Cloud();
        // set the rotation and the position of each cloud;
        // for that we use a bit of trigonometry
        var a = stepAngle*i; // this is the final angle of the cloud
        var h = game.seaRadius + 150 + Math.random()*200;

        // Trigonometry!!! I hope you remember what you've learned in Math :)
        // in case you don't: 
        // we are simply converting polar coordinates (angle, distance) into Cartesian coordinates (x, y)
        c.mesh.position.y = Math.sin(a)*h;
        c.mesh.position.x = Math.cos(a)*h;

        C.mesh.position.y = Math.sin(a)*h;
        C.mesh.position.x = Math.cos(a)*h;

        // rotate the cloud according to its position
        c.mesh.rotation.z = a + Math.PI/2;
        C.mesh.rotation.z = a + Math.PI/2;

        // for a better result, we position the clouds 
        // at random depths inside of the scene
        c.mesh.position.z = Math.random()*700;
        C.mesh.position.z = -Math.random()*700;
        
        // we also set a random scale for each cloud
        var s = 1+Math.random()*2;
        c.mesh.scale.set(s,s,s);
        C.mesh.scale.set(s,s,s);

        // do not forget to add the mesh of each cloud in the scene
        this.mesh.add(c.mesh);  
        this.mesh.add(C.mesh);  
    }
}  
}

class Sea{
    constructor() {
        var geom = new THREE.CylinderGeometry(game.seaRadius,game.seaRadius,game.seaLength,40,10);
        geom.applyMatrix4(new THREE.Matrix4().makeRotationX(-Math.PI/2));

        let uvBuffer = geom.getAttribute('uv');
        delete uvBuffer.array;
        delete geom.attributes['uv'];

        let normalBuffer = geom.getAttribute('normal'); 
        delete normalBuffer.array;
        delete geom.attributes['normal'];
        //console.log(geom);

        // important: by merging vertices we ensure the continuity of the waves 
        geom = BufferGeometryUtils.mergeVertices(geom);
        geom.computeVertexNormals();
        let positionBuffer = geom.getAttribute('position'); 
        let positions = positionBuffer.array; 
        //console.log(positionBuffer.count);

        // get the vertices
        var l = positionBuffer.count;

        // create an array to store new data associated to each vertex 
        this.waves = [];

        for (var i = 0; i < l; i++){
            // get each vertex
            let v = new THREE.Vector3(positions [3*i + 0], positions [3*i + 1], positions [3*i + 2]);

            // store some data associated to it
            this.waves.push({y:v.y,

                                            x:v.x,
                                            z:v.z,
                                            // a random angle
                                            ang: Math.random()*Math.PI*2,
                                            // a random distance
                                            amp:5 + Math.random()*15,
                                            // a random speed between 0.016 and 0.048 radians / frame 
                                            speed: 0.016 + Math.random()*0.032
                                            });
                                            
        };
        var mat = new THREE.MeshPhongMaterial({
            color:Colors.blue,
            transparent:true,
            opacity:.8,
            flatShading: true,
        });

        this.mesh = new THREE.Mesh(geom, mat); 
        this.mesh.receiveShadow = true;
    }

    moveWaves(){
        // get the vertices
        var positionBuffer = this.mesh.geometry.getAttribute('position'); 
        var l = positionBuffer.count;
        let positions = positionBuffer.array;

        //console.log(verts);

        for (var i = 0; i < l; i++){
            var v = positions [3 * i];

            // get the data associated to it 
            var vprops = this.waves[i];

            // update the position of the vertex
            positions [3 * i + 0] = vprops.x + Math.cos(vprops.ang)*vprops.amp; 
            positions [3 * i + 1] = vprops.y + Math.sin(vprops.ang)*vprops.amp;

            // increment the angle for the next frame 
            vprops.ang += vprops.speed;

        }

        // Tell the renderer that the geometry of the sea has changed. 
        // In fact, in order to maintain the best level of performance,
        // three.js caches the geometries and ignores any changes
        // unless we add this line
        positionBuffer.needsUpdate = true;
        this.mesh.geometry.verticesNeedUpdate=true;
        //sea.mesh.rotation.z += .005;
    }
}

class SeaSphere {
  constructor() {
    this.mesh = new THREE.Object3D(); // sphere 클래스의 mesh 속성을 Object3D로 초기화
    // Sphere를 나타내는 geometry 생성
    var sphere1 = new THREE.SphereGeometry(15, 32, 16);
    var sphere2 = new THREE.MeshBasicMaterial({ color: 0x00ff00, transparent: true, opacity: 0 });
    var sphere = new THREE.Mesh(sphere1, sphere2);
    sphere.castShadow = false;
    sphere.receiveShadow = false;
    // 생성된 sphere를 sphere의 mesh에 추가
    this.mesh.add(sphere);
}
}

class Background {
  constructor() {
    this.mesh = new THREE.Object3D(); // sphere 클래스의 mesh 속성을 Object3D로 초기화
    const geometry = new THREE.SphereGeometry(1500, 60, 40); // 반지름 500, 가로 세로 분할 60x40
    geometry.applyMatrix4(new THREE.Matrix4().makeRotationX(-Math.PI/2));
    geometry.scale(-1, 1, 1); // 구를 내부로 뒤집기

    // TextureLoader를 사용하여 galaxy.jpeg 로드
    const textureLoader = new THREE.TextureLoader();
    const texture = textureLoader.load('./sky.jpg');

    // MeshBasicMaterial을 사용하여 구에 텍스처 적용
    const material = new THREE.MeshBasicMaterial({ map: texture });
    // 구를 씬에 추가
    const sphere = new THREE.Mesh(geometry, material);
    this.mesh.add(sphere);
  }
}

class Cloud {
    constructor() {
      this.mesh = new THREE.Object3D();
      this.mesh.name = "cloud";
  
      const geom = new THREE.BoxGeometry(20, 20, 20);
      const mat = new THREE.MeshPhongMaterial({
        color: Colors.white,
      });
  
      const nBlocs = 3 + Math.floor(Math.random() * 3);
      for (let i = 0; i < nBlocs; i++) {
        const m = new THREE.Mesh(geom.clone(), mat);
        m.position.x = i * 15;
        m.position.y = Math.random() * 10;
        m.position.z = Math.random() * 10;
        m.rotation.z = Math.random() * Math.PI * 2;
        m.rotation.y = Math.random() * Math.PI * 2;
        const s = 0.1 + Math.random() * 0.9;
        m.scale.set(s, s, s);
        this.mesh.add(m);
        m.castShadow = true;
        m.receiveShadow = true;
      }
    }
  
    rotate() {
      const children = this.mesh.children;
      const l = children.length;
      for (let i = 0; i < l; i++) {
        const m = children[i];
        m.rotation.z += Math.random() * 0.005 * (i + 1);
        m.rotation.y += Math.random() * 0.002 * (i + 1);
      }
    }
}

let crash = 0;

class Ennemy {
    constructor() {
      const geom = new THREE.TetrahedronGeometry(10, 0); // Adjust geometry as needed
      const mat = new THREE.MeshPhongMaterial({
        color: 0xff0000, // Example color
        shininess: 0,
        specular: 0xffffff,
        flatShading: true
      });
      this.mesh = new THREE.Mesh(geom, mat);
      this.mesh.castShadow = true;
      this.angle = 0;
      this.distance = 0;
    }
  }
  
  class EnnemiesHolder {
    constructor() {
      this.mesh = new THREE.Object3D();
      this.ennemiesInUse = [];
      this.ennemiesPool = []; // Ensure the pool is initialized
    }
  
    spawnEnnemies() {
      const nEnnemies = game.level;
  
      for (let i = 0; i < nEnnemies * 10; i++) {
        let ennemy;
        if (this.ennemiesPool.length) {
          ennemy = this.ennemiesPool.pop();
        } else {
          ennemy = new Ennemy();
        }
  
        // Debugging logs
        //console.log('Ennemy initialized:', ennemy);
  
        ennemy.angle = - (i * 0.1);
        ennemy.distance = game.seaRadius + game.planeDefaultHeight + (-1 + Math.random() * 2) * (game.planeAmpHeight - 20);
  
        // Check if mesh is defined
        if (ennemy.mesh) {
          ennemy.mesh.position.y = -game.seaRadius + Math.sin(ennemy.angle) * ennemy.distance;
          ennemy.mesh.position.x = Math.cos(ennemy.angle) * ennemy.distance;
          ennemy.mesh.position.z = -300 + Math.random() * 600;
          
          this.mesh.add(ennemy.mesh);
          this.ennemiesInUse.push(ennemy);
        } else {
          console.error('Ennemy mesh is undefined:', ennemy);
        }
      }
    }
  
    rotateEnnemies() {
      for (let i = 0; i < this.ennemiesInUse.length; i++) {
        const ennemy = this.ennemiesInUse[i];
        ennemy.angle += game.speed * deltaTime * game.ennemiesSpeed;
  
        if (ennemy.angle > Math.PI * 2) ennemy.angle -= Math.PI * 2;
  
        ennemy.mesh.position.y = -game.seaRadius + Math.sin(ennemy.angle) * ennemy.distance + 600;
        ennemy.mesh.position.x = Math.cos(ennemy.angle) * ennemy.distance;
        ennemy.mesh.rotation.z += Math.random() * 0.1;
        ennemy.mesh.rotation.y += Math.random() * 0.1;
  
        const diffPos = airplane.mesh.position.clone().sub(ennemy.mesh.position.clone());
        const d = diffPos.length();
        if (d < game.ennemyDistanceTolerance) {
          particlesHolder.spawnParticles(ennemy.mesh.position.clone(), 15, Colors.red, 3);
  
          this.ennemiesPool.unshift(this.ennemiesInUse.splice(i, 1)[0]);
          this.mesh.remove(ennemy.mesh);
          game.planeCollisionSpeedX = 100 * diffPos.x / d;
          game.planeCollisionSpeedY = 100 * diffPos.y / d;
          ambientLight.intensity = 2;
          
          crash = 1;
          executeAfterFrames(() => {
            crash = 0;
          }, 120);
  
          removeEnergy();
          i--;
        } else if (ennemy.angle > Math.PI) {
          this.ennemiesPool.unshift(this.ennemiesInUse.splice(i, 1)[0]);
          this.mesh.remove(ennemy.mesh);
          i--;
        }
      }
    }
  }

class Particle {
    constructor() {
      const geom = new THREE.TetrahedronGeometry(3, 0);
      const mat = new THREE.MeshPhongMaterial({
        color: 0x009999,
        shininess: 0,
        specular: 0xffffff,
        flatShading: true
      });
      this.mesh = new THREE.Mesh(geom, mat);
    }
  
    explode(pos, color, scale) {
      this.mesh.material.color = new THREE.Color(color);
      this.mesh.material.needsUpdate = true;
      this.mesh.scale.set(scale, scale, scale);
      
      const targetX = pos.x + (-1 + Math.random() * 2) * 50;
      const targetY = pos.y + (-1 + Math.random() * 2) * 50;
      const targetZ = pos.z + (-1 + Math.random() * 2) * 50;
      const speed = 0.6 + Math.random() * 0.2;
      
      TweenMax.to(this.mesh.rotation, speed, { x: Math.random() * 12, y: Math.random() * 12 , z: Math.random() * 12 });
      TweenMax.to(this.mesh.scale, speed, { x: 0.1, y: 0.1, z: 0.1 });
      TweenMax.to(this.mesh.position, speed, { 
        x: targetX, 
        y: targetY, 
        z: targetZ, 
        delay: Math.random() * 0.1, 
        ease: Power2.easeOut, 
        onComplete: () => {
          if (this.mesh.parent) {
            this.mesh.parent.remove(this.mesh);
          }
          this.mesh.scale.set(1, 1, 1);
          particlesPool.unshift(this);
        }
      });
    }
  }
  
  class ParticlesHolder {
    constructor() {
      this.mesh = new THREE.Object3D();
      this.particlesInUse = [];
    }
  
    spawnParticles(pos, density, color, scale) {
      for (let i = 0; i < density; i++) {
        let particle;
        if (particlesPool.length) {
          particle = particlesPool.pop();
        } else {
          particle = new Particle();
        }
        this.mesh.add(particle.mesh);
        particle.mesh.visible = true;
        particle.mesh.position.y = pos.y;
        particle.mesh.position.x = pos.x;
        particle.mesh.position.z = pos.z;
        particle.explode(pos, color, scale);
      }
    }
}

class Coin {
    constructor() {
      const geom = new THREE.TetrahedronGeometry(10, 0);
      const mat = new THREE.MeshPhongMaterial({
        color: 0x009999,
        shininess: 0,
        specular: 0xffffff,
        flatShading: true
      });
      this.mesh = new THREE.Mesh(geom, mat);
      this.mesh.castShadow = true;
      this.angle = 0;
      this.dist = 0;
      this.exploding = false; // Add this property to check if the coin is exploding
    }
  }
  
  class CoinsHolder {
    constructor(nCoins) {
      this.mesh = new THREE.Object3D();
      this.coinsInUse = [];
      this.coinsPool = [];
      for (let i = 0; i < nCoins; i++) {
        const coin = new Coin();
        this.coinsPool.push(coin);
      }
    }
  
    spawnCoins() {
      const nCoins = 1 + Math.floor(Math.random() * 10);
      const d = game.seaRadius + game.planeDefaultHeight + (-1 + Math.random() * 2) * (game.planeAmpHeight - 20);
      const amplitude = 10 + Math.round(Math.random() * 10);
      
      for (let i = 0; i < nCoins * 10; i++) {
        let coin;
        if (this.coinsPool.length) {
          coin = this.coinsPool.pop();
        } else {
          coin = new Coin();
        }
        
        this.mesh.add(coin.mesh);
        this.coinsInUse.push(coin);
        coin.angle = - (i * 0.02);
        coin.distance = d + Math.cos(i * 0.5) * amplitude;
        coin.mesh.position.y = -game.seaRadius + Math.sin(coin.angle) * coin.distance;
        coin.mesh.position.x = Math.cos(coin.angle) * coin.distance;
        coin.mesh.position.z = -300 + Math.random() * 600;
      }
    }
  
    rotateCoins() {
      for (let i = 0; i < this.coinsInUse.length; i++) {
        const coin = this.coinsInUse[i];
        if (coin.exploding) continue;
  
        coin.angle += game.speed * deltaTime * game.coinsSpeed;
        if (coin.angle > Math.PI * 2) coin.angle -= Math.PI * 2;
  
        coin.mesh.position.y = -game.seaRadius + Math.sin(coin.angle) * coin.distance + 600;
        coin.mesh.position.x = Math.cos(coin.angle) * coin.distance;
        coin.mesh.rotation.z += Math.random() * 0.1;
        coin.mesh.rotation.y += Math.random() * 0.1;
  
        const diffPos = airplane.mesh.position.clone().sub(coin.mesh.position.clone());
        const d = diffPos.length();
  
        if (d < game.coinDistanceTolerance) {
          this.coinsPool.unshift(this.coinsInUse.splice(i, 1)[0]);
          this.mesh.remove(coin.mesh);
          particlesHolder.spawnParticles(coin.mesh.position.clone(), 5, 0x009999, 0.8);
          addEnergy();
          i--;
        } else if (coin.angle > Math.PI) {
          this.coinsPool.unshift(this.coinsInUse.splice(i, 1)[0]);
          this.mesh.remove(coin.mesh);
          i--;
        }
      }
    }
}
  


// 3D Models
let sea, airplane, sky, coinsHolder, ennemiesHolder, ennemy, particlesHolder, pilot, sphere, seasphere, background;

function createPlane(){
  airplane = new AirPlane();
  airplane.mesh.scale.set(.25,.25,.25);
  scene.add(airplane.mesh);
  
  pilot = new Pilot();
  pilot.mesh.position.y = 35;
  scene.add(pilot.mesh);

  // sphere 객체 생성
  sphere = new Sphere();
  //sphere.mesh.scale.set(1,1,1);
  sphere.mesh.position.y = 108;
  scene.add(sphere.mesh); // sphere.mesh를 scene에 추가

  // 비행기의 mesh에 조종사를 자식으로 추가
  airplane.mesh.add(pilot.mesh);
}

function createBackground(){

  background = new Background();
  background.mesh.position.y = -600;

  scene.add(background.mesh);
}

function createSea(){
  sea = new Sea();
  sea.mesh.position.y = -game.seaRadius;
  scene.add(sea.mesh);

  seasphere = new SeaSphere();
  seasphere.mesh.position.y = -600;
  scene.add(seasphere.mesh);

  // 비행기의 mesh에 조종사를 자식으로 추가
  seasphere.mesh.add(airplane.mesh);

  // 비행기의 mesh에 조종사를 자식으로 추가
  seasphere.mesh.add(camera);
}

function createSky(){
  sky = new Sky();
  sky.mesh.position.y = -game.seaRadius;
  scene.add(sky.mesh);
}

function createCoins(){
  coinsHolder = new CoinsHolder(20);
  scene.add(coinsHolder.mesh)

  seasphere.mesh.add(coinsHolder.mesh);
}

function createEnnemies(){
  for (var i=0; i<10; i++){
    ennemy = new Ennemy();
    ennemiesPool.push(ennemy);
  }
  ennemiesHolder = new EnnemiesHolder();
  //ennemiesHolder.mesh.position.y = -game.seaRadius;
  scene.add(ennemiesHolder.mesh)

  seasphere.mesh.add(ennemiesHolder.mesh);
}

function createParticles(){
  for (var i=0; i<10; i++){
    var particle = new Particle();
    particlesPool.push(particle);
  }
  particlesHolder = new ParticlesHolder();
  //ennemiesHolder.mesh.position.y = -game.seaRadius;
  scene.add(particlesHolder.mesh)
  seasphere.mesh.add(particlesHolder.mesh);
}

function loop(){
  newTime = new Date().getTime();
  deltaTime = newTime-oldTime;
  oldTime = newTime;
  if (game.status=="playing"){

    // Add energy coins every 100m;
    if (Math.floor(game.distance)%game.distanceForCoinsSpawn == 0 && Math.floor(game.distance) > game.coinLastSpawn){
      game.coinLastSpawn = Math.floor(game.distance);
      coinsHolder.spawnCoins();
    }

    if (Math.floor(game.distance)%game.distanceForSpeedUpdate == 0 && Math.floor(game.distance) > game.speedLastUpdate){
      game.speedLastUpdate = Math.floor(game.distance);
      game.targetBaseSpeed += game.incrementSpeedByTime*deltaTime;
    }


    if (Math.floor(game.distance)%game.distanceForEnnemiesSpawn == 0 && Math.floor(game.distance) > game.ennemyLastSpawn){
      game.ennemyLastSpawn = Math.floor(game.distance);
      ennemiesHolder.spawnEnnemies();
    }

    if (Math.floor(game.distance)%game.distanceForLevelUpdate == 0 && Math.floor(game.distance) > game.levelLastUpdate){
      game.levelLastUpdate = Math.floor(game.distance);
      game.level++;
      fieldLevel.innerHTML = Math.floor(game.level);

      game.targetBaseSpeed = game.initSpeed + game.incrementSpeedByLevel*game.level
    }
    updatePlane();
    updateDistance();
    updateEnergy();
    game.baseSpeed += (game.targetBaseSpeed - game.baseSpeed) * deltaTime * 0.02;
    game.speed = game.baseSpeed * game.planeSpeed;

  }else if(game.status=="gameover"){
    game.speed *= .99;
    airplane.mesh.rotation.z += (-Math.PI/2 - airplane.mesh.rotation.z)*.0002*deltaTime;
    airplane.mesh.rotation.x += 0.0003*deltaTime;
    game.planeFallSpeed *= 1.05;
    airplane.mesh.position.y -= game.planeFallSpeed*deltaTime;

    if (airplane.mesh.position.y <-300){
      showReplay();
      game.status = "waitingReplay";

    }
  }else if (game.status=="waitingReplay"){

  }


  airplane.propeller.rotation.x += .2 + game.planeSpeed * deltaTime * .005;
  ambientLight.intensity += (.5 - ambientLight.intensity) * deltaTime * 0.005;

  coinsHolder.rotateCoins();
  ennemiesHolder.rotateEnnemies();

  sea.moveWaves();

  renderer.render(scene, camera);
  requestAnimationFrame(loop);
}

function updateDistance(){
  if (crash === 0) {
    game.distance += game.speed*deltaTime*game.ratioSpeedDistance;
  }
  else if (crash === 1) {
    game.distance -= game.speed*deltaTime*game.ratioSpeedDistance / 2;
  }
  fieldDistance.innerHTML = Math.floor(game.distance);
  var d = 502*(1-(game.distance%game.distanceForLevelUpdate)/game.distanceForLevelUpdate);
  levelCircle.setAttribute("stroke-dashoffset", d);

}

var blinkEnergy=false;

function updateEnergy(){
  game.energy -= game.speed*deltaTime*game.ratioSpeedEnergy;
  game.energy = Math.max(0, game.energy);
  energyBar.style.right = (100-game.energy)+"%";
  energyBar.style.backgroundColor = (game.energy<50)? "#f25346" : "#68c3c0";

  if (game.energy<30){
    energyBar.style.animationName = "blinking";
  }else{
    energyBar.style.animationName = "none";
  }

  if (game.energy <1){
    game.status = "gameover";
  }
}

function addEnergy(){
  game.energy += game.coinValue;
  game.energy = Math.min(game.energy, 100);
}

function removeEnergy(){
  game.energy -= game.ennemyValue;
  game.energy = Math.max(0, game.energy);
}
var startX = 0;
var startY = 700;
var startZ = 0;
var keyboard = {}; // 키보드 입력을 추적하기 위한 객체
var frameCount = 0;  // 프레임 카운트 변수
var currentY = startY;  // 비행기의 현재 Y 위치
var currentZ = startZ;   // 비행기의 현재 Z 위치
var currentX = startX;  // 비행기의 현재 X 위치
var cameraType = 0;
var i = 0;
var Rmax = startZ + 300;
var Lmax = -Rmax;
var Umax = startY + 200;
var Dmax = startY - 70;

// 키가 눌릴 때 실행되는 함수
function onKeyDown(event) {
    keyboard[event.keyCode] = true;
}

// 키가 떼어질 때 실행되는 함수
function onKeyUp(event) {
    keyboard[event.keyCode] = false;
}

function executeAfterFrames(callback, frames) {
    function frameHandler() {
      if (--frames <= 0) {
        callback();
      } else {
        requestAnimationFrame(frameHandler);
      }
    }
    
    requestAnimationFrame(frameHandler);
}

// 이벤트 리스너 등록
document.addEventListener('keydown', onKeyDown);
document.addEventListener('keyup', onKeyUp);
var transitionFrames = 60; // Total frames for the transition
var currentTransitionFrame = 0; // Current frame in the transition
var isTransitioning = false; // Flag to check if a transition is happening
var startPosition = new THREE.Vector3(); // Starting position for the camera transition
var startLookAt = new THREE.Vector3(); // Starting look-at vector for the camera transition
var endPosition = new THREE.Vector3(); // Ending position for the camera transition
var endLookAt = new THREE.Vector3(); // Ending look-at vector f
let rotationX = 0, rotationZ = 0;
let trans = 0;

function updatePlane(){

  if (crash === 0) {
    seasphere.mesh.rotation.z -= .005;
  }
  else if (crash === 1) {
    seasphere.mesh.rotation.z += .001;
    airplane.mesh.rotation.z += .1;
  }
  game.planeSpeed = normalize(0,-.5,.5,game.planeMinSpeed, game.planeMaxSpeed);
  let targetY = currentY;  // 현재 위치를 기본으로 설정
  let targetZ = currentZ;  // 현재 위치를 기본으로 설정
  let targetX = currentX;
  const rotationSpeed = 0.05; // 각도 변경 속도 조절
  const moveDistance = 30; // 키보드 입력에 따라 이동 거리
  const sphereMoveDistance = moveDistance / 10; // 구체 이동 거리
  const easing = 0.1;  // 이동 속도 조절
  var angle = 0; // Initial angle
  var speed = 0.01; // Rotation speed

  game.planeCollisionDisplacementX += game.planeCollisionSpeedX;
  //targetX += game.planeCollisionDisplacementX;
  game.planeCollisionDisplacementY += game.planeCollisionSpeedY;
  //targetY += game.planeCollisionDisplacementY;
  
  airplane.mesh.position.y += (targetY-airplane.mesh.position.y)*deltaTime*game.planeMoveSensivity;
  airplane.mesh.position.x += (targetX-airplane.mesh.position.x)*deltaTime*game.planeMoveSensivity;

  var targetCameraZ = normalize(game.planeSpeed, game.planeMinSpeed, game.planeMaxSpeed, game.cameraNearPos, game.cameraFarPos);
  camera.fov = normalize(0,-1,1,40, 80);


  game.planeCollisionSpeedX += (0-game.planeCollisionSpeedX)*deltaTime * 0.03;
  game.planeCollisionDisplacementX += (0-game.planeCollisionDisplacementX)*deltaTime *0.01;
  game.planeCollisionSpeedY += (0-game.planeCollisionSpeedY)*deltaTime * 0.03;
  game.planeCollisionDisplacementY += (0-game.planeCollisionDisplacementY)*deltaTime *0.01;
  if (crash === 0 && trans === 0){
    // 키보드 입력에 따라 targetY와 targetZ 값을 조정
    if (keyboard[87] && targetY < Umax) {  // 'W' 키
        targetY += moveDistance;
        sphere.mesh.position.y += sphereMoveDistance;
        if (cameraType === 0) camera.position.y += 3;
    }
    if (keyboard[65] && targetZ > Lmax) {  // 'A' 키
        targetZ -= moveDistance;
        sphere.mesh.position.z -= sphereMoveDistance;
        if (cameraType === 0) camera.position.z -= 3;
    }
    if (keyboard[83] && targetY > Dmax) {  // 'S' 키
        targetY -= moveDistance;
        sphere.mesh.position.y -= sphereMoveDistance;
        if (cameraType === 0) camera.position.y -= 3;
    }
    if (keyboard[68] && targetZ < Rmax) {  // 'D' 키
        targetZ += moveDistance;
        sphere.mesh.position.z += sphereMoveDistance;
        if (cameraType === 0) camera.position.z += 3; 
    }


    // 회전을 위한 Quaternion 설정
    const quaternion = new THREE.Quaternion();
    const targetQuaternion = new THREE.Quaternion();
    const axis = new THREE.Vector3();

    if (keyboard[65] || keyboard[87] || keyboard[68] || keyboard[83]) {  // A, W, D, S 키
        rotationX = 0, rotationZ = 0;
        if (keyboard[87]) { // 'W' 키
            rotationZ = -Math.PI / 5; // 위로 기울기
        }
        if (keyboard[65]) { // 'A' 키
            rotationX = -Math.PI / 5; // 왼쪽으로 기울기
        }
        if (keyboard[83]) { // 'S' 키
            rotationZ = Math.PI / 5; // 아래로 기울기
        }
        if (keyboard[68]) { // 'D' 키
            rotationX = Math.PI / 5; // 오른쪽으로 기울기
        }

        // 새로운 회전 계산
        if (keyboard[87] || keyboard[83]) {
            axis.set(0, 0, 1); // Z 축 회전
            targetQuaternion.setFromAxisAngle(axis, rotationZ);
            airplane.mesh.quaternion.slerp(targetQuaternion, rotationSpeed);
        }
        if (keyboard[65] || keyboard[68]) {
            axis.set(1, 0, 0); // X 축 회전
            targetQuaternion.setFromAxisAngle(axis, rotationX);
            airplane.mesh.quaternion.slerp(targetQuaternion, rotationSpeed);
        }
    } else {
        // W, A, S, D 키를 누르지 않았을 때 각도가 0에 가까워질 때까지 서서히 변경
        const resetQuaternion = new THREE.Quaternion();
        airplane.mesh.quaternion.slerp(resetQuaternion, rotationSpeed);
    }
  }
  else if (crash === 1) {
    
    game.planeSpeed = normalize(0,-.5,.5,0, game.planeMaxSpeed);
  }
  // 비행기를 부드럽게 이동시키는 로직 추가 (예: 각 프레임마다 조금씩 이동)
  currentY += (targetY - currentY) * easing;
  currentZ += (targetZ - currentZ) * easing;
  currentX += (targetX - currentX) * easing;

  // 'O' 키를 눌렀을 때의 처리
  if (keyboard[79] && !isTransitioning) {
      if (frameCount % 60 === 0) {
          if (cameraType === 1) {
              cameraType = 0;
              trans = 1;
              TweenMax.to(camera.position, 1, { x: -300, y: currentY + 200, z: currentZ });
              TweenMax.to(camera.rotation, 1, { x: -Math.PI / 2, y: -Math.PI / 3, z: -Math.PI / 2 });
              executeAfterFrames(() => {
                    trans = 0;
              }, 180); 
          } 
          currentTransitionFrame = 0;
      }
      frameCount++;
  } else {
      frameCount = 0;
  }


  // 'P' 키를 눌렀을 때의 처리
  if (keyboard[80] && !isTransitioning) {
      if (frameCount % 60 === 0) {
          if (cameraType === 0) {
              cameraType = 1;
              TweenMax.to(camera.position, 1, { x: 0, y: 1500, z: 0 });
              TweenMax.to(camera.rotation, 1, { x: -Math.PI / 2, y: 0, z: -Math.PI / 2 });
          }
          currentTransitionFrame = 0;
      }
      frameCount++;
  } else {
      frameCount = 0;
  }

  if (isTransitioning) {
      const t = currentTransitionFrame / transitionFrames;
      camera.position.lerpVectors(startPosition, endPosition, t);
      const currentLookAt = new THREE.Vector3().lerpVectors(startLookAt, endLookAt, t);
      camera.lookAt(currentLookAt);
      currentTransitionFrame++;
      if (currentTransitionFrame >= transitionFrames) {
          isTransitioning = false;
      }
  }

  // 비행기를 이동시키는 부분
  airplane.mesh.position.y += (targetY - airplane.mesh.position.y) * easing;
  airplane.mesh.position.z += (targetZ - airplane.mesh.position.z) * easing;
  airplane.mesh.position.x += (targetX - airplane.mesh.position.x) * easing;
  airplane.propeller.rotation.x += 0.3;
}

function showReplay(){
  replayMessage.style.display="block";
}

function hideReplay(){
  replayMessage.style.display="none";
}

function normalize(v,vmin,vmax,tmin, tmax){
  var nv = Math.max(Math.min(v,vmax), vmin);
  var dv = vmax-vmin;
  var pc = (nv-vmin)/dv;
  var dt = tmax-tmin;
  var tv = tmin + (pc*dt);
  return tv;
}

var fieldDistance, energyBar, replayMessage, fieldLevel, levelCircle;

function init(event){

  // UI

  fieldDistance = document.getElementById("distValue");
  energyBar = document.getElementById("energyBar");
  replayMessage = document.getElementById("replayMessage");
  fieldLevel = document.getElementById("levelValue");
  levelCircle = document.getElementById("levelCircleStroke");

  resetGame();
  createScene();
  createLights();
  createPlane();
  createBackground();
  createSea();
  createSky();
  createCoins();
  createEnnemies();
  createParticles();

  document.addEventListener('mousemove', handleMouseMove, false);
  document.addEventListener('touchmove', handleTouchMove, false);
  document.addEventListener('mouseup', handleMouseUp, false);
  document.addEventListener('touchend', handleTouchEnd, false);


  loop();
}

window.addEventListener('load', init, false);