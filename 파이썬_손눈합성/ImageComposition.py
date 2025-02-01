import cv2
import numpy as np
from matplotlib import pyplot as plt

# 이미지 읽기
hand_img = cv2.imread('./hand.jpg')
face_img = cv2.imread('./face.jpg')

# ================================== 기존 hand 이미지를 640 X 640으로 바꾸기 ===================================

# 이미지의 원본 크기
hand_height, hand_width = hand_img.shape[:2]

# 가로 세로 비율 계산
hand_aspect_ratio = hand_width / hand_height

# 이미지 크기 조정 (짧은 쪽을 640으로 맞춤)
if hand_aspect_ratio > 1:
    # 가로가 더 긴 경우, 세로를 640으로 맞추고 가로를 비율에 맞춰 조정
    new_hand_height = 640
    new_hand_width = int(640 * hand_aspect_ratio)
else:
    # 세로가 더 긴 경우, 가로를 640으로 맞추고 세로를 비율에 맞춰 조정
    new_hand_width = 640
    new_hand_height = int(640 / hand_aspect_ratio)


# 이미지 크기 조정
hand_resized_image = cv2.resize(hand_img, (new_hand_width, new_hand_height))

# 중심을 기준으로 640 x 640 크기로 잘라내기
hand_x_center = new_hand_width // 2
hand_y_center = new_hand_height // 2

hand_x_start = hand_x_center - 320
hand_y_start = hand_y_center - 320

hand640X640_img = hand_resized_image[hand_y_start:hand_y_start + 640, hand_x_start:hand_x_start + 640]

# 결과 저장
cv2.imwrite('./hand640X640.jpg', hand640X640_img)
# =================================================================================================================

# =================================== face_img의 eye 부분만 따로 잘라서 저장하기 ====================================

# 눈의 좌표(640 X 640 기준)
eye_x_center, eye_y_center = 500, 1500

# 크기 자르기 (좌상단 좌표, 우하단 좌표 계산)
width, height = 400, 300 # 대충 큰 크기
half_width = width // 2
half_height = height // 2

top_left_x = eye_x_center - half_width
top_left_y = eye_y_center - half_height
bottom_right_x = eye_x_center + half_width
bottom_right_y = eye_y_center + half_height

