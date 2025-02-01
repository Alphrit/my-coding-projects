import pygetwindow as gw
import pyautogui
import random
import time
import pyautogui
import math
import cv2
import numpy as np
import copy
from PIL import Image

def click(hr) : # 매크로 감지에 걸리지 않게 주어진 좌표 안에서 랜덤 클릭하는 함수
    pyautogui.moveTo(random.uniform(hr[0], hr[2]), random.uniform(hr[1], hr[3]))
    pyautogui.doubleClick()
    
# 좌표 간의 거리 계산 함수
def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# line_macrotree_coords 재정렬
def reorder_macrotree_coords(previous_coords, current_coords):
    reordered_coords = {}
    used_coords = set()  # 이미 매칭된 current_coords를 중복 사용하지 않기 위한 집합

    for previous_key, previous_value in previous_coords.items():
        min_distance = float('inf')
        closest_key = None

        # current_coords에서 이전 값과 가장 가까운 값을 찾음
        for current_key, current_value in current_coords.items():
            if current_key not in used_coords:
                distance = calculate_distance(previous_value[:2], current_value[:2])
                if distance < min_distance:
                    min_distance = distance
                    closest_key = current_key

        # 가장 가까운 current_coords 항목을 이전 항목에 매칭하고, 재정렬 리스트에 추가
        reordered_coords[previous_key] = current_coords[closest_key]
        used_coords.add(closest_key)

    return reordered_coords

# 창 크기와 위치
window = pyautogui.getActiveWindow()

window_title = 'NoxPlayer' # 매크로를 돌릴 때 실행되어 있을 게임 프로그램 이름. 이 이름의 창이 켜져 있어야 프로그램이 실행됨.

# 모든 창 목록을 가져옵니다.
windows = gw.getWindowsWithTitle(window_title)


