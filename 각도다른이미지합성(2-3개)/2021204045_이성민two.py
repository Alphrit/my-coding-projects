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

def visualize_overlap_and_edges_corrected(img1, img2, H): # 시각화 이미지를 만드는 함수
    stitch_plane_rows = img1.shape[0]
    stitch_plane_cols = img1.shape[1] + img2.shape[1]
    warped_img2 = cv.warpPerspective(img2, H, (stitch_plane_cols, stitch_plane_rows))

    result_visual = np.zeros((stitch_plane_rows, stitch_plane_cols, 3), dtype=np.uint8)

    # 윤곽선 검출 (캔버스 크기에 맞게 확장)
    edges_img1 = cv.Canny(cv.cvtColor(img1, cv.COLOR_BGR2GRAY), 100, 200)
    edges_img1_padded = np.zeros((stitch_plane_rows, stitch_plane_cols), dtype=np.uint8)
    edges_img1_padded[0:img1.shape[0], 0:img1.shape[1]] = edges_img1

    edges_warped_img2 = cv.Canny(cv.cvtColor(warped_img2, cv.COLOR_BGR2GRAY), 100, 200)

    # 겹치는 영역 계산 (그레이스케일 변환 후 마스크 생성)
    warped_img2_gray = cv.cvtColor(warped_img2, cv.COLOR_BGR2GRAY)
    binary_mask1 = np.zeros((stitch_plane_rows, stitch_plane_cols), dtype=np.uint8)
    binary_mask2 = np.zeros((stitch_plane_rows, stitch_plane_cols), dtype=np.uint8)
    binary_mask1[0:img1.shape[0], 0:img1.shape[1]] = 255  # img1의 영역 마스크
    binary_mask2[warped_img2_gray > 0] = 255  # warped_img2의 영역 마스크
    overlap_mask = cv.bitwise_and(binary_mask1, binary_mask2)

    # 윤곽선 흰색, 겹치는 영역 초록색
    result_visual[edges_img1_padded > 0] = [255, 255, 255]
    result_visual[edges_warped_img2 > 0] = [255, 255, 255]
    result_visual[overlap_mask > 0] = [0, 255, 0]

    return result_visual

def blend_images(img1, img2, H): # 이미지 합성 함수
    # 합성된 이미지를 위한 빈 캔버스
    stitch_plane_rows = img1.shape[0]
    stitch_plane_cols = img1.shape[1] + img2.shape[1]
    
    result1 = cv.warpPerspective(img2, H, (stitch_plane_cols, stitch_plane_rows), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_TRANSPARENT)
    
    # img1을 캔버스에 배치
    result2 = np.zeros((stitch_plane_rows, stitch_plane_cols, 3), np.uint8)
    result2[0:img1.shape[0], 0:img1.shape[1]] = img1

    # 중첩 영역 계산
    overlap_mask = cv.bitwise_and(result1, result2)
    overlap_mask_gray = cv.cvtColor(overlap_mask, cv.COLOR_BGR2GRAY)
    _, binary_mask = cv.threshold(overlap_mask_gray, 1, 255, cv.THRESH_BINARY) 

    # 비율 계산
    overlap_ratio = calculate_overlap_ratio(binary_mask)
    print(f"중첩된 영역의 비율: {overlap_ratio * 2:.2%}")  # 비율을 퍼센트로 출력(캔버스가 이미지 크기의 2배이므로 겹치는 비율도 2배)
    
#  ==================================================== 선형 가중치 블렌딩 =========================================
    y_indices, x_indices = np.where(binary_mask > 0)
    if len(x_indices) > 0:  # 겹치는 영역이 있다면
        x_min, x_max = x_indices.min(), x_indices.max()
        gradient = np.linspace(0, 1, x_max - x_min + 1) # 선형 가중치를 적용한 블렌딩
        result3 = np.zeros((stitch_plane_rows, stitch_plane_cols, 3), np.uint8)
        for y in range(stitch_plane_rows):
            for x in range(stitch_plane_cols):
                if binary_mask[y, x] > 0:  # 겹치는 영역
                    weight = gradient[x - x_min]
                    result3[y, x] = np.uint8(result1[y, x] * weight + result2[y, x] * (1 - weight))
                elif x < img1.shape[1]:  # 왼쪽
                    result3[y, x] = result2[y, x]
                else:  # 오른쪽
                    result3[y, x] = result1[y, x]
    else:
        # 겹치는 영역이 없을 경우 단순 합성
        result3 = cv.addWeighted(result1, 0.5, result2, 0.5, 0)
    
    return result3
