import * as THREE from 'three';
import * as BufferGeometryUtils from './node_modules/three/examples/jsm/utils/BufferGeometryUtils.js';

var Colors = {
    red:0xf25346,
    white:0xd8d0d1,
    brown:0x59332e,
    pink:0xF5986E,
    brownDark:0x23190f,
    blue:0x68c3c0,
};



window.addEventListener('load', init, false);

function init() {
    
    // set up the scene, the camera and the renderer
    createScene();

    // add the lights
    createLights();

    // add the objects
    createPlane();
    createSea();
    createSky();

    // start a loop that will update the objects' positions 
    // and render the scene on each frame
    loop();
}

var scene,
        camera, fieldOfView, aspectRatio, nearPlane, farPlane, HEIGHT, WIDTH,
        renderer, container;

function createScene() {
    // Get the width and the height of the screen,
    // use them to set up the aspect ratio of the camera 
    // and the size of the renderer.
    HEIGHT = window.innerHeight;
    WIDTH = window.innerWidth;

    // Create the scene
    scene = new THREE.Scene();

    // Add a fog effect to the scene; same color as the
    // background color used in the style sheet
    scene.fog = new THREE.Fog(0xf7d9aa, 100, 1500);
    
    // Create the camera
    aspectRatio = WIDTH / HEIGHT;
    fieldOfView = 60;
    nearPlane = 1;
    farPlane = 10000;
    camera = new THREE.PerspectiveCamera(
        fieldOfView,
        aspectRatio,
        nearPlane,
        farPlane
        );
    
    // Set the position of the camera
    camera.position.set(-300, 200, 0);
    camera.lookAt(new THREE.Vector3(0, 0, 0));
    camera.applyMatrix4(new THREE.Matrix4().makeTranslation(0, 0, 0));
    camera.applyMatrix4(new THREE.Matrix4().makeRotationY(0));
    camera.up.set(0, 1, 0);

    //let axisHelper = new THREE.AxesHelper(100);
    //scene.add(axisHelper);


    // Create the renderer
    renderer = new THREE.WebGLRenderer({ 
        // Allow transparency to show the gradient background
        // we defined in the CSS
        alpha: true, 

        // Activate the anti-aliasing; this is less performant,
        // but, as our project is low-poly based, it should be fine :)
        antialias: true 
    });

    // Define the size of the renderer; in this case,
    // it will fill the entire screen
    renderer.setSize(WIDTH, HEIGHT);
    
    // Enable shadow rendering
    renderer.shadowMap.enabled = true;
    
    // Add the DOM element of the renderer to the 
    // container we created in the HTML
    container = document.getElementById('world');
    container.appendChild(renderer.domElement);
    
    // Listen to the screen: if the user resizes it
    // we have to update the camera and the renderer size
    window.addEventListener('resize', handleWindowResize, false);

}

function handleWindowResize() {
    // update height and width of the renderer and the camera
    HEIGHT = window.innerHeight;
    WIDTH = window.innerWidth;
    renderer.setSize(WIDTH, HEIGHT);
    camera.aspect = WIDTH / HEIGHT;
    camera.updateProjectionMatrix();
}

var hemisphereLight, shadowLight;

function createLights() {
    // A hemisphere light is a gradient colored light; 
    // the first parameter is the sky color, the second parameter is the ground color, 
    // the third parameter is the intensity of the light
    hemisphereLight = new THREE.HemisphereLight(0xaaaaaa,0x000000, .9)
    
    // A directional light shines from a specific direction. 
    // It acts like the sun, that means that all the rays produced are parallel. 
    shadowLight = new THREE.DirectionalLight(0xffffff, .9);

    // Set the direction of the light  
    shadowLight.position.set(150, 350, 350);
    
    // Allow shadow casting 
    shadowLight.castShadow = true;

    // define the visible area of the projected shadow
    shadowLight.shadow.camera.left = -400;
    shadowLight.shadow.camera.right = 400;
    shadowLight.shadow.camera.top = 400;
    shadowLight.shadow.camera.bottom = -400;
    shadowLight.shadow.camera.near = 1;
    shadowLight.shadow.camera.far = 1000;

    // define the resolution of the shadow; the higher the better, 
    // but also the more expensive and less performant
    shadowLight.shadow.mapSize.width = 2048;
    shadowLight.shadow.mapSize.height = 2048;
    
    // to activate the lights, just add them to the scene
    scene.add(hemisphereLight);
    scene.add(shadowLight);

    // an ambient light modifies the global color of a scene and makes the shadows softer
    let ambientLight = new THREE.AmbientLight(0xdc8874, .5);
    scene.add(ambientLight);
}