if windows:
    window = windows[0]
    image_path = f"C:/Visual_Studio_Code/GrowCastle/file/{1}.png" # 각 변수의 좌표 할당을 위한 사진 사이즈 제시
    image = cv2.imread(image_path)

    height, width, channels = image.shape
    start_coords = (0, 0)
    end_coords = (0, 0)
    midpoint_color = (127, 165, 189) # GBR 기준
    background_color = (73, 87, 98) # GBR 기준
    movecount = 0
    lastvector = False

    converted_macrotree_coords = {
            'macrotree1': (width * 0.6468, height * 0.1306), 
            'macrotree2': (width * 0.6468, height * 0.3806), 
            'macrotree3': (width * 0.6468, height * 0.6306), 
            'macrotree4': (width * 0.4931, height * 0.7164), 
            'macrotree5': (width * 0.3440, height * 0.6306), 
            'macrotree6': (width * 0.3440, height * 0.3806), 
            'macrotree7': (width * 0.3440, height * 0.1306), 
            'macrotree8': (width * 0.4931, height * 0.0485)
    }
    macrobar = (((window.width)*0.2635)+window.left, 
                ((window.height)*0.2767)+window.top, 
                ((window.width)*0.7026)+window.left, 
                ((window.height)*0.7465)+window.top)

    macrobarstart = (((window.width)*0.6447)+window.left, 
                ((window.height)*0.7698)+window.top, 
                ((window.width)*0.7403)+window.left, 
                ((window.height)*0.8418)+window.top)

    macrotree_click_coords = { # macrotree 클릭을 위한 좌표
        'macrotree1': (((window.width)*0.5444) + window.left + ((window.width)*0.01), 
                ((window.height)*0.4112)+window.top), 
        'macrotree2': (((window.width)*0.5644)+window.left + ((window.width)*0.01), 
                ((window.height)*0.5237)+window.top), 
        'macrotree3': (((window.width)*0.5444)+window.left + ((window.width)*0.01), 
                ((window.height)*0.6441)+window.top), 
        'macrotree4': (((window.width)*0.4779)+window.left + ((window.width)*0.01), 
                ((window.height)*0.6810)+window.top), 
        'macrotree5': (((window.width)*0.4106)+window.left + ((window.width)*0.01), 
                ((window.height)*0.6441)+window.top), 
        'macrotree6': (((window.width)*0.3897)+window.left + ((window.width)*0.01), 
                ((window.height)*0.5237)+window.top), 
        'macrotree7': (((window.width)*0.4106)+window.left + ((window.width)*0.01), 
                ((window.height)*0.4112)+window.top), 
        'macrotree8': (((window.width)*0.4779)+window.left + ((window.width)*0.01), 
                ((window.height)*0.3638)+window.top)
    }



    previous_macrotree_midpoint_coords = { # 직전 사진의 중점 좌표 정보. 또한, 최초 macrotree 중점 설정.
                'macrotree1': (283, 76),
                'macrotree2': (305, 143),
                'macrotree3': (282, 210),
                'macrotree4': (215, 232), 
                'macrotree5': (148, 210),
                'macrotree6': (126, 143), 
                'macrotree7': (149, 76), 
                'macrotree8': (216, 52)
        }

    macrotree_coords = { # 현 사진의 좌표 정보.
            'macrotree1': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'macrotree2': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'macrotree3': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'macrotree4': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
            'macrotree5': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'macrotree6': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
            'macrotree7': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
            'macrotree8': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    }
    previous_macrotree_coords = { # 직전 사진의 좌표 정보. 
            'macrotree1': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'macrotree2': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'macrotree3': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'macrotree4': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
            'macrotree5': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'macrotree6': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
            'macrotree7': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
            'macrotree8': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    }



    # ==============================================================분석을 위한 사진을 연속적으로 찍음==============================================================
    # 저장할 이미지 수
    num_images = 80

    screenshot = pyautogui.screenshot()
    # 지정된 영역 잘라내기
    cropped_image = screenshot.crop((macrobar))
        
    # 이미지 저장
    cropped_image.save(f"C:/Visual_Studio_Code/GrowCastle/file/1.png")
        
    click(macrobarstart)

    # 이미지 생성 및 저장
    for i in range(num_images):
        # 전체 화면 스크린샷 찍기
        screenshot = pyautogui.screenshot()

        # 지정된 영역 잘라내기
        cropped_image = screenshot.crop((macrobar))

        # 이미지 저장
        cropped_image.save(f"C:/Visual_Studio_Code/GrowCastle/file/{i + 1}.png")


    # ==============================================================찍은 사진의 일부(8 ~ 25)를 분석==============================================================

    for i in range(8, 23):
        # 이미지 경로 설정
        image_path = f"C:/Visual_Studio_Code/GrowCastle/file/{i}.png"

        # 이미지 읽기
        image = cv2.imread(image_path)
        print(converted_macrotree_coords)

        # 목표 색상과 허용 오차 설정
        target_color = np.array([(145, 194, 214)])
        diamond_color = np.array([(247, 195, 63)])
        tolerance = 15
        tolerance2 = 100

        # 색상의 상한과 하한 설정
        lower_bound = target_color - tolerance
        upper_bound = target_color + tolerance

        lower_diamond_bound = diamond_color - tolerance2
        upper_diamond_bound = diamond_color + tolerance2

        # 이미지에서 목표 색상과 가까운 부분 마스크 생성
        mask = cv2.inRange(image, lower_bound, upper_bound)
        diamond_mask = cv2.inRange(image, lower_diamond_bound, upper_diamond_bound)

        # 마스크된 영역을 초록색으로 변경
        image[mask != 0] = [0, 255, 0]
        image[diamond_mask != 0] = [0, 0, 0]

        # BGR에서 HSV로 변환
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 마스크에서 초록색 뭉치 찾기
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        diamondcontours, _ = cv2.findContours(diamond_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 최소 면적 필터 (160보다 큰 뭉치만)
        min_area = 130


        # 검정색 뭉치들의 중심 좌표 계산 및 출력
        count_black_blobs = 0
        for contour in diamondcontours:
            area = cv2.contourArea(contour)
            if area >= min_area:
                count_black_blobs += 1
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # print(f"검정색 뭉치의 중심 좌표: ({cX}, {cY})")
                    cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
                else:
                    # print("중심을 계산할 수 없는 뭉치가 있습니다.")
                    pass

        # print(f"넓이가 {min_area} 이상인 검정색 뭉치의 개수: {count_black_blobs}")


        # 초록색 뭉치가 7개 미만이라면 루프를 끝냄
        count = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_area:
                count += 1
        if count < 7:
            break

        count = 0
        # 초록색 뭉치의 좌표 표시
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_area:
                count += 1
                # 뭉치의 좌표들 중에서 가장 왼쪽과 가장 오른쪽 좌표 찾기
                leftmost = tuple(map(int, contour[contour[:, :, 0].argmin()][0]))  # 가장 왼쪽 x 좌표
                rightmost = tuple(map(int, contour[contour[:, :, 0].argmax()][0]))  # 가장 오른쪽 x 좌표
                # 가장 위쪽과 아래쪽 좌표 찾기
                topmost = tuple(map(int, contour[contour[:, :, 1].argmin()][0]))    # 가장 위쪽 y 좌표
                bottommost = tuple(map(int, contour[contour[:, :, 1].argmax()][0])) # 가장 아래쪽 y 좌표

                if calculate_distance(topmost, bottommost) > calculate_distance(leftmost, rightmost):
                    leftmost, rightmost = topmost, bottommost

                # 가장 왼쪽 좌표에 빨간색 점 표시
                cv2.circle(image, leftmost, 5, (count * 30, count * 30, 255), -1)
                # 가장 오른쪽 좌표에 빨간색 점 표시
                cv2.circle(image, rightmost, 5, (count * 30, count * 30, 255), -1)
                # 왼쪽과 오른쪽을 잇는 빨간색 선 그리기
                cv2.line(image, leftmost, rightmost, (count * 30, count * 30, 255), 2)

                # 선의 중점 계산
                midpoint = ((leftmost[0] + rightmost[0]) // 2, (leftmost[1] + rightmost[1]) // 2)
                
                # 중점에 빨간색 점 표시
                cv2.circle(image, midpoint, 5, (count * 30, count * 30, 255), -1)


                # 선의 각도 계산 (atan2 사용)
                dx = rightmost[0] - leftmost[0]
                dy = rightmost[1] - leftmost[1]
                angle = math.atan2(dy, dx)  # 각도 (라디안 단위)
                
                # 수직 방향으로 선을 그리기 위한 각도 계산 (현재 각도에서 90도 회전)
                perpendicular_angle = angle + math.pi / 2  # 90도 (라디안) 추가
                
                # 30 픽셀 떨어진 좌표 계산 (중점에서 수직으로)
                offset_x = int(23 * math.cos(perpendicular_angle))
                offset_y = int(23 * math.sin(perpendicular_angle))
                
                # 새로운 좌표 계산
                new_point = (midpoint[0] + offset_x, midpoint[1] + offset_y)
                new_point2 = (midpoint[0] - offset_x, midpoint[1] - offset_y)
                

                rgb_color1 = image[new_point[1], new_point[0]]
                rgb_color2 = image[new_point2[1], new_point2[0]]

                
                distance1 = np.linalg.norm(midpoint_color - rgb_color1)
                distance2 = np.linalg.norm(midpoint_color - rgb_color2)

                # print(f"{new_point}의 색: {rgb_color1}, {new_point2}의 색: {rgb_color2}")
                if  np.array_equal(rgb_color1, background_color) or np.array_equal(rgb_color2, background_color):
                    if np.array_equal(rgb_color1, background_color):
                        new_point, new_point2 = new_point2, new_point
                        rgb_color1, rgb_color2 = rgb_color2, rgb_color1
                elif not np.array_equal(rgb_color1, background_color) and not np.array_equal(rgb_color2, background_color):
                    # 더 가까운 색상 출력
                    if distance1 > distance2:
                        # print("바꾸기 실행")
                        new_point, new_point2 = new_point2, new_point
                        rgb_color1, rgb_color2 = rgb_color2, rgb_color1
                    # print(f"중심 색: {rgb_color1}, 바깥쪽 색: {rgb_color2}")

                if np.all(rgb_color1 == rgb_color2):
                    # Initialize minimum distances
                    min_distance_new_point = float('inf')
                    min_distance_new_point2 = float('inf')

                    # Compare distances
                    for name, coords in previous_macrotree_midpoint_coords.items():
                        distance_to_new_point = calculate_distance(coords, new_point)
                        distance_to_new_point2 = calculate_distance(coords, new_point2)
                        
                        min_distance_new_point = min(min_distance_new_point, distance_to_new_point)
                        min_distance_new_point2 = min(min_distance_new_point2, distance_to_new_point2)

                    # Determine which new point is closer
                    if min_distance_new_point > min_distance_new_point2:
                        new_point, new_point2 = new_point2, new_point
                        rgb_color1, rgb_color2 = rgb_color2, rgb_color1
                
                cv2.circle(image, new_point2, 5, (0, 0, 0), -1)
                cv2.line(image, midpoint, new_point2, (0, 0, 0), 2)

        
                
                # 좌표 출력 (중심 좌표)
                # print(f'뭉치 {count}: 가장 왼쪽 좌표 = {leftmost}, 가장 오른쪽 좌표 = {rightmost}, 중점 = {midpoint}, 중심 = {new_point}, 중심의 색 = {rgb_color1}')

                # new_point와 가장 가까운 previous_macrotree_midpoint_coords 찾기
                min_distance = float('inf')
                close_macrotree = None
                
                for macrotree, prev_midpoint in previous_macrotree_midpoint_coords.items():
                    distance = calculate_distance(new_point, prev_midpoint)
                    if distance < min_distance:
                        min_distance = distance
                        close_macrotree = macrotree

                # 가장 가까운 macrotree 항목에 좌표 저장
                if close_macrotree:
                    macrotree_coords[close_macrotree] = (
                        leftmost[0], leftmost[1], rightmost[0], rightmost[1],
                        midpoint[0], midpoint[1], new_point[0], new_point[1]
                    )



        
        
        if movecount > 0:
            movecount += 1
        # 결과 macrotree_coords 출력
        # print("업데이트된 macrotree_coords:")
        # for macrotree, coords in macrotree_coords.items():
        #     print(f'{macrotree}: {coords}')

        # cv2.circle(image, (macrotree_coords['macrotree6'][6], macrotree_coords['macrotree6'][7]), 5, (0, 0, 0), -1)

        # 초록색 뭉치의 개수 출력
        # print(f'초록색 뭉치의 개수: {count}')


        previous_macrotree_midpoint_coords = {}
        # macrotree_coords의 7번째, 8번째 값으로 previous_macrotree_midpoint_coords 업데이트
        for key, value in macrotree_coords.items():
            previous_macrotree_midpoint_coords[key] = (value[6], value[7])

        # 결과 macrotree_coords 출력
        # print("업데이트된 macrotree_coords:")
        # for macrotree, coords in previous_macrotree_midpoint_coords.items():
        #     print(f'{macrotree}: {coords}')


        if count_black_blobs >= 1:
            min_distance = float('inf')
            closest_macrotree = None

            for i in range(1, 9):  # macrotree1 ~ macrotree8 반복
                macrotree_name = f'macrotree{i}'
                macrotree_point = (macrotree_coords[macrotree_name][6], macrotree_coords[macrotree_name][7])

                # 거리 계산
                distance = calculate_distance((cX, cY), macrotree_point)
                
                # 가장 가까운 macrotree 찾기
                if distance < min_distance:
                    min_distance = distance
                    closest_macrotree = macrotree_name

            diamond_macrotree = closest_macrotree
        print(f"다이아몬드 트리는 {diamond_macrotree}")
        if previous_macrotree_coords[diamond_macrotree][6] != 0 and previous_macrotree_coords[diamond_macrotree] != macrotree_coords[diamond_macrotree]:
            # 벡터 그리기
            cv2.arrowedLine(image, (previous_macrotree_coords[diamond_macrotree][6], previous_macrotree_coords[diamond_macrotree][7]), (macrotree_coords[diamond_macrotree][6], macrotree_coords[diamond_macrotree][7]), (255, 0, 0), 2)
            # 점을 그리기
            cv2.circle(image, (previous_macrotree_coords[diamond_macrotree][6], previous_macrotree_coords[diamond_macrotree][7]), 5, (0, 255, 0), -1)  # 시작점 (녹색)
            cv2.circle(image, (macrotree_coords[diamond_macrotree][6], macrotree_coords[diamond_macrotree][7]), 5, (255, 0, 0), -1)    # 끝점 (파란색)
            print(f"시작: {(previous_macrotree_coords[diamond_macrotree][6], previous_macrotree_coords[diamond_macrotree][7])} -> 끝: {(macrotree_coords[diamond_macrotree][6], macrotree_coords[diamond_macrotree][7])}")
            if movecount == 0:
                start_coords = list(previous_macrotree_coords[diamond_macrotree][6:8])  # [6], [7]을 리스트로 변환
                movecount += 1
            lastvector = True
            
        # previous_macrotree_coords에 macrotree_coords의 값 복사
        previous_macrotree_coords = macrotree_coords.copy()
        # 결과 이미지 보여주기
        print(f"movecount: {movecount}")
        # cv2.imshow('Image with Red Dots', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    # 나무가 전체적으로 위로 올라가기 때문에, 벡터에 보정치를 줌. 벡터를 제외한 나머지는 영향을 끼치지 않음
    correction_value = 0
    if diamond_macrotree == 'macrotree8':
        correction_value = 0        
    elif diamond_macrotree == 'macrotree1' or diamond_macrotree == 'macrotree7':
        correction_value = -1
    elif diamond_macrotree == 'macrotree2' or diamond_macrotree == 'macrotree6':
        correction_value = -18
    elif diamond_macrotree == 'macrotree3' or diamond_macrotree == 'macrotree5':
        correction_value = -10
    elif diamond_macrotree == 'macrotree4':
        correction_value = -10

    end_coords = macrotree_coords[diamond_macrotree][6], macrotree_coords[diamond_macrotree][7]
    end_coords = list(end_coords)

    correction_start_coords = list(start_coords)
    correction_start_coords[1] += correction_value
    # print(start_coords, end_coords)


    correction_end_coords = list(end_coords)
    if not lastvector:
        movecount -= 1

    one_picture_move = calculate_distance(start_coords, end_coords)/movecount
    if correction_start_coords[1] > end_coords[1] and one_picture_move > 2:
        one_picture_move -= 2

    if movecount == 1:
        one_picture_move *= 2
    # 거리 출력
    print(f"한 사진 당 이동한 거리: {one_picture_move}")
    # converted_macrotree_coords의 좌표를 하얀 점으로 그리기
    for key, coord in converted_macrotree_coords.items():
        x, y = coord
        cv2.circle(image, (int(x), int(y)), 5, (255, 255, 255), -1)

    if correction_start_coords[1] > end_coords[1]:
        correction_end_coords[1] += 10
        print("위로 이동함")
        



    if start_coords != (0, 0):
        # 기존 선 그리기
        cv2.arrowedLine(image, (correction_start_coords), (end_coords), (255, 255, 255), 2)
        cv2.circle(image, (start_coords), 5, (0, 255, 0), -1)  # 시작점 (녹색)
        cv2.circle(image, (end_coords), 5, (255, 0, 0), -1)    # 끝점 (파란색)
        
        # 방향 벡터 계산 (end_coords에서 start_coords로 향하는 벡터)
        direction_vector = np.array(end_coords) - np.array(correction_start_coords)
        
        # 벡터 정규화 (길이를 1로 만들기)
        unit_vector = direction_vector / np.linalg.norm(direction_vector)
        

        prolongation = 50
        if one_picture_move < 2:
            prolongation = 30
        elif one_picture_move >= 5:
            prolongation = 70
        # 원하는 길이만큼 벡터 연장 (200 픽셀)
        extended_vector = unit_vector * prolongation
        
        # print(f"{start_coords} -> {end_coords}")
        # 새로운 끝점 계산 (end_coords에서 벡터를 연장)
        new_end_coords = np.array(end_coords) + extended_vector



        new_end_coords = tuple(new_end_coords.astype(int))  # 좌표는 정수형이어야 함
                
        # 연장된 선 그리기
        # cv2.arrowedLine(image, (correction_end_coords), (new_end_coords), (255, 0, 255), 2)  # 연장된 선은 자홍색

        # 기울기 계산
        if (new_end_coords[0] - correction_end_coords[0]) != 0:  # 분모가 0이 아닌 경우에만 기울기를 계산
            slope = (new_end_coords[1] - correction_end_coords[1]) / (new_end_coords[0] - correction_end_coords[0])
        else:
            slope = np.inf  # 수직선의 경우 기울기는 무한대

        print("직선의 기울기:", slope)

        curve, curve_x, curve_y = 15, 0, 0
        if (slope < 9 and slope > 2.5) or (slope > -9 and slope < -7):
            if (correction_end_coords[0] + new_end_coords[0]) >= width:
                print("오른쪽")
                curve_x = -curve
            elif (correction_end_coords[0] + new_end_coords[0]) < width:
                print("왼쪽")
                curve_x = curve
            if (correction_end_coords[1] + new_end_coords[1]) >= height:
                print("아래")
                curve_y = -curve
            elif (correction_end_coords[1] + new_end_coords[1]) < height:
                print("위")
                curve_y = curve

        # 곡선의 제어점 (중간에 위치한 점을 조정하여 곡선 모양을 결정)
        control_point = ((correction_end_coords[0] + new_end_coords[0]) // 2 + curve_x, (correction_end_coords[1] + new_end_coords[1]) // 2 + curve_y)


    # ==============================================================꺾어지는 곡선을 연장함==============================================================

        # 방향 벡터 계산 (new_end_coords에서 control_point로 향하는 벡터)
        direction_vector2 = np.array(new_end_coords) - np.array(control_point)
        
        # 벡터 정규화 (길이를 1로 만들기)
        unit_vector2 = direction_vector2 / np.linalg.norm(direction_vector2)
        
        # 원하는 길이만큼 벡터 연장 (200 픽셀)
        extended_vector2 = unit_vector2 * 100
        
        # print(f"{start_coords} -> {end_coords}")
        # 새로운 끝점 계산 (end_coords에서 벡터를 연장)
        new_end_coords2 = np.array(new_end_coords) + extended_vector2


        new_end_coords2 = tuple(new_end_coords2.astype(int))  # 좌표는 정수형이어야 함
                
        # 곡선의 좌표들 생성 (Bézier 곡선을 사용)
        curve_points = np.array([correction_end_coords, control_point, new_end_coords, new_end_coords2])

        cv2.polylines(image, [curve_points], isClosed=False, color=(255, 0, 255), thickness=2)

        # 연장된 선 그리기
        #cv2.arrowedLine(image, (new_end_coords), (new_end_coords2), (255, 0, 255), 2)  # 연장된 선은 자홍색

        # diamond_macrotree의 좌표
        diamond_macrotree_coords = converted_macrotree_coords[diamond_macrotree]

        # 거리 계산 및 정렬
        distances = []

        for macrotree, coords in converted_macrotree_coords.items():
            if macrotree != diamond_macrotree:
                distance = calculate_distance(diamond_macrotree_coords, coords)
                distances.append((macrotree, distance))

        # 거리를 기준으로 정렬 (가까운 순)
        distances.sort(key=lambda x: x[1])

        # 1위와 2위의 macrotree 이름 가져오기
        first_place_macrotree = distances[0][0]
        second_place_macrotree = distances[1][0]
        third_place_macrotree = distances[2][0]
        fourth_place_macrotree = distances[3][0]
        fifth_place_macrotree = distances[4][0]
        sixth_place_macrotree = distances[5][0]
        seventh_place_macrotree = distances[6][0]

        if diamond_macrotree != 'macrotree4' and correction_start_coords[1] <= end_coords[1] and diamond_macrotree:
            a = 0
            if correction_start_coords[1] > end_coords[1] and diamond_macrotree != 'macrotree2' and diamond_macrotree != 'macrotree6': # 위로 올라가는 판정
                a = 1.85
            elif correction_start_coords[1] < end_coords[1]: # 아래로 내려가는 판정
                a = 3
            elif diamond_macrotree == 'macrotree2' or diamond_macrotree == 'macrotree6':
                a = 5.2
            if one_picture_move > a: # 많이 움직였을 때, 양 옆 가장 가까운 macrotree 제거
                del converted_macrotree_coords[first_place_macrotree]
                del converted_macrotree_coords[second_place_macrotree]
            elif one_picture_move < a: # 작게 움직였을 때, 양 옆을 제외하고 모두 삭제
                del converted_macrotree_coords[third_place_macrotree]
                del converted_macrotree_coords[fourth_place_macrotree]
                del converted_macrotree_coords[fifth_place_macrotree]
                del converted_macrotree_coords[sixth_place_macrotree]
                del converted_macrotree_coords[seventh_place_macrotree]

        print(f"{start_coords} -> {end_coords}")

        delpoint = 0
        if correction_start_coords[1] > end_coords[1]: # 위로 이동함
            if diamond_macrotree != 'macrotree6' and diamond_macrotree != 'macrotree2':
                delpoint = 100
            else:
                delpoint = 10
        elif correction_start_coords[1] < end_coords[1]: # 아래로 이동함
            delpoint = -10

        # 위로 올라갔을 때, 다이아몬드 매크로트리 아래를 모두 삭제. 반대의 경우, 위를 모두 삭제. 맨 위, 맨 아래의 macrotree는 없앨 필요가 없음
        if diamond_macrotree != 'macrotree4' and diamond_macrotree != 'macrotree8':
            for macrotree in list(converted_macrotree_coords.keys()):
                if correction_start_coords[1] > end_coords[1]: # 위로 이동함
                    if converted_macrotree_coords[macrotree][1] > diamond_macrotree_coords[1] + delpoint:
                        del converted_macrotree_coords[macrotree]
                        print(f"{macrotree} 삭제됨")
                elif correction_start_coords[1] < end_coords[1]: # 아래로 이동함
                    if converted_macrotree_coords[macrotree][1] < diamond_macrotree_coords[1] + delpoint:
                        del converted_macrotree_coords[macrotree]
                        print(f"{macrotree} 삭제됨")
        # 가장 위, 아래에 D.M가 있다면 기울기(slope)의 절대값이 일정량 미만일 때, 가장 위, 아래의 D.M을 삭제(Folder11)
        if diamond_macrotree == 'macrotree4' or diamond_macrotree == 'macrotree8':
            if slope != np.inf and (slope <= 8 and slope >= -8):
                print("양극단 삭제")
                del converted_macrotree_coords['macrotree4']
                del converted_macrotree_coords['macrotree8']

        # 다이아몬드 매크로트리 자기 자신을 삭제
        if diamond_macrotree in converted_macrotree_coords:
            del converted_macrotree_coords[diamond_macrotree]


        # 결과 출력
        # print("남은 macrotree:", converted_macrotree_coords)


        # 결과 출력
        print("남은 macrotree:", converted_macrotree_coords) 


        # 곡선과 각 macrotree 사이의 최소 거리 계산
        min_distance = float('inf')
        result_macrotree = None

        # macrotree 좌표와 곡선 사이의 거리 비교
        for tree_name, tree_coords in converted_macrotree_coords.items():
            distance = cv2.pointPolygonTest(curve_points, tree_coords, True)  # 거리 계산
            abs_distance = abs(distance)  # 절대값으로 변환
            print(tree_name, abs_distance)  # 거리 출력
            if abs_distance < min_distance:  # 절대값을 비교
                min_distance = abs_distance
                result_macrotree = tree_name

        print(f"결과 macrotree: {result_macrotree}")



        # 이미지 출력
        # cv2.imshow('Image with Extended Line', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if result_macrotree in macrotree_coords:
            coords = macrotree_click_coords[result_macrotree]
            pyautogui.moveTo(coords[0], coords[1])
            pyautogui.doubleClick()
            time.sleep(0.01)
            pyautogui.doubleClick()
        else:
            print("오류: 잘못된 macrotree 이름입니다.")