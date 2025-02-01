import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'

def resize_img(img): # 이미지의 크기가 1024를 넘으면 1024로 재조정 (숫자가 작을수록 부자연스러운 스티치)
    new_width = 1024
    aspect_ratio = img.shape[0] / img.shape[1]  # 높이 / 너비
    new_height = int(new_width * aspect_ratio)
    resized_image = cv.resize(img, (new_width, new_height), interpolation=cv.INTER_LANCZOS4)
    return resized_image

def calculate_overlap_ratio(binary_mask): # 겹치는 비율(픽셀 수 기반) 계산
    overlap_pixels = np.sum(binary_mask > 0)
    
    total_pixels = binary_mask.shape[0] * binary_mask.shape[1]
    overlap_ratio = overlap_pixels / total_pixels
    return overlap_ratio


def plot_img(rows, cols, index, img, title): # 이미지 출력 함수
    ax = plt.subplot(rows, cols, index)
    if len(img.shape) == 3:
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap='gray')
    plt.axis('off')
    if title:
        plt.title(title)

def visualize_overlap_and_edges_corrected(img1, img2, H):
    # img2의 코너 좌표 변환
    h2, w2 = img2.shape[:2]
    corners_img2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)
    transformed_corners = cv.perspectiveTransform(corners_img2, H)

    # img1의 크기와 변환된 img2의 범위를 포함할 수 있도록 캔버스 크기 계산
    h1, w1 = img1.shape[:2]
    all_corners = np.concatenate((np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]), transformed_corners.reshape(-1, 2)), axis=0)
    [x_min, y_min] = np.int32(all_corners.min(axis=0).ravel())
    [x_max, y_max] = np.int32(all_corners.max(axis=0).ravel())

    # 캔버스 크기 및 이동 오프셋 계산
    stitch_plane_cols = x_max - x_min
    stitch_plane_rows = y_max - y_min
    translation_offset = [-x_min, -y_min]

    # 이동 행렬 생성
    translation_matrix = np.array([[1, 0, translation_offset[0]], [0, 1, translation_offset[1]], [0, 0, 1]])
    H_adjusted = translation_matrix @ H

    # img2 변환
    warped_img2 = cv.warpPerspective(img2, H_adjusted, (stitch_plane_cols, stitch_plane_rows))

    # 윤곽선 검출 (캔버스 크기에 맞게 확장)
    result_visual = np.zeros((stitch_plane_rows, stitch_plane_cols, 3), dtype=np.uint8)
    edges_img1 = cv.Canny(cv.cvtColor(img1, cv.COLOR_BGR2GRAY), 100, 200)
    edges_img1_padded = np.zeros((stitch_plane_rows, stitch_plane_cols), dtype=np.uint8)
    edges_img1_padded[
        translation_offset[1]:translation_offset[1] + h1,
        translation_offset[0]:translation_offset[0] + w1
    ] = edges_img1

    edges_warped_img2 = cv.Canny(cv.cvtColor(warped_img2, cv.COLOR_BGR2GRAY), 100, 200)

    # 겹치는 영역 계산 (그레이스케일 변환 후 마스크 생성)
    warped_img2_gray = cv.cvtColor(warped_img2, cv.COLOR_BGR2GRAY)
    binary_mask1 = np.zeros((stitch_plane_rows, stitch_plane_cols), dtype=np.uint8)
    binary_mask2 = np.zeros((stitch_plane_rows, stitch_plane_cols), dtype=np.uint8)
    binary_mask1[
        translation_offset[1]:translation_offset[1] + h1,
        translation_offset[0]:translation_offset[0] + w1
    ] = 255  # img1의 영역 마스크

    # 수정된 조건: 유효 픽셀 값 확인
    binary_mask2[(warped_img2_gray > 0) & (warped_img2_gray < 255)] = 255

    # 겹치는 영역 계산
    overlap_mask = cv.bitwise_and(binary_mask1, binary_mask2)

    # 윤곽선 흰색, 겹치는 영역 초록색
    result_visual[edges_img1_padded > 0] = [255, 255, 255]
    result_visual[edges_warped_img2 > 0] = [255, 255, 255]
    result_visual[overlap_mask > 0] = [0, 255, 0]

    return result_visual