#  =============================================================================================================
#  ============================================= 단순 가중치 블렌딩 ==============================================
    # result3 = np.zeros((stitch_plane_rows, stitch_plane_cols, 3), np.uint8)
    
    # for y in range(stitch_plane_rows):
    #     for x in range(stitch_plane_cols):
    #         if binary_mask[y, x] > 0:  # 바이너리 마스크를 사용하여 중복 확인
    #             # 겹치는 영역에서 두 이미지를 합성
    #             result3[y, x] = np.uint8(result1[y, x] * 0.5 + result2[y, x] * 0.5) # 이 곳의 숫자를 조절
    #         elif x < img1.shape[1]:  # 겹치는 영역의 왼쪽
    #             result3[y, x] = result2[y, x]
    #         else:  # 겹치는 영역의 오른쪽
    #             result3[y, x] = result1[y, x]
    # return result3
#  =============================================================================================================
for i in range(8):
    if i == 0: # i에 따라 여러 결과 출력
        img1 = cv.imread("./pic/three/0650_1.jpg")
        img2 = cv.imread("./pic/three/0650_2.jpg")
    elif i == 1:
        img1 = cv.imread("./pic/0710_1.jpg")
        img2 = cv.imread("./pic/0710_2.jpg")
    elif i == 2:
        img1 = cv.imread("./pic/0730_1.jpg")
        img2 = cv.imread("./pic/0730_2.jpg")
    elif i == 3:
        img1 = cv.imread("./pic/0740_1.jpg")
        img2 = cv.imread("./pic/0740_2.jpg")
    elif i == 4:
        img1 = cv.imread("./pic/0810_1.jpg")
        img2 = cv.imread("./pic/0810_2.jpg")
    elif i == 5:
        img1 = cv.imread("./pic/img1.jpg")
        img2 = cv.imread("./pic/img4.jpg")
    elif i == 6:
        img1 = cv.imread("./pic/img3.jpg")
        img2 = cv.imread("./pic/img4.jpg")
    elif i == 7:
        img1 = cv.imread("./pic/img5.jpg")
        img2 = cv.imread("./pic/img6.jpg")

    print(f"\n{i + 1}번째 이미지")

    if img1.shape[1] > 1024 or img1.shape[0] > 1024:
        img1 = resize_img(img1)
    if img2.shape[1] > 1024 or img2.shape[0] > 1024:
        img2 = resize_img(img2)

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

    result_filenames = {
        0: "0650_result",
        1: "0710_result",
        2: "0730_result",
        3: "0740_result",
        4: "0810_result",
        5: "img12_result",
        6: "img34_result",
        7: "img56_result"
    }

    visualize_filenames = {
        0: "0650_visualize",
        1: "0710_visualize",
        2: "0730_visualize",
        3: "0740_visualize",
        4: "0810_visualize",
        5: "img12_visualize",
        6: "img34_visualize",
        7: "img56_visualize"
    }

    # stitched_img 출력
    # print("합성된 이미지의 크기:", stitched_img.shape)

    # 결과 이미지 저장
    plt.figure(figsize=(12, 6))
    if i in result_filenames:
        plot_img(1, 1, 1, stitched_img, result_filenames[i])
        plt.savefig(f"./result/{result_filenames[i]}.png", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    # 시각화 이미지 저장
    plt.figure(figsize=(12, 6))
    if i in visualize_filenames:
        plot_img(1, 1, 1, visualized_img, visualize_filenames[i])
        plt.savefig(f"./result/{visualize_filenames[i]}.png", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()