class Sea{
    constructor() {
        var geom = new THREE.CylinderGeometry(600,600,800,40,10);
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
        sea.mesh.rotation.z += .005;
    }
}

class Cloud{ 
    constructor() {
    // Create an empty container that will hold the different parts of the cloud
    this.mesh = new THREE.Object3D();
    
    // create a cube geometry;
    // this shape will be duplicated to create the cloud
    var geom = new THREE.BoxGeometry(20,20,20);
    
    // create a material; a simple white material will do the trick
    var mat = new THREE.MeshPhongMaterial({
        color:Colors.white,  
    });
    
    // duplicate the geometry a random number of times
    var nBlocs = 3+Math.floor(Math.random()*3);
    for (var i=0; i<nBlocs; i++ ){
        
        // create the mesh by cloning the geometry
        var m = new THREE.Mesh(geom, mat); 
        
        // set the position and the rotation of each cube randomly
        m.position.x = i*15;
        m.position.y = Math.random()*10;
        m.position.z = Math.random()*10;
        m.rotation.z = Math.random()*Math.PI*2;
        m.rotation.y = Math.random()*Math.PI*2;
        
        // set the size of the cube randomly
        var s = .1 + Math.random()*.9;
        m.scale.set(s,s,s);
        
        // allow each cube to cast and to receive shadows
        m.castShadow = true;
        m.receiveShadow = true;
        
        // add the cube to the container we first created
        this.mesh.add(m);
    } 
}
}

// Define a Sky Object
class Sky{ 
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
        var h = 750 + Math.random()*200; // this is the distance between the center of the axis and the cloud itself

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

// Now we instantiate the sky and push its center a bit
// towards the bottom of the screen

var sky;

function createSky(){
    sky = new Sky();
    sky.mesh.position.y = 100;
    scene.add(sky.mesh);
}


// Instantiate the sea and add it to the scene:

var sea;

function createSea(){
    sea = new Sea();

    // push it a little bit at the bottom of the scene
    sea.mesh.position.y = -600;

    // add the mesh of the sea to the scene
    scene.add(sea.mesh);
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
    
    // Create the wing
    var geomSideWing = new THREE.BoxGeometry(40,8,150,1,1,1);
    var matSideWing = new THREE.MeshPhongMaterial({color:Colors.red, flatShading:true});
    var sideWing = new THREE.Mesh(geomSideWing, matSideWing);
    sideWing.castShadow = true;
    sideWing.receiveShadow = true;
    this.mesh.add(sideWing);    

    
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

   }
}
class Sphere { 
    constructor() {
        this.mesh = new THREE.Object3D(); // sphere 클래스의 mesh 속성을 Object3D로 초기화

        // Sphere를 나타내는 geometry 생성
        var sphere1 = new THREE.SphereGeometry( 15, 32, 16);
        var sphere2 = new THREE.MeshBasicMaterial({ color: 0x00ff00, transparent: true, opacity: 0 });
        var sphere = new THREE.Mesh(sphere1, sphere2);
        sphere.castShadow = false;
        sphere.receiveShadow = false;
        // 생성된 sphere를 sphere의 mesh에 추가
        this.mesh.add(sphere);
    }
}

var airplane, pilot, sphere;



function createPlane(){ 
    airplane = new AirPlane();
    airplane.mesh.scale.set(.25,.25,.25);
    airplane.mesh.position.y = 100;
    scene.add(airplane.mesh);

    pilot = new Pilot();
    pilot.mesh.position.y = 35;
    scene.add(pilot.mesh);

    // 비행기의 mesh에 조종사를 자식으로 추가
    airplane.mesh.add(pilot.mesh);

    // sphere 객체 생성
    sphere = new Sphere();
    sphere.mesh.scale.set(1,1,1);
    sphere.mesh.position.y = 108;
    scene.add(sphere.mesh); // sphere.mesh를 scene에 추가

    sphere.mesh.add(camera); // 카메라를 비행기에 추가 
    
}