def blend_images(img1, img2, H):
    print("1. img2의 코너 좌표 변환 중...")
    h2, w2 = img2.shape[:2]
    corners_img2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)
    transformed_corners = cv.perspectiveTransform(corners_img2, H)
    print("1. img2의 코너 좌표 변환 완료.")

    print("2. 캔버스 크기 및 이동 오프셋 계산 중...")
    h1, w1 = img1.shape[:2]
    all_corners = np.concatenate((np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]), transformed_corners.reshape(-1, 2)), axis=0)
    [x_min, y_min] = np.int32(all_corners.min(axis=0).ravel())
    [x_max, y_max] = np.int32(all_corners.max(axis=0).ravel())

    stitch_plane_cols = x_max - x_min
    stitch_plane_rows = y_max - y_min
    translation_offset = [-x_min, -y_min]
    print(f"2. 캔버스 크기: {stitch_plane_cols}x{stitch_plane_rows}, 이동 오프셋: {translation_offset}")

    print("3. 이동 행렬 생성 중...")
    translation_matrix = np.array([[1, 0, translation_offset[0]], [0, 1, translation_offset[1]], [0, 0, 1]])
    H_adjusted = translation_matrix @ H
    print("3. 이동 행렬 생성 완료.")

    print("4. img2 변환 중...")
    result1 = cv.warpPerspective(img2, H_adjusted, (stitch_plane_cols, stitch_plane_rows), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_TRANSPARENT)
    print("4. img2 변환 완료.")

    print("5. img1 배치 중...")
    result2 = np.zeros((stitch_plane_rows, stitch_plane_cols, 3), np.uint8)
    result2[translation_offset[1]:translation_offset[1] + h1, translation_offset[0]:translation_offset[0] + w1] = img1
    print("5. img1 배치 완료.")

    print("6. 겹치는 영역 계산 및 블렌딩 중...")
    overlap_mask = cv.bitwise_and(result1, result2)
    overlap_mask_gray = cv.cvtColor(overlap_mask, cv.COLOR_BGR2GRAY)
    _, binary_mask = cv.threshold(overlap_mask_gray, 1, 255, cv.THRESH_BINARY)

    y_indices, x_indices = np.where(binary_mask > 0)
    if len(x_indices) > 0:
        print("6. 겹치는 영역이 발견되었습니다. 선형 가중치 블렌딩 시작...")

        x_min, x_max = x_indices.min(), x_indices.max()
        gradient = np.linspace(0, 1, x_max - x_min + 1)

        # 블렌딩 영역에 대한 마스크 생성
        blending_mask = np.zeros((stitch_plane_rows, stitch_plane_cols), dtype=np.float32)
        blending_mask[:, x_min:x_max + 1] = gradient[np.newaxis, :]  # 선형 가중치 그라데이션 적용

        # 결과 이미지 생성
        weight1 = blending_mask[..., np.newaxis]  # 채널에 맞게 확장
        weight2 = 1 - weight1

        # NumPy 브로드캐스팅으로 블렌딩 수행
        result3 = (result1 * weight1 + result2 * weight2).astype(np.uint8)
        result3[result2 > 0] = result2[result2 > 0]  # result2 픽셀 보정
        result3[result1 > 0] = result1[result1 > 0]  # result1 픽셀 보정

        print("6. 블렌딩 완료.")
    else:
        print("6. 겹치는 영역이 없어 기본 가중치 블렌딩을 수행합니다.")
        result3 = cv.addWeighted(result1, 0.5, result2, 0.5, 0)

    print("7. 최종 이미지 생성 완료.")
    return result3