# 이미지 자르기
eye_img = face_img[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

# 결과 저장
cv2.imwrite('./eye.jpg', eye_img)

# =================================================================================================================

# =================================== 손 가운데 위치에 맞게 눈 위치를 조정 ===========================================

# 손 이미지의 크기와 맞춤. 합성에 필요 없는 부분이니 검정색으로 처리
non_masked_eye_img = np.zeros((640, 640, 3), dtype=np.uint8) 

# 눈 이미지를 삽입할 좌표
insert_x = 160
insert_y = 280

# 눈 이미지의 크기
eye_height, eye_width = eye_img.shape[:2]

# 손 이미지에 삽입할 공간의 끝 좌표
end_x = min(insert_x + eye_width, non_masked_eye_img.shape[1])
end_y = min(insert_y + eye_height, non_masked_eye_img.shape[0])

# 잘라낼 부분 계산
cropped_eye_image = eye_img[0:(end_y - insert_y), 0:(end_x - insert_x)]

# 검은 이미지에 눈 이미지를 삽입
non_masked_eye_img[insert_y:end_y, insert_x:end_x] = cropped_eye_image

# 결과 이미지 저장
cv2.imwrite('./non_masked_eye.jpg', non_masked_eye_img)

# ===================================================================================================================

# =============================== 눈 주위와 손의 피부색을 맞추기 위한 masking 작업(손) ==================================

# hand640X640_img을 hand640X640_debug로 복사
hand640X640_debug = hand640X640_img.copy()

# 기준이 되는 손의 색을 추출할 좌표
hand_center_coords = (360, 460)

# 좌표에 빨간 점 찍기 (디버깅용)
cv2.circle(hand640X640_debug, hand_center_coords, radius=5, color=(0, 0, 255), thickness=-1)

# 색상 추출
hand_center_color = hand640X640_debug[hand_center_coords]

# 색상 범위 설정 (색상이 비슷한 픽셀 찾기)
lower_bound_hand_color = np.maximum(hand_center_color - 40, 0)
upper_bound_hand_color = np.minimum(hand_center_color + 30, 255)

# 마스크 생성
hand_mask = cv2.inRange(hand640X640_debug, lower_bound_hand_color, upper_bound_hand_color)

# 거리 기반 조건 추가: 마스크에서 손 중심과의 거리 계산
height, width, _ = hand640X640_debug.shape
for y in range(height):
    for x in range(width):
        if hand_mask[y, x] != 0:  # 색상이 비슷한 픽셀인 경우
            distance = np.sqrt((x - hand_center_coords[0]) ** 2 + (y - hand_center_coords[1]) ** 2)
            if distance > 130:  # 거리가 130보다 크면 마스크에서 제외
                hand_mask[y, x] = 0

# 마스크에 해당하는 부분의 색상 평균 계산
hand_color = cv2.mean(hand640X640_debug, mask=hand_mask)

# 색상의 평균 출력
print(f"{hand_center_color} 색과 비슷한 픽셀에 대한 평균 색상: {hand_color[:3]}")  # B, G, R 순서로 출력

# 변환할 부분 설정
hand640X640_debug[hand_mask != 0] = (0, 255, 0)  # 초록색

# 결과 출력
cv2.imshow('Image with Red Dot', hand640X640_debug)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ===================================================================================================================

# =============================== 눈 주위와 손의 피부색을 맞추기 위한 masking 작업(눈) ==================================

# non_masked_eye_img을 masked_eye_img로 복사
masked_eye_img = non_masked_eye_img.copy()

# 기준이 되는 얼굴의 색을 추출할 좌표
face_center_coords = (480, 550)

# 색상 추출
face_color = masked_eye_img[face_center_coords]

print(f"{face_center_coords}의 색: {face_color}")

# 색상 범위 설정 (색상이 비슷한 픽셀 찾기)
lower_bound_face_color = np.maximum(face_color - 40, 0)
upper_bound_face_color = np.minimum(face_color + 10, 255)

# 마스크 생성
face_mask = cv2.inRange(masked_eye_img, lower_bound_face_color, upper_bound_face_color)

# 마스크를 확장하기 위해 침식 및 팽창 수행
kernel = np.ones((3, 5), np.uint8)  # 1x3 커널 생성(눈이 양 옆으로 길기 때문에 커널 또한 양 옆으로 길게 설정)
face_mask = cv2.dilate(face_mask, kernel, iterations=1)  # 팽창을 통해 작은 영역을 연결
face_mask = cv2.erode(face_mask, kernel, iterations=1)   # 침식을 통해 원래의 크기로 복원


# 변환할 부분 설정
masked_eye_img[face_mask != 0] = hand_color[:3]  # mean_color의 첫 세 요소 사용


# masked_eye_imgg을 masked_eye_with_red_dot_img로 복사
masked_eye_with_red_dot_img = masked_eye_img.copy()

# 좌표에 빨간 점 찍기(디버깅용)
cv2.circle(masked_eye_with_red_dot_img, face_center_coords, radius=5, color=(0, 0, 255), thickness=-1)

# 결과 출력
cv2.imshow('Masked Eye with Red Dot Image', masked_eye_with_red_dot_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 결과 저장
cv2.imwrite('./masked_eye.jpg', masked_eye_img)

# ===================================================================================================================

# ========================================== Gaussian / Laplacian pyramid 생성 ==========================================
# hand640X640_img에 대한 Gaussian pyramid 생성
GA = hand640X640_img.copy()
gpA = [GA]
for i in range(6):
    GA = cv2.pyrDown(GA)
    gpA.append(GA)

# non_masked_eye_img 대한 Gaussian pyramid 생성
GB = non_masked_eye_img.copy()
gpB = [GB]
for i in range(6):
    GB = cv2.pyrDown(GB)
    gpB.append(GB)

# masked_eye_img 대한 Gaussian pyramid 생성
GC = masked_eye_img.copy()
gpC = [GC]
for i in range(6):
    GC = cv2.pyrDown(GC)
    gpC.append(GC)


# hand640X640_img에 대한 Gaussian Pyramid로 생성된 결과로부터 Laplacian Pyramids를 생성
lpA = [gpA[5]]
for i in range(5, 0, -1):
    GEA = cv2.pyrUp(gpA[i])
    if GEA.shape != gpA[i-1].shape:
        GEA = cv2.resize(GEA, (gpA[i-1].shape[1], gpA[i-1].shape[0]))
    LA = cv2.subtract(gpA[i-1], GEA)
    lpA.append(LA)

# non_masked_eye_img 대한 Gaussian Pyramid로 생성된 결과로부터 Laplacian Pyramids를 생성
lpB = [gpB[5]]
for i in range(5, 0, -1):
    GEB = cv2.pyrUp(gpB[i])
    if GEB.shape != gpB[i-1].shape:
        GEB = cv2.resize(GEB, (gpB[i-1].shape[1], gpB[i-1].shape[0]))
    LB = cv2.subtract(gpB[i-1], GEB)
    lpB.append(LB)

# masked_eye_img 대한 Gaussian Pyramid로 생성된 결과로부터 Laplacian Pyramids를 생성
lpC = [gpC[5]]  # 리스트로 초기화
for i in range(5, 0, -1):
    GEC = cv2.pyrUp(gpC[i])  # 여기서 pyrUp의 결과를 lpC가 아닌 GEC에 저장
    if GEC.shape != gpC[i-1].shape:
        GEC = cv2.resize(GEC, (gpC[i-1].shape[1], gpC[i-1].shape[0]))
    LC = cv2.subtract(gpC[i-1], GEC)
    lpC.append(LC)
# =======================================================================================================================

# ====================== 눈의 위치에 맞게 경계의 위치 설정, 그에 따른 각 피라미드 레벨 결합(non masked) ======================
AB = []

# Laplacian 피라미드의 각 레벨에 이미지의 위쪽과 아래쪽 절반을 추가
for la, lb in zip(lpA, lpB):
    rows, cols, dpt = la.shape
    
    # 위쪽은 손 사진에서, 아래쪽은 눈 사진에서 가져옴
    lsab = np.vstack((la[0:int(rows * 0.6), :], lb[int(rows * 0.6):, :]))
    
    # 남은 눈 사진의 왼쪽 부분을 손 사진으로 채움
    lsab[int(rows * 0.6):, 0:int(cols * 0.4)] = la[int(rows * 0.6):, 0:int(cols * 0.4)]
    
    # 남은 눈 사진의 오른쪽 25% 영역을 손 사진으로 덮음 (눈 사진의 전체 영역 중 오른쪽 25%)
    lsab[:, int(cols * 0.75):] = la[:, int(cols * 0.75):]
    
    # 남은 눈 사진의 아래쪽 20% 영역을 손 사진으로 덮음 (눈 사진의 전체 영역 중 아래쪽 20%)
    lsab[int(rows * 0.8):, :] = la[int(rows * 0.8):, :]
    
    AB.append(lsab)
# =======================================================================================================================

# =================================================== 결합된 이미지 재구성 ===============================================
hand_with_non_masked_eye = AB[0]
for i in range(1, 6):
    hand_with_non_masked_eye = cv2.pyrUp(hand_with_non_masked_eye)
    if hand_with_non_masked_eye.shape != AB[i].shape:
        hand_with_non_masked_eye = cv2.resize(hand_with_non_masked_eye, (AB[i].shape[1], AB[i].shape[0]))
    hand_with_non_masked_eye = cv2.add(hand_with_non_masked_eye, AB[i])

# =======================================================================================================================

# ======================== 눈의 위치에 맞게 경계의 위치 설정, 그에 따른 각 피라미드 레벨 결합(masked) ========================
AC = []

# Laplacian 피라미드의 각 레벨에 이미지의 위쪽과 아래쪽 절반을 추가
for la, lc in zip(lpA, lpC):
    rows, cols, dpt = la.shape
    
    # 위쪽은 손 사진에서, 아래쪽은 눈 사진에서 가져옴
    lsac = np.vstack((la[0:int(rows * 0.6), :], lc[int(rows * 0.6):, :]))
    
    # 남은 눈 사진의 왼쪽 부분을 손 사진으로 채움
    lsac[int(rows * 0.6):, 0:int(cols * 0.4)] = la[int(rows * 0.6):, 0:int(cols * 0.4)]
    
    # 남은 눈 사진의 오른쪽 25% 영역을 손 사진으로 덮음 (눈 사진의 전체 영역 중 오른쪽 25%)
    lsac[:, int(cols * 0.75):] = la[:, int(cols * 0.75):]
    
    # 남은 눈 사진의 아래쪽 20% 영역을 손 사진으로 덮음 (눈 사진의 전체 영역 중 아래쪽 20%)
    lsac[int(rows * 0.8):, :] = la[int(rows * 0.8):, :]
    
    AC.append(lsac)
# =======================================================================================================================

# =================================================== 결합된 이미지 재구성 ===============================================
hand_with_masked_eye = AC[0]
for i in range(1, 6):
    hand_with_masked_eye = cv2.pyrUp(hand_with_masked_eye)
    if hand_with_masked_eye.shape != AC[i].shape:
        hand_with_masked_eye = cv2.resize(hand_with_non_masked_eye, (AC[i].shape[1], AC[i].shape[0]))
    hand_with_masked_eye = cv2.add(hand_with_masked_eye, AC[i])
# =======================================================================================================================

# 이미지 저장
cv2.imwrite('./hand_with_non_masked_eye.jpg', hand_with_non_masked_eye)
cv2.imwrite('./hand_with_masked_eye.jpg', hand_with_masked_eye)


# =========== Image pyramid 기법을 적용하지 않은 합성 사진 hand_with_non_masked_eye_no_GPI_LPI(non masked) =================

# 위쪽은 손 사진에서, 아래쪽은 눈 사진에서 가져옴
hand_with_non_masked_eye_no_GPI_LPI = np.vstack((hand640X640_img[:int(rows * 0.6), :], non_masked_eye_img[int(rows * 0.6):, :]))

# 남은 눈 사진의 왼쪽 부분을 손 사진으로 채움
hand_with_non_masked_eye_no_GPI_LPI[int(rows * 0.6):, 0:int(cols * 0.4)] = hand640X640_img[int(rows * 0.6):, 0:int(cols * 0.4)]

# 남은 눈 사진의 오른쪽 25% 영역을 손 사진으로 덮음 (눈 사진의 전체 영역 중 오른쪽 25%)
hand_with_non_masked_eye_no_GPI_LPI[:, int(cols * 0.75):] = hand640X640_img[:, int(cols * 0.75):]
    
# 남은 눈 사진의 아래쪽 20% 영역을 손 사진으로 덮음 (눈 사진의 전체 영역 중 아래쪽 20%)
hand_with_non_masked_eye_no_GPI_LPI[int(rows * 0.8):, :] = hand640X640_img[int(rows * 0.8):, :]
# =======================================================================================================================

# =============== Image pyramid 기법을 적용하지 않은 합성 사진 hand_with_non_masked_eye_no_GPI_LPI(masked) ================

# 위쪽은 손 사진에서, 아래쪽은 눈 사진에서 가져옴
hand_with_masked_eye_no_GPI_LPI = np.vstack((hand640X640_img[:int(rows * 0.6), :], masked_eye_img[int(rows * 0.6):, :]))

# 남은 눈 사진의 왼쪽 부분을 손 사진으로 채움
hand_with_masked_eye_no_GPI_LPI[int(rows * 0.6):, 0:int(cols * 0.4)] = hand640X640_img[int(rows * 0.6):, 0:int(cols * 0.4)]

# 남은 눈 사진의 오른쪽 25% 영역을 손 사진으로 덮음 (눈 사진의 전체 영역 중 오른쪽 25%)
hand_with_masked_eye_no_GPI_LPI[:, int(cols * 0.75):] = hand640X640_img[:, int(cols * 0.75):]

# 남은 눈 사진의 아래쪽 20% 영역을 손 사진으로 덮음 (눈 사진의 전체 영역 중 아래쪽 20%)
hand_with_masked_eye_no_GPI_LPI[int(rows * 0.8):, :] = hand640X640_img[int(rows * 0.8):, :]
# =======================================================================================================================

# 이미지 저장
cv2.imwrite('./hand_with_non_masked_eye(no_GPI_LPI).jpg', hand_with_non_masked_eye_no_GPI_LPI)
cv2.imwrite('./hand_with_masked_eye(no_GPI_LPI).jpg', hand_with_masked_eye_no_GPI_LPI)

# ===================================================== plt 이미지 1 =====================================================

for i in range(len(gpA)):  # 첫 번째 줄
    b, g, r = cv2.split(gpA[i])  # RGB 채널을 BGR에서 RGB로 변환
    gpA[i] = cv2.merge([r, g, b])
    plt.subplot(6, 7, i + 1), plt.imshow(gpA[i]), plt.title(f'Hand GPI {i}'), plt.xticks([]), plt.yticks([])
    # 이미지 크기 표시
    height, width, _ = gpA[i].shape  # 이미지의 크기 가져오기
    plt.xlabel(f'{width} X {height}')  # 크기를 x축 아래에 표시

for i in range(len(lpA)):  # 두 번째 줄
    b, g, r = cv2.split(lpA[i])
    lpA[i] = cv2.merge([r, g, b])
    plt.subplot(6, 7, i + 8), plt.imshow(lpA[i]), plt.title(f'Hand LPI {i}'), plt.xticks([]), plt.yticks([])
    height, width, _ = lpA[i].shape
    plt.xlabel(f'{width} X {height}')

for i in range(len(gpB)):  # 세 번째 줄
    b, g, r = cv2.split(gpB[i])
    gpB[i] = cv2.merge([r, g, b])
    plt.subplot(6, 7, i + 15), plt.imshow(gpB[i]), plt.title(f'non masked eye GPI {i}'), plt.xticks([]), plt.yticks([])
    # 이미지 크기 표시
    height, width, _ = gpB[i].shape
    plt.xlabel(f'{width} X {height}')

for i in range(len(lpB)):  # 네 번째 줄
    b, g, r = cv2.split(lpB[i])
    lpB[i] = cv2.merge([r, g, b])
    plt.subplot(6, 7, i + 22), plt.imshow(lpB[i]), plt.title(f'non masked eye LPI {i}'), plt.xticks([]), plt.yticks([])
    height, width, _ = lpB[i].shape
    plt.xlabel(f'{width} X {height}')


for i in range(len(gpC)):  # 다섯 번째 줄
    b, g, r = cv2.split(gpC[i])
    gpC[i] = cv2.merge([r, g, b])
    plt.subplot(6, 7, i + 29), plt.imshow(gpC[i]), plt.title(f'masked eye GPI {i}'), plt.xticks([]), plt.yticks([])
    # 이미지 크기 표시
    height, width, _ = gpC[i].shape
    plt.xlabel(f'{width} X {height}')

for i in range(len(lpC)):  # 여섯 번째 줄
    b, g, r = cv2.split(lpC[i])
    lpC[i] = cv2.merge([r, g, b])
    plt.subplot(6, 7, i + 36), plt.imshow(lpC[i]), plt.title(f'masked eye LPI {i}'), plt.xticks([]), plt.yticks([])
    height, width, _ = lpC[i].shape
    plt.xlabel(f'{width} X {height}')

# 서브플롯 사이의 간격 조정
plt.subplots_adjust(hspace=1)  # hspace로 상하 간격을 조정 (값을 증가시키면 간격이 커짐)

plt.show()

# =======================================================================================================================

# ===================================================== plt 이미지 2 =====================================================

b, g, r = cv2.split(hand640X640_img) # RGB 채널을 BGR에서 RGB로 변환
hand640X640_img = cv2.merge([r, g, b])
plt.subplot(3, 3, 1), plt.imshow(hand640X640_img), plt.title('hand640X640'), plt.xticks([]), plt.yticks([])
height, width, _ = hand640X640_img.shape
plt.xlabel(f'{width} X {height}')

b, g, r = cv2.split(non_masked_eye_img)
non_masked_eye_img = cv2.merge([r, g, b])
plt.subplot(3, 3, 2), plt.imshow(non_masked_eye_img), plt.title('non masked eye'), plt.xticks([]), plt.yticks([])
height, width, _ = non_masked_eye_img.shape
plt.xlabel(f'{width} X {height}')


b, g, r = cv2.split(masked_eye_img)
masked_eye_img = cv2.merge([r, g, b])
plt.subplot(3, 3, 3), plt.imshow(masked_eye_img), plt.title('masked eye'), plt.xticks([]), plt.yticks([])
height, width, _ = masked_eye_img.shape
plt.xlabel(f'{width} X {height}')


b, g, r = cv2.split(hand_with_non_masked_eye_no_GPI_LPI)
hand_with_non_masked_eye_no_GPI_LPI = cv2.merge([r, g, b])
plt.subplot(3, 3, 4), plt.imshow(hand_with_non_masked_eye_no_GPI_LPI), plt.title('real'), plt.xticks([]), plt.yticks([])
height, width, _ = hand_with_non_masked_eye_no_GPI_LPI.shape
plt.xlabel(f'{width} X {height}')


b, g, r = cv2.split(hand_with_non_masked_eye)
hand_with_non_masked_eye = cv2.merge([r, g, b])
plt.subplot(3, 3, 5), plt.imshow(hand_with_non_masked_eye), plt.title('hand with non masked eye'), plt.xticks([]), plt.yticks([])
height, width, _ = hand_with_non_masked_eye.shape
plt.xlabel(f'{width} X {height}')

b, g, r = cv2.split(hand_with_masked_eye_no_GPI_LPI)
hand_with_masked_eye_no_GPI_LPI = cv2.merge([r, g, b])
plt.subplot(3, 3, 7), plt.imshow(hand_with_masked_eye_no_GPI_LPI), plt.title('real'), plt.xticks([]), plt.yticks([])
height, width, _ = hand_with_masked_eye_no_GPI_LPI.shape
plt.xlabel(f'{width} X {height}')


b, g, r = cv2.split(hand_with_masked_eye)
hand_with_masked_eye = cv2.merge([r, g, b])
plt.subplot(3, 3, 8), plt.imshow(hand_with_masked_eye), plt.title('hand with masked eye'), plt.xticks([]), plt.yticks([])
height, width, _ = hand_with_masked_eye.shape
plt.xlabel(f'{width} X {height}')


plt.subplots_adjust(hspace=1)  # hspace로 상하 간격을 조정 (값을 증가시키면 간격이 커짐)
plt.show()

# =======================================================================================================================

# 최종 결과 출력
hand_with_masked_eye = cv2.merge([b, g, r])
cv2.imshow('Result Image', hand_with_masked_eye)
cv2.waitKey(0)
cv2.destroyAllWindows()