var keyboard = {}; // 키보드 입력을 추적하기 위한 객체
var frameCount = 0;  // 프레임 카운트 변수
var frameCountgun = 0;
var daynightCount = 0;
var dayandnight = 0;
var currentY = 100;  // 비행기의 현재 Y 위치
var currentZ = 0;   // 비행기의 현재 Z 위치
var cameraType = 0;
var i = 0;
var Rmax = 300;
var Lmax = -Rmax;
var Umax = 500;
var Dmax = 70;

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



function updatePlane() {
    let targetY = currentY;  // 현재 위치를 기본으로 설정
    let targetZ = currentZ;  // 현재 위치를 기본으로 설정
    const rotationSpeed = 0.05; // 각도 변경 속도 조절
    const moveDistance = 30; // 키보드 입력에 따라 이동 거리
    const sphereMoveDistance = moveDistance / 10; // 구체 이동 거리
    const easing = 0.1;  // 이동 속도 조절

    // 키보드 입력에 따라 targetY와 targetZ 값을 조정
    if (keyboard[87] && targetY < Umax) {  // 'W' 키
        targetY += moveDistance;
        sphere.mesh.position.y += sphereMoveDistance;
    }
    if (keyboard[65] && targetZ > Lmax) {  // 'A' 키
        targetZ -= moveDistance;
        sphere.mesh.position.z -= sphereMoveDistance;
    }
    if (keyboard[83] && targetY > Dmax) {  // 'S' 키
        targetY -= moveDistance;
        sphere.mesh.position.y -= sphereMoveDistance;
    }
    if (keyboard[68] && targetZ < Rmax) {  // 'D' 키
        targetZ += moveDistance;
        sphere.mesh.position.z += sphereMoveDistance;
    }
    // 회전을 위한 Quaternion 설정
    const quaternion = new THREE.Quaternion();
    const targetQuaternion = new THREE.Quaternion();
    const axis = new THREE.Vector3();

    if (keyboard[65] || keyboard[87] || keyboard[68] || keyboard[83]) {  // A, W, D, S 키
        let rotationX = 0, rotationZ = 0;

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

    // 비행기를 부드럽게 이동시키는 로직 추가 (예: 각 프레임마다 조금씩 이동)
    currentY += (targetY - currentY) * easing;
    currentZ += (targetZ - currentZ) * easing;

    // 'O' 키를 눌렀을 때의 처리
    if (keyboard[79] && !isTransitioning) {
        if (frameCount % 60 === 0) {
            if (cameraType === 1) {
                cameraType = 0;
                sphere.mesh.add(camera);
                startPosition.set(-100, 750 - airplane.mesh.position.y, -airplane.mesh.position.z);
                startLookAt.set(0, 100, 0);
                endPosition.set(-300, 200, 0);
                endLookAt.set(0, airplane.mesh.position.y, airplane.mesh.position.z);
                isTransitioning = true;
                executeAfterFrames(() => {
                    camera.lookAt(0, airplane.mesh.position.y, airplane.mesh.position.z);
                }, 60);
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
                sphere.mesh.remove(camera);
                startPosition.set(-300, 200 + airplane.mesh.position.y, airplane.mesh.position.z);
                startLookAt.set(0, airplane.mesh.position.y, airplane.mesh.position.z);
                endPosition.set(-100, 750, 0);
                endLookAt.set(0, 100, 0);
                isTransitioning = true;
            }
            currentTransitionFrame = 0;
        }
        frameCount++;
    } else {
        frameCount = 0;
    }

    if (isTransitioning) {
        const t = currentTransitionFrame / transitionFrames;
        if (cameraType === 0) {
            if (keyboard[87] && airplane.mesh.position.y < Umax) { // 'W'키
                endLookAt.y += sphereMoveDistance;
            }
            if (keyboard[65] && airplane.mesh.position.z > Lmax) { // 'A'키
                endLookAt.z -= sphereMoveDistance;
            }
            if (keyboard[83] && airplane.mesh.position.y > Dmax) { // 'S'키
                endLookAt.y -= sphereMoveDistance;
            }
            if (keyboard[68] && airplane.mesh.position.z < Rmax) { // 'D'키
                endLookAt.z += sphereMoveDistance;
            }
        }
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
    airplane.propeller.rotation.x += 0.3;
}


function loop(){
    // Rotate the propeller, the sea and the sky
    airplane.propeller.rotation.x += 0.3;
    sky.mesh.rotation.z += .01;

    // update the plane on each frame
    updatePlane();  

    // render the scene
    renderer.render(scene, camera);

    // call the loop function again
    requestAnimationFrame(loop);
    pilot.updateHairs();
    sea.moveWaves();
}

// create a container for the hairs at the top 
// of the head (the ones that will be animated)

class Pilot {
    constructor() {
        this.mesh = new THREE.Object3D();
        this.mesh.name = "pilot";
        this.angleHairs = 0;

        const bodyGeom = new THREE.BoxGeometry(15, 15, 15);
        const bodyMat = new THREE.MeshPhongMaterial({ color: Colors.brown, flatShading: true });
        const body = new THREE.Mesh(bodyGeom, bodyMat);
        body.position.set(2, -12, 0);
        this.mesh.add(body);

        const faceGeom = new THREE.BoxGeometry(10, 10, 10);
        const faceMat = new THREE.MeshLambertMaterial({ color: Colors.pink });
        const face = new THREE.Mesh(faceGeom, faceMat);
        this.mesh.add(face);

        const hairGeom = new THREE.BoxGeometry(4, 4, 4);
        const hairMat = new THREE.MeshLambertMaterial({ color: Colors.brown });
        const hair = new THREE.Mesh(hairGeom, hairMat);
        hair.geometry.translate(0, 2, 0);

        this.hairsTop = new THREE.Object3D();
        for (let i = 0; i < 12; i++) {
            const h = hair.clone();
            const col = i % 3;
            const row = Math.floor(i / 3);
            const startPosZ = -4;
            const startPosX = -4;
            h.position.set(startPosX + row * 4, 0, startPosZ + col * 4);
            this.hairsTop.add(h);
        }

        const hairSideGeom = new THREE.BoxGeometry(12, 4, 2).translate(-6, 0, 0);
        const hairSideR = new THREE.Mesh(hairSideGeom, hairMat);
        const hairSideL = hairSideR.clone();
        hairSideR.position.set(8, -2, 6);
        hairSideL.position.set(8, -2, -6);

        const hairBackGeom = new THREE.BoxGeometry(2, 8, 10);
        const hairBack = new THREE.Mesh(hairBackGeom, hairMat);
        hairBack.position.set(-1, -4, 0);

        this.hairsTop.position.set(-5, 5, 0);
        this.mesh.add(this.hairsTop);

        const glassGeom = new THREE.BoxGeometry(5, 5, 5);
        const glassMat = new THREE.MeshLambertMaterial({ color: Colors.brown });
        const glassR = new THREE.Mesh(glassGeom, glassMat);
        glassR.position.set(6, 0, 3);
        const glassL = glassR.clone();
        glassL.position.z = -glassR.position.z;

        const glassAGeom = new THREE.BoxGeometry(11, 1, 11);
        const glassA = new THREE.Mesh(glassAGeom, glassMat);

        const earGeom = new THREE.BoxGeometry(2, 3, 2);
        const earL = new THREE.Mesh(earGeom, faceMat);
        earL.position.set(0, 0, -6);
        const earR = earL.clone();
        earR.position.set(0, 0, 6);

        this.mesh.add(glassR, glassL, glassA, earL, earR, hairSideR, hairSideL, hairBack);
    }

    updateHairs() {
        const hairs = this.hairsTop.children;
        for (let i = 0; i < hairs.length; i++) {
            const h = hairs[i];
            h.scale.y = 0.75 + Math.cos(this.angleHairs + i / 3) * 0.25;
        }
        this.angleHairs += 0.16;
    }
}
