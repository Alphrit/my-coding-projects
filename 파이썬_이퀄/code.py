import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def plot_histogram(image, title):
    # 히스토그램 계산
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    
    # 히스토그램을 그래프로 표시
    plt.plot(hist, color='black')
    plt.title(title)
    plt.xlim([0, 256])
    plt.grid(True)



def  Analysis_and_output_color(num):
    if num == 1:
        img_yuv = img_yuv1
        img_ori = img_ori1
    elif num == 2:
        img_yuv = img_yuv2
        img_ori = img_ori2
    elif num == 3:
        img_yuv = img_yuv3
        img_ori = img_ori3
    elif num == 4:
        img_yuv = img_yuv4
        img_ori = img_ori4
    elif num == 5:
        img_yuv = img_yuv5
        img_ori = img_ori5
    img_yuv_cl = np.copy(img_yuv_list[num-1])
    img_yuv_eq = np.copy(img_yuv_list[num-1])

    # Y 채널 추출
    y_channel = img_yuv[:, :, 0]
    y_channel_cl = img_yuv_cl[:, :, 0]
    y_channel_eq = img_yuv_eq[:, :, 0]

    # CLAHE 객체 생성
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    # CLAHE를 Y 채널에 적용
    clahe_y = clahe.apply(y_channel_cl)
    # Global Histogram Equalization을 Y 채널에 적용
    y_channel_eq = cv2.equalizeHist(y_channel_eq)
    # Y 채널에 적응형 이진화 적용
    y_channel_thresh = cv2.adaptiveThreshold(y_channel, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
    # U와 V 채널 추출
    u_channel = img_yuv[:, :, 1]
    v_channel = img_yuv[:, :, 2]

    # Y 채널을 다시 YUV 이미지에 넣기
    img_yuv_cl[:, :, 0] = clahe_y
    img_yuv_eq[:, :, 0] = y_channel_eq
    # 적응형 이진화된 Y 채널을 다시 YUV 이미지에 넣기
    img_yuv_thresh = np.zeros_like(img_yuv)
    img_yuv_thresh[:, :, 0] = y_channel_thresh
    img_yuv_thresh[:, :, 1] = u_channel
    img_yuv_thresh[:, :, 2] = v_channel

    # YUV 이미지를 BGR 색 공간으로 다시 변환
    img_clahe_yuv = cv2.cvtColor(img_yuv_cl, cv2.COLOR_YUV2BGR)
    img_eq_yuv = cv2.cvtColor(img_yuv_eq, cv2.COLOR_YUV2BGR)
    img_thresh_yuv = cv2.cvtColor(img_yuv_thresh, cv2.COLOR_YUV2BGR)


    # R, G, B 채널 분리
    b_channel, g_channel, r_channel = cv2.split(img_ori)

    # CLAHE를 각 채널에 적용
    clahe_r = clahe.apply(r_channel)
    clahe_g = clahe.apply(g_channel)
    clahe_b = clahe.apply(b_channel)

    # 각 채널에 글로벌 히스토그램 평활화 적용
    r_channel_eq = cv2.equalizeHist(r_channel)
    g_channel_eq = cv2.equalizeHist(g_channel)
    b_channel_eq = cv2.equalizeHist(b_channel)
    # 각 채널에 적응형 이진화 적용
    b_channel_thresh = cv2.adaptiveThreshold(b_channel, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
    g_channel_thresh = cv2.adaptiveThreshold(g_channel, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
    r_channel_thresh = cv2.adaptiveThreshold(r_channel, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)


    # 수정된 채널을 다시 결합
    img_clahe_rgb = cv2.merge((clahe_b, clahe_g, clahe_r))
    img_eq_rgb = cv2.merge((b_channel_eq, g_channel_eq, r_channel_eq))
    img_thresh_rgb = cv2.merge((b_channel_thresh, g_channel_thresh, r_channel_thresh))

    # OpenCV 이미지를 RGB로 변환
    img_final = cv2.cvtColor(img_ori, cv2.COLOR_BGR2RGB)
    img_clahe_yuv_final = cv2.cvtColor(img_clahe_yuv, cv2.COLOR_BGR2RGB)
    img_clahe_rgb_final = cv2.cvtColor(img_clahe_rgb, cv2.COLOR_BGR2RGB)
    img_eq_yuv_final = cv2.cvtColor(img_eq_yuv, cv2.COLOR_BGR2RGB)
    img_eq_rgb_final = cv2.cvtColor(img_eq_rgb, cv2.COLOR_BGR2RGB)
    img_thresh_yuv_final = cv2.cvtColor(img_thresh_yuv, cv2.COLOR_BGR2RGB)
    img_thresh_rgb_final = cv2.cvtColor(img_thresh_rgb, cv2.COLOR_BGR2RGB)


    # cv2.imwrite('./saved_image_clahe.png', img_clahe_rgb_final)
    cv2.imwrite('./saved_image_eq.png', img_eq_rgb_final)
    cv2.imwrite('./saved_image_thresh.png', img_thresh_rgb_final)

    # 결과 이미지 보여주기
    plt.figure(figsize=(20, 10))  # 전체 크기 조정

    # 그리드 스펙 설정 (행, 열, 비율)
    gs = gridspec.GridSpec(6, 3, height_ratios=[3, 1, 3, 1, 3, 1])

    # 원본 이미지
    ax1 = plt.subplot(gs[0, 0])
    plt.imshow(img_final)
    plt.title('Original Image')
    plt.axis('off')

    # 원본 히스토그램
    ax2 = plt.subplot(gs[1, 0])
    plot_histogram(img_final, 'Original Image Histogram')

    # YUV에서 Global Histogram Equalization 적용된 이미지
    ax3 = plt.subplot(gs[0, 1])
    plt.imshow(img_eq_yuv_final)
    plt.title('Global Histogram Equalization Applied (YUV)')
    plt.axis('off')

    # YUV에서 GHE 히스토그램
    ax4 = plt.subplot(gs[1, 1])
    plot_histogram(img_eq_yuv_final, 'GHE Histogram (YUV)')

    # RGB에서 Global Histogram Equalization 적용된 이미지
    ax5 = plt.subplot(gs[0, 2])
    plt.imshow(img_eq_rgb_final)
    plt.title('Global Histogram Equalization Applied (RGB)')
    plt.axis('off')

    # RGB에서 GHE 히스토그램
    ax6 = plt.subplot(gs[1, 2])
    plot_histogram(img_eq_rgb_final, 'GHE Histogram (RGB)')

    # YUV에서 Adaptive Histogram Equalization 적용된 이미지
    ax7 = plt.subplot(gs[2, 1])
    plt.imshow(img_thresh_yuv_final)
    plt.title('Adaptive Histogram Equalization Applied (YUV)')
    plt.axis('off')

    # YUV에서 AHE 히스토그램
    ax8 = plt.subplot(gs[3, 1])
    plot_histogram(img_thresh_yuv_final, 'AHE Histogram (YUV)')

    # RGB에서 Adaptive Histogram Equalization 적용된 이미지
    ax9 = plt.subplot(gs[2, 2])
    plt.imshow(img_thresh_rgb_final)
    plt.title('Adaptive Histogram Equalization Applied (RGB)')
    plt.axis('off')

    # RGB에서 AHE 히스토그램
    ax10 = plt.subplot(gs[3, 2])
    plot_histogram(img_thresh_rgb_final, 'AHE Histogram (RGB)')

    # YUV에서 CLAHE 적용된 이미지
    ax11 = plt.subplot(gs[4, 1])
    plt.imshow(img_clahe_yuv_final)
    plt.title('CLAHE Applied (YUV)')
    plt.axis('off')

    # YUV에서 CLAHE 히스토그램
    ax12 = plt.subplot(gs[5, 1])
    plot_histogram(img_clahe_yuv_final, 'CLAHE Histogram (YUV)')

    # RGB에서 CLAHE 적용된 이미지
    ax13 = plt.subplot(gs[4, 2])
    plt.imshow(img_clahe_rgb_final)
    plt.title('CLAHE Applied (RGB)')
    plt.axis('off')

    # RGB에서 CLAHE 히스토그램
    ax14 = plt.subplot(gs[5, 2])
    plot_histogram(img_clahe_rgb_final, 'CLAHE Histogram (RGB)')

    plt.tight_layout()  # 여백 조정
    plt.show()

def Analysis_and_output_gray(num):
    if num == 1:
        y_channel = y_channel1
        img_rgb_gray = img_rgb_gray1
        img_ori = img_ori1
    elif num == 2:
        y_channel = y_channel2
        img_rgb_gray = img_rgb_gray2
        img_ori = img_ori2
    elif num == 3:
        y_channel = y_channel3
        img_rgb_gray = img_rgb_gray3
        img_ori = img_ori3
    elif num == 4:
        y_channel = y_channel4
        img_rgb_gray = img_rgb_gray4
        img_ori = img_ori4
    elif num == 5:
        y_channel = y_channel5
        img_rgb_gray = img_rgb_gray5
        img_ori = img_ori5
        
    # 1. Global Histogram Equalization
    global_eq_yuv = cv2.equalizeHist(y_channel)
    global_eq_rgb = cv2.equalizeHist(img_rgb_gray)

    # 2. Adaptive Histogram Equalization
    adaptive_eq_yuv = cv2.adaptiveThreshold(y_channel, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    adaptive_eq_rgb = cv2.adaptiveThreshold(img_rgb_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # 3. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_eq_yuv = clahe.apply(y_channel)
    clahe_eq_rgb = clahe.apply(img_rgb_gray)



    # 결과를 출력
    plt.figure(figsize=(30, 15))

    plt.subplot(4, 5, 2)
    plt.imshow(cv2.cvtColor(y_channel, cv2.COLOR_BGR2RGB))
    plt.title('Only Y channel(YUV)')

    plt.subplot(4, 5, 3)
    plt.imshow(global_eq_yuv, cmap='gray')
    plt.title('Global Histogram Equalization')

    plt.subplot(4, 5, 4)
    plt.imshow(adaptive_eq_yuv, cmap='gray')
    plt.title('Adaptive Histogram Equalization')

    plt.subplot(4, 5, 5)
    plt.imshow(clahe_eq_yuv, cmap='gray')
    plt.title('CLAHE')


    plt.subplot(4, 5, 6)
    plt.imshow(cv2.cvtColor(img_ori, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')

    plt.subplot(4, 5, 11)
    plot_histogram(img_ori, 'Original Image Histogram')


    plt.subplot(4, 5, 7)
    plot_histogram(y_channel, 'Only Y channel Histogram')

    plt.subplot(4, 5, 8)
    plot_histogram(global_eq_yuv, 'GHE Histogram')

    plt.subplot(4, 5, 9)
    plot_histogram(adaptive_eq_yuv, 'AHE Histogram')

    plt.subplot(4, 5, 10)
    plot_histogram(clahe_eq_yuv, 'CLAHE Histogram')



    plt.subplot(4, 5, 12)
    plt.imshow(cv2.cvtColor(img_rgb_gray4, cv2.COLOR_BGR2RGB))
    plt.title('Gray Scale(RGB)')

    plt.subplot(4, 5, 13)
    plt.imshow(global_eq_rgb, cmap='gray')
    plt.title('Global Histogram Equalization')

    plt.subplot(4, 5, 14)
    plt.imshow(adaptive_eq_rgb, cmap='gray')
    plt.title('Adaptive Histogram Equalization')

    plt.subplot(4, 5, 15)
    plt.imshow(clahe_eq_rgb, cmap='gray')
    plt.title('CLAHE')


    plt.subplot(4, 5, 17)
    plot_histogram(img_rgb_gray, 'Gray Scale Histogram')

    plt.subplot(4, 5, 18)
    plot_histogram(global_eq_rgb, 'GHE Histogram')

    plt.subplot(4, 5, 19)
    plot_histogram(adaptive_eq_rgb, 'AHE Histogram')

    plt.subplot(4, 5, 20)
    plot_histogram(clahe_eq_rgb, 'CLAHE Histogram')

    plt.show()





# 이미지 파일 경로
image_paths = ['C:\Visual_Studio_Code\Visual_Computing\PowerAde.png', 
               'C:\Visual_Studio_Code\Visual_Computing\Tissue.png', 
               'C:\Visual_Studio_Code\Visual_Computing\Tengen1.png',
               'C:\Visual_Studio_Code\Visual_Computing\Tengen2.png',
               'C:\Visual_Studio_Code\Visual_Computing\Tengen3.png']

# 변환된 이미지를 저장할 변수
img_yuv_list = []
img_rgb_list = []

for i, img_path in enumerate(image_paths):
    img = cv2.imread(img_path)
    
    # 색상 공간 변환 (BGR -> YUV)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    
    # RGB 개별 채널 변환
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    img_yuv_list.append(img_yuv)
    img_rgb_list.append(img_rgb)

img_ori1, img_ori2, img_ori3, img_ori4, img_ori5 = image_paths
img_ori1 = cv2.imread(img_ori1)
img_ori2 = cv2.imread(img_ori2)
img_ori3 = cv2.imread(img_ori3)
img_ori4 = cv2.imread(img_ori4)
img_ori5 = cv2.imread(img_ori5)

img_yuv1, img_yuv2, img_yuv3, img_yuv4, img_yuv5 = img_yuv_list
img_rgb1, img_rgb2, img_rgb3, img_rgb4, img_rgb5 = img_rgb_list


y_channel1, u_channel1, v_channel1 = cv2.split(img_yuv1)
y_channel2, u_channel2, v_channel2 = cv2.split(img_yuv2)
y_channel3, u_channel3, v_channel3 = cv2.split(img_yuv3)
y_channel4, u_channel4, v_channel4 = cv2.split(img_yuv4)
y_channel5, u_channel5, v_channel5 = cv2.split(img_yuv5)

img_rgb_gray1 = cv2.cvtColor(img_rgb1, cv2.COLOR_BGR2GRAY)
img_rgb_gray2 = cv2.cvtColor(img_rgb2, cv2.COLOR_BGR2GRAY)
img_rgb_gray3 = cv2.cvtColor(img_rgb3, cv2.COLOR_BGR2GRAY)
img_rgb_gray4 = cv2.cvtColor(img_rgb4, cv2.COLOR_BGR2GRAY)
img_rgb_gray5 = cv2.cvtColor(img_rgb5, cv2.COLOR_BGR2GRAY)

img_rgb_gray_list = img_rgb_gray1, img_rgb_gray2, img_rgb_gray3, img_rgb_gray4, img_rgb_gray5 

# =============================색상을 처리하는 두 가지 방법 (color space 변환, RGB 개별 채널 변환) 을 통한 방법 비교


# # 원본 이미지 표시
# for i, img_path in enumerate(image_paths):
#     img = cv2.imread(img_path)
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     plt.subplot(6, 5, i + 1)
#     plt.imshow(img_rgb)
#     plt.title(f'Original {i + 1}')
#     plt.axis('off')

# # YUV 이미지 채널 표시
# for i in range(5):
#     # Y 채널 표시
#     plt.subplot(5, 5, 5 + i + 1)
#     plt.imshow(img_yuv_list[i][..., 0])
#     plt.title(f'Y Channel {i + 1}')
#     plt.axis('off')


# for i in range(5):
#     # U 채널 표시
#     plt.subplot(5, 5, 10 + i + 1)
#     plt.imshow(img_yuv_list[i][..., 1])
#     plt.title(f'U Channel {i + 1}')
#     plt.axis('off')


# for i in range(5):
#     # V 채널 표시
#     plt.subplot(5, 5, 15 + i + 1)
#     plt.imshow(img_yuv_list[i][..., 2])
#     plt.title(f'V Channel {i + 1}')
#     plt.axis('off')


# # RGB_gray 이미지 표시
# for i in range(5):
#     plt.subplot(5, 5, 20 + (i + 1) )
#     plt.imshow(img_rgb_gray_list[i])
#     plt.title(f'RGB_gray {i + 1}')
#     plt.axis('off')

# plt.show()
# =============================색상을 처리하는 두 가지 방법 (color space 변환, RGB 개별 채널 변환) 을 통한 방법 비교


# =============================컬러=================================
Analysis_and_output_color(2)
# =============================컬러=================================


# =============================흑백=================================
# Analysis_and_output_gray(5)
# =============================흑백=================================