for i in range(9, 10):
    if i == 0:
        path1 = './pic/three/0650_1.jpg'
        path2 = './pic/three/0650_2.jpg'
        path3 = './pic/three/0650_3.jpg'
        result_filenames = "0650_result"
        visualize_filenames = "0650_visualize"
    elif i == 1:
        path1 = './pic/three/0710_1.jpg'
        path2 = './pic/three/0710_2.jpg'
        path3 = './pic/three/0710_3.jpg'
        result_filenames = "0710_result"
        visualize_filenames = "0710_visualize"
    elif i == 2:
        path1 = './pic/three/0710_1.jpg'
        path2 = './pic/three/0710_2.jpg'
        path3 = './pic/three/0710_3.jpg'
        result_filenames = "0710_result"
        visualize_filenames = "0710_visualize"
    elif i == 3:
        path1 = './pic/three/0730_1.jpg'
        path2 = './pic/three/0730_2.jpg'
        path3 = './pic/three/0730_3.jpg'
        result_filenames = "0730_result"
        visualize_filenames = "0730_visualize"
    elif i == 4:
        path1 = './pic/three/0740_1.jpg'
        path2 = './pic/three/0740_2.jpg'
        path3 = './pic/three/0740_3.jpg'
        result_filenames = "0740_result"
        visualize_filenames = "0740_visualize"
    elif i == 5:
        path1 = './pic/three/0810_1.jpg'
        path2 = './pic/three/0810_2.jpg'
        path3 = './pic/three/0810_3.jpg'
        result_filenames = "0810_result"
        visualize_filenames = "0810_visualize"
    elif i == 6:
        path1 = './pic/three/img1.jpg'
        path2 = './pic/three/img2.jpg'
        path3 = './pic/three/img3.jpg'
        result_filenames = "img1_result"
        visualize_filenames = "img1_visualize"
    elif i == 7:
        path1 = './pic/three/img4.jpg'
        path2 = './pic/three/img5.jpg'
        path3 = './pic/three/img6.jpg'
        result_filenames = "img4_result"
        visualize_filenames = "img4_visualize"
    elif i == 8:
        path1 = './pic/three/img7.jpg'
        path2 = './pic/three/img8.jpg'
        path3 = './pic/three/img9.jpg'
        result_filenames = "img7_result"
        visualize_filenames = "img7_visualize"
    elif i == 9:
        path1 = './pic/three/img7.jpg'
        path2 = './pic/three/img2.jpg'
        path3 = './pic/three/img6.jpg'
        result_filenames = "house_result"
        visualize_filenames = "house_visualize"

    print(f"{i+1}번째 이미지")

    img1 = cv.imread(path1)
    img2 = cv.imread(path2)
    img3 = cv.imread(path3)


    if img1.shape[1] > 1024 or img1.shape[0] > 1024:
        img1 = resize_img(img1)
    if img2.shape[1] > 1024 or img2.shape[0] > 1024:
        img2 = resize_img(img2)
    if img3.shape[1] > 1024 or img3.shape[0] > 1024:
        img3 = resize_img(img3)

    img1_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    img2_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

    sift = cv.SIFT_create() # SIFT를 사용하여 기능 감지 및 설명자 계산
    kp1, des1 = sift.detectAndCompute(img1_gray, None)
    kp2, des2 = sift.detectAndCompute(img2_gray, None)

    flann = cv.FlannBasedMatcher({"algorithm": 1, "trees": 5}, {"checks": 50})
    matches = flann.knnMatch(des1, des2, k=2)

    # Lowe의 비율 테스트를 적용하여 일치 항목 필터링
    good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

    # 좋은 일치 항목을 사용하여 호모그래피 행렬 찾기
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    try:
        H, _ = cv.findHomography(dst_pts, src_pts, cv.RANSAC, 5.0)
    except:
        print("4개의 대응점을 찾지 못함.")
        quit()

    stitched_img = blend_images(img1, img2, H)

    # 시각화 함수
    visualized_img = visualize_overlap_and_edges_corrected(img1, img2, H)



    # stitched_img 출력
    # print("합성된 이미지의 크기:", stitched_img.shape)

    # 결과 이미지 저장
    plt.figure(figsize=(12, 6))
    plt.axis('off')  # 축 제거
    plt.imshow(cv.cvtColor(stitched_img, cv.COLOR_BGR2RGB))  # OpenCV 이미지를 RGB로 변환하여 출력
    plt.savefig(f"./result/three/{result_filenames}.png", dpi=300, bbox_inches='tight', pad_inches=0)  # 여백 제거
    plt.show()
    plt.close()

    # 시각화 이미지 저장
    plt.figure(figsize=(12, 6))
    plot_img(1, 1, 1, visualized_img, visualize_filenames)
    plt.savefig(f"./result/three/{visualize_filenames}.png", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()


    print("stitched_img와 img3 합성 시작")


    print("img3 resize 완료")

    stitched_img_gray = cv.cvtColor(stitched_img, cv.COLOR_BGR2GRAY)
    img2_gray = cv.cvtColor(img3, cv.COLOR_BGR2GRAY)

    print("stitched_img와 img3 그레이스케일 완료")

    sift = cv.SIFT_create() # SIFT를 사용하여 기능 감지 및 설명자 계산
    kp3, des3 = sift.detectAndCompute(stitched_img_gray, None)
    kp4, des4 = sift.detectAndCompute(img2_gray, None)

    print("stitched_img와 img3 특징점 검출 완료")

    flann2 = cv.FlannBasedMatcher({"algorithm": 1, "trees": 5}, {"checks": 50})
    matches2 = flann2.knnMatch(des3, des4, k=2)

    print("stitched_img와 img3 특징점의 최근접 이웃 발견 완료")

    # Lowe의 비율 테스트를 적용하여 일치 항목 필터링
    good_matches2 = [m for m, n in matches2 if m.distance < 0.7 * n.distance]

    print("stitched_img와 img3 Lowe의 비율 테스트를 적용")

    # 좋은 일치 항목을 사용하여 호모그래피 행렬 찾기
    src_pts2 = np.float32([kp3[m.queryIdx].pt for m in good_matches2]).reshape(-1, 1, 2)
    dst_pts2 = np.float32([kp4[m.trainIdx].pt for m in good_matches2]).reshape(-1, 1, 2)
    try:
        H2, _ = cv.findHomography(dst_pts2, src_pts2, cv.RANSAC, 5.0)
        print("호모그래피 행렬 H 발견")
    except:
        print("4개의 대응점을 찾지 못함.")
        quit()

    stitched_img2 = blend_images(stitched_img, img3, H2)

    print("stitched_img와 img3 blend_images 적용 완료")

    # 시각화 함수
    visualized_img2 = visualize_overlap_and_edges_corrected(stitched_img, img3, H2)

    print("stitched_img와 img3 visualize_overlap_and_edges_corrected 적용 완료")


    result_filenames2 = f"{result_filenames}2"
    visualize_filenames2 = f"{visualize_filenames}2"

    # stitched_img 출력
    # print("합성된 이미지의 크기:", stitched_img.shape)

    # 결과 이미지 저장
    plt.figure(figsize=(12, 6))
    plt.axis('off')  # 축 제거
    plt.imshow(cv.cvtColor(stitched_img2, cv.COLOR_BGR2RGB))  # OpenCV 이미지를 RGB로 변환하여 출력
    plt.savefig(f"./result/three/{result_filenames2}.png", dpi=300, bbox_inches='tight', pad_inches=0)  # 여백 제거
    plt.show()
    plt.close()

    # 시각화 이미지 저장
    plt.figure(figsize=(12, 6))
    plot_img(1, 1, 1, visualized_img2, visualize_filenames2)
    plt.savefig(f"./result/three/{visualize_filenames2}.png", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()