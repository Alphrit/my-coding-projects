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