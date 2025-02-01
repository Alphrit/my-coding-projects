import sys
import pyautogui
import time
import keyboard
from datetime import datetime
import os
from PIL import Image
import tkinter as tk
from tkinter import messagebox
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import threading

level = 1
value = "레이저 소총"

def rgbcomp(image, unique):
    rgb_values = []
    for coord in unique:
        x, y = coord
        rgb_value = image[y, x]
        rgb_values.append(tuple(rgb_value))

    all_same = all(value == rgb_values[0] for value in rgb_values)


    if all_same:
        return True
    else:
        return False

Display = 0

def submit():
        global A, B, C, D, E, F, LeastLevel, Display, Thundercloud, Starttime
        if not (var_A.get() or var_B.get() or var_C.get() or var_D.get() or var_E.get() or var_F.get()):
            A = B = C = D = E = F = 1
        else:
            A = 1 if var_A.get() else 0
            B = 1 if var_B.get() else 0
            C = 1 if var_C.get() else 0
            D = 1 if var_D.get() else 0
            E = 1 if var_E.get() else 0
            F = 1 if var_F.get() else 0

        LeastLevel = level_var.get()
        Display = display_var.get()
        Thundercloud = 1 if var_T.get() else 0
        Starttime = 5 if var_S.get() else 2.5

        if display_var.get() == 0:
            messagebox.showwarning("경고", "해상도를 선택해주세요.")
            return 

        # 창 닫기
        root.destroy()

def stop_program():
    global running
    global app
    running = False
    
    root = tk.Tk()
    root.withdraw()
    
    if app is not None:
        app.quit()
    sys.exit()

keyboard.add_hotkey('p', stop_program)


def find_image(image, i, conf, type):
    while running:
        try:
            if isinstance(image, tuple):  # image 변수가 튜플(좌표값)인지 확인
                x, y = image  # 좌표값을 x, y로 분리
                if type == 1:
                    pyautogui.click(x, y)
                    break
                elif type == 2:
                    pyautogui.doubleClick(x, y)
                    break
                elif type == 3:
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    break
                elif type == 4:
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseDown(button='right')
                    pyautogui.mouseUp(button='right')
                    break
            else:
                image_location = pyautogui.locateOnScreen(image, confidence=conf)
                if image_location:
                    image_center = pyautogui.center(image_location)
                    if type == 1:
                        pyautogui.click(image_center)
                        break
                    elif type == 2:
                        pyautogui.doubleClick(image_center)
                        break
                    elif type == 3:
                        pyautogui.moveTo(image_center)
                        pyautogui.mouseDown()
                        pyautogui.mouseUp()
                        break
                    elif type == 4:
                        pyautogui.moveTo(image_center)
                        pyautogui.mouseDown(button='right')
                        pyautogui.mouseUp(button='right')
                        break
                else:
                    time.sleep(i)
        
        except Exception as e:
            time.sleep(i)

        if not running:
            break


def loading(i):

    global running
    running = True
    x, y = 500, 900

    while running:

        try:
            screenshot = pyautogui.screenshot()
            image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
            
            rgb_value = image.getpixel((x, y))
            if rgb_value == (0, 0, 0):
                pyautogui.sleep(i)
            else:
                break
        except Exception as e:
            running = False
        if not running:
            break

def congratulation(level, value):
    if Thundercloud == 1:
        time.sleep(1.0)
        pyautogui.press('tab')
        find_image(image_path5, 0.1, 0.95, 4)

        time.sleep(0.5)

        find_image(image_path6, 0.1, 0.95, 1)

        time.sleep(10)
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Congratulation!", f"{level}레벨 {value} 획득을 축하드립니다!")
    
    stop_program()

running = True
app = None



root = tk.Tk()
root.title("Palcro")
icon_path = './image/Image_99.ico'
root.iconbitmap(icon_path)

# 체크박스 변수 생성
var_A = tk.IntVar()
var_B = tk.IntVar()
var_C = tk.IntVar()
var_D = tk.IntVar()
var_E = tk.IntVar()
var_F = tk.IntVar()


level_var = tk.IntVar(value=0)
display_var = tk.IntVar(value=0)
var_T = tk.IntVar()
var_S = tk.IntVar()

# 전역으로 이미지 변수 생성
image_mult = tk.PhotoImage(file="./image/Image_mult.png")
image_misa = tk.PhotoImage(file="./image/Image_misa.png")
image_flame = tk.PhotoImage(file="./image/Image_flame.png")
image_gren = tk.PhotoImage(file="./image/Image_gren.png")
image_lesa = tk.PhotoImage(file="./image/Image_lesa.png")
image_gatl = tk.PhotoImage(file="./image/Image_gatl.png")
image_hero = tk.PhotoImage(file="./image/Image_hero.png")
image_lege = tk.PhotoImage(file="./image/Image_lege.png")
image_1920X1080 = tk.PhotoImage(file="./image/Image_1920X1080.png")
image_2560X1440 = tk.PhotoImage(file="./image/Image_2560X1440.png")
image_1920X1080mini = tk.PhotoImage(file="./image/Image_1920X1080mini.png")
image_thundercloud = tk.PhotoImage(file="./image/Image_thundercloud.png")

tk.Label(root, text="무기 종류:").grid(row=0, column=0, sticky='w')

checkbutton1 = tk.Checkbutton(root, text="다연장 미사일 발사기", variable=var_A)
checkbutton1.grid(row=1, column=0, sticky='w')
image_label1 = tk.Label(root, image=image_mult)
image_label1.grid(row=1, column=1, sticky='e')

checkbutton2 = tk.Checkbutton(root, text="미사일 발사기", variable=var_B)
checkbutton2.grid(row=2, column=0, sticky='w')
image_label2 = tk.Label(root, image=image_misa)
image_label2.grid(row=2, column=1, sticky='e')

checkbutton3 = tk.Checkbutton(root, text="화염 방사기", variable=var_C)
checkbutton3.grid(row=3, column=0, sticky='w')
image_label3 = tk.Label(root, image=image_flame)
image_label3.grid(row=3, column=1, sticky='e')

checkbutton4 = tk.Checkbutton(root, text="유탄 발사기", variable=var_D)
checkbutton4.grid(row=4, column=0, sticky='w')
image_label4 = tk.Label(root, image=image_gren)
image_label4.grid(row=4, column=1, sticky='e')

checkbutton5 = tk.Checkbutton(root, text="레이저 소총", variable=var_E)
checkbutton5.grid(row=5, column=0, sticky='w')
image_label5 = tk.Label(root, image=image_lesa)
image_label5.grid(row=5, column=1, sticky='e')

checkbutton6 = tk.Checkbutton(root, text="개틀링 건", variable=var_F)
checkbutton6.grid(row=6, column=0, sticky='w')
image_label6 = tk.Label(root, image=image_gatl)
image_label6.grid(row=6, column=1, sticky='e')

tk.Label(root, text="최소 레벨:").grid(row=7, column=0, sticky='w')

checkbutton7 = tk.Radiobutton(root, text="영웅", variable=level_var, value=3)
checkbutton7.grid(row=8, column=0, sticky='w')
image_label7 = tk.Label(root, image=image_hero)
image_label7.grid(row=8, column=1, sticky='e')

checkbutton8 = tk.Radiobutton(root, text="전설", variable=level_var, value=4)
checkbutton8.grid(row=9, column=0, sticky='w')
image_label8 = tk.Label(root, image=image_lege)
image_label8.grid(row=9, column=1, sticky='e')

tk.Label(root, text="해상도:").grid(row=10, column=0, sticky='w')

checkbutton9 = tk.Radiobutton(root, text="FHD(1920X1080) 전체화면", variable=display_var, value=1)
checkbutton9.grid(row=11, column=0, sticky='w')
image_label9 = tk.Label(root, image=image_1920X1080)
image_label9.grid(row=11, column=1, sticky='e')

checkbutton10 = tk.Radiobutton(root, text="QHD(2560X1440) 전체화면", variable=display_var, value=2)
checkbutton10.grid(row=12, column=0, sticky='w')
image_label10 = tk.Label(root, image=image_2560X1440)
image_label10.grid(row=12, column=1, sticky='e')

checkbutton11 = tk.Radiobutton(root, text="QHD(2560X1440) 환경에서 FHD(1920X1080) 창모드", variable=display_var, value=3)
checkbutton11.grid(row=13, column=0, sticky='w')
image_label11 = tk.Label(root, image=image_1920X1080mini)
image_label11.grid(row=13, column=1, sticky='e')

tk.Label(root, text="").grid(row=14, column=0, sticky='w')

checkbutton12 = tk.Checkbutton(root, text="목표 달성 시 귀환의 뇌운 사용 \n(⚠️ 인벤토리에 귀환의 뇌운을 소지중이어야 함)", variable=var_T,  justify=tk.LEFT)
checkbutton12.grid(row=15, column=0, sticky='w')
image_label12 = tk.Label(root, image=image_thundercloud)
image_label12.grid(row=15, column=1, sticky='e')

checkbutton13 = tk.Checkbutton(root, text="느린 재시작\n(기존 설정으로 실행 시 빠른 재시작으로 문제 발생하면 체크)", variable=var_S,  justify=tk.LEFT)
checkbutton13.grid(row=16, column=0, sticky='w')

tk.Label(root, text="⚠️1: P 버튼을 누르면 프로그램이 종료됩니다.").grid(row=17, column=0, sticky='w')
tk.Label(root, text="⚠️2: 팰월드의 아이콘이 깔끔하게 보이는 곳에서 프로그램을 실행해주세요.").grid(row=18, column=0, sticky='w')
tk.Label(root, text="⚠️3: 팰월드 옵션에서 해상도를 맞춰주세요. 전체화면&창모드도 확인해주세요.").grid(row=19, column=0, sticky='w')
tk.Label(root, text="⚠️4: 해당 설정을 끝내고 나올 하늘색 박스에 설계도가 들어가는지 확인해주세요.").grid(row=20, column=0, sticky='w')
tk.Label(root, text="⚠️5: 설정에서 '상호작용 4'를 on 시켜주세요.").grid(row=21, column=0, sticky='w')
tk.Label(root, text="⚠️6: 본 프로그램은 유기될 수 있습니다.").grid(row=22, column=0, columnspan=2, sticky='w')
tk.Label(root, text="Made by 알프리트").grid(row=23, column=0, sticky='w', padx=(10, 0))
tk.Label(root, text="Version 0.1.0").grid(row=23, column=1, sticky='e', padx=(0, 10))

tk.Button(root, text="시작", command=submit).grid(row=24, column=0, columnspan=2, sticky='nsew')



# 창 실행
root.mainloop()
        
# 이미지 파일의 경로
if (Display == 1 or Display == 3):
    image_path1 = "./image/Image_1.png"
    image_path2 = "./image/Image_2.png"
    image_path3 = "./image/Image_3.png"
    image_path4 = "./image/Image_4.png"
    image_path5 = "./image/Image_5.png"
    image_path6 = "./image/Image_6.png"
elif (Display == 2):
    image_path1 = "./image/Image_1.png"
    image_path2 = "./image/Image_2 (1).png"
    image_path3 = "./image/Image_3 (1).png"
    image_path4 = "./image/Image_4 (1).png"
    image_path5 = "./image/Image_5 (1).png"
    image_path6 = "./image/Image_6 (1).png"
elif (Display == 0):
    sys.exit()


if (Display == 1 or Display == 3):
    flame_unique = [(9, 10), (12, 17), (7, 17), (9, 13), (13, 17), (8, 17), (14, 17), (10, 17), (11, 9), (21, 12), (13, 9), (9, 17), (15, 12)]

    mult_unique = [(21, 11), (22, 11)]

    gatl_unique = [
        (16, 7), (13, 8), (16, 16), (16, 13), (16, 19), (9, 7), (13, 7), (11, 13), (16, 9), (16, 6), (16, 12), 
        (16, 15), (16, 18), (10, 7), (9, 15), (16, 5), (16, 8), (18, 11), (16, 17)
    ]

    gren_unique = [
        (9, 8), (9, 14), (13, 5), (13, 11), (18, 14), (15, 5), (11, 20), (15, 14),
        (17, 20), (11, 19), (18, 6), (18, 15), (21, 14), (14, 5), (9, 9), (10, 10), (11, 15), (11, 18), (7, 14)
    ]

    miss_unique = [(14, 8), (14, 7), (14, 10), (14, 9), (14, 12), (14, 15)]

    lesa_unique = [(10, 11), (17, 7), (17, 10), (17, 13), (17, 9), (17, 6), (17, 5), (9, 11), (17, 8), (12, 8), (11, 11)]

    gatl_one_unique = [(142, 10), (142, 17), (142, 15), (142, 12), (142, 18), (142, 11), (142, 14)]
    flame_one_unique = [(x + 13, y) for x, y in gatl_one_unique]
    gren_one_unique = [(x + 17, y) for x, y in gatl_one_unique]
    miss_one_unique = [(x + 34, y) for x, y in gatl_one_unique]
    mult_one_unique = [(x + 89, y) for x, y in gatl_one_unique]


    gatl_two_unique = [(139, 17), (139, 18), (139, 14)]
    flame_two_unique = [(x + 13, y) for x, y in gatl_two_unique]
    gren_two_unique = [(x + 17, y) for x, y in gatl_two_unique]
    miss_two_unique = [(x + 34, y) for x, y in gatl_two_unique]
    mult_two_unique = [(x + 89, y) for x, y in gatl_two_unique]

    gatl_three_unique = [
        (140, 7), (141, 7), (142, 7), (143, 7),
        (145, 8), (145, 9), (145, 10), (145, 11),
        (140, 13), (141, 13), (142, 13), (143, 13),
        (144, 13), (145, 14), (145, 15), (145, 16),
        (145, 17), (145, 18), (140, 19), (141, 19),
        (142, 19), (143, 19)
    ]
    flame_three_unique = [(x + 13, y) for x, y in gatl_three_unique]
    gren_three_unique = [(x + 17, y) for x, y in gatl_three_unique]
    miss_three_unique = [(x + 34, y) for x, y in gatl_three_unique]
    mult_three_unique = [(x + 89, y) for x, y in gatl_three_unique]

    gatl_four_unique = [(141, 11), (141, 10), (144, 16), (145, 13), (140, 16), (141, 16), (143, 16)]
    flame_four_unique = [(x + 13, y) for x, y in gatl_four_unique]
    gren_four_unique = [(x + 17, y) for x, y in gatl_four_unique]
    miss_four_unique = [(x + 34, y) for x, y in gatl_four_unique]
    mult_four_unique = [(x + 89, y) for x, y in gatl_four_unique]

elif (Display == 2):
    flame_unique = [
        (16, 20), (18, 20), (12, 13), (20, 20), (14, 10), (16, 4), (11, 20), (16, 16), (18, 10), (18, 16), 
        (13, 20), (21, 6), (12, 15), (17, 20), (15, 4), (19, 20), (13, 16), (10, 20), (15, 10), (15, 16), 
        (12, 11), (12, 14), (21, 20), (12, 20), (17, 16), (14, 20), (13, 15)
    ]
    mult_unique = [
        (28, 12), (21, 18)
    ]
    gatl_unique = [(15, 14), (16, 13), (22, 24), (23, 13), (17, 9), (14, 15), (24, 13), (17, 11), (17, 8), (15, 15)
    ]

    gren_unique = [(15, 21), (20, 5), (18, 17), (15, 24), (12, 10), (23, 19), (23, 22), (17, 12), (23, 25), (13, 11), 
                (24, 11), (13, 8), (24, 17), (15, 23), (18, 13), (12, 9), (23, 18), (17, 5), (23, 21), (14, 18)
    ]
    miss_unique = [
                (19, 8), (20, 11), (20, 8), (19, 7), (20, 7), (19, 10), (19, 16), (20, 10), (20, 16), (19, 9), 
                (20, 19), (20, 9), (20, 15)
    ]

    lesa_unique = [
        (10, 15), (10, 14), (16, 9), (27, 23), (10, 13), (10, 16), (10, 12), (13, 12), (16, 8), (21, 11)
    ]

    gatl_one_unique =  [(194, 11), (194, 17), (194, 13), (194, 16), (194, 12), (194, 18), (194, 21)]

    flame_one_unique = [(x + 17, y) for x, y in gatl_one_unique]
    gren_one_unique = [(x + 23, y) for x, y in gatl_one_unique]
    miss_one_unique = [(x + 46, y) for x, y in gatl_one_unique]
    mult_one_unique = [(x + 121, y) for x, y in gatl_one_unique]



    gatl_two_unique = [(189, 21), (189, 17), (192, 16), (189, 23), (190, 21)]

    flame_two_unique = [(x + 17, y) for x, y in gatl_two_unique]
    gren_two_unique = [(x + 23, y) for x, y in gatl_two_unique]
    miss_two_unique = [(x + 46, y) for x, y in gatl_two_unique]
    mult_two_unique = [(x + 121, y) for x, y in gatl_two_unique]



    gatl_three_unique = [(195, 14), (193, 14), (196, 14), (197, 15)]

    flame_three_unique = [(x + 17, y) for x, y in gatl_three_unique]
    gren_three_unique = [(x + 23, y) for x, y in gatl_three_unique]
    miss_three_unique = [(x + 46, y) for x, y in gatl_three_unique]
    mult_three_unique = [(x + 121, y) for x, y in gatl_three_unique]



    gatl_four_unique = [(192, 20), (192, 13), (192, 19), (195, 20), (196, 19), (191, 19), (193, 11), (192, 12), (197, 20), (195, 19), 
                        (193, 20), (198, 15), (193, 10), (197, 19), (193, 19), (196, 20), (191, 20), (193, 12)]

    flame_four_unique = [(x + 17, y) for x, y in gatl_four_unique]
    gren_four_unique = [(x + 23, y) for x, y in gatl_four_unique]
    miss_four_unique = [(x + 46, y) for x, y in gatl_four_unique]
    mult_four_unique = [(x + 121, y) for x, y in gatl_four_unique]


if (Display == 1):
    left, top, right, bottom, worldx, worldy = 109, 794, 400, 819, 950, 260
elif (Display == 2):
    left, top, right, bottom, worldx, worldy = 145, 1060, 505, 1090, 1270, 340
elif (Display == 3):
    left, top, right, bottom, worldx, worldy = 429, 950, 720, 975, 1270, 410

class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transparent Window")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

        # 화면 해상도 가져오기
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))

        width = right - left
        height = bottom - top

        pen = QPen(QColor('skyblue'), 4)
        painter.setPen(pen)

        # 직사각형 그리기
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawRect(left, top, width, height)

#------------------------------------------------------------------

def maincode():
    global running
    while running:
        time.sleep(0.5)

        find_image(image_path1, 1.0, 0.95, 2)
        if not running:
            break
        time.sleep(1.0)
        pyautogui.moveTo(100, 100)
        time.sleep(4.0)

        find_image(image_path2, 0.1, 0.95, 1)
        if not running:
            break

        find_image(image_path3, 0.1, 0.95, 3)
        if not running:
            break

        find_image((worldx, worldy), 0.1, 0.95, 3)
        if not running:
            break


        find_image(image_path4, 0.1, 0.95, 3)
        if not running:
            break

        time.sleep(5.0)

        loading(1)
        if not running:
            break

        time.sleep(2)

        pyautogui.keyDown('F') 
        time.sleep(0.1)
        pyautogui.keyUp('F')
        if not running:
            break

        time.sleep(11.0)
        if not running:
            break


        screenshot = pyautogui.screenshot()
        processed_img = screenshot.crop((left, top, right, bottom))
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'screenshot_{current_time}.png'
        folder_path = './history'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name)
        processed_img.save(file_path)
        processed_img = np.array(processed_img)

        value = '다연장 미사일 발사기'
        if not rgbcomp(processed_img, mult_unique):
            value = '미사일 발사기'
            if not rgbcomp(processed_img, miss_unique):
                value = '화염 방사기'
                if not rgbcomp(processed_img, flame_unique):
                    value = '유탄 발사기'
                    if not rgbcomp(processed_img, gren_unique):
                        value = '레이저 소총'
                        if not rgbcomp(processed_img, lesa_unique):
                            value = '개틀링 건'
        level = 1
        if (value == '개틀링 건'):
            if not rgbcomp(processed_img, gatl_one_unique):
                level = 2
                if not rgbcomp(processed_img, gatl_two_unique):
                    level = 3
                    if not rgbcomp(processed_img, gatl_three_unique):
                        level = 4
                        if not rgbcomp(processed_img, gatl_four_unique):
                            level = 0

        elif (value == '유탄 발사기' or value == '레이저 소총' ):
            if not rgbcomp(processed_img, gren_one_unique):
                level = 2
                if not rgbcomp(processed_img, gren_two_unique):
                    level = 3
                    if not rgbcomp(processed_img, gren_three_unique):
                        level = 4
                        if not rgbcomp(processed_img, gren_four_unique):
                            level = 0

        elif (value == '화염 방사기'):
            if not rgbcomp(processed_img, flame_one_unique):
                level = 2
                if not rgbcomp(processed_img, flame_two_unique):
                    level = 3
                    if not rgbcomp(processed_img, flame_three_unique):
                        level = 4
                        if not rgbcomp(processed_img, flame_four_unique):
                            level = 0

        elif (value == '미사일 발사기'):
            if not rgbcomp(processed_img, miss_one_unique):
                level = 2
                if not rgbcomp(processed_img, miss_two_unique):
                    level = 3
                    if not rgbcomp(processed_img, miss_three_unique):
                        level = 4
                        if not rgbcomp(processed_img, miss_four_unique):
                            level = 0

        elif (value == '다연장 미사일 발사기'):
            if not rgbcomp(processed_img, mult_one_unique):
                level = 2
                if not rgbcomp(processed_img, mult_two_unique):
                    level = 3
                    if not rgbcomp(processed_img, mult_three_unique):
                        level = 4
                        if not rgbcomp(processed_img, mult_four_unique):
                            level = 0


        if (level >= LeastLevel and value == '다연장 미사일 발사기' and A == 1) :
            congratulation(level, value)
            break
        elif (level >= LeastLevel and value == '미사일 발사기' and B == 1) :
            congratulation(level, value)
            break
        elif (level >= LeastLevel and value == '화염 방사기' and C == 1) :
            congratulation(level, value)
            break
        elif (level >= LeastLevel and value == '유탄 발사기' and D == 1) :
            congratulation(level, value)
            break
        elif (level >= LeastLevel and value == '레이저 소총' and E == 1) :
            congratulation(level, value)
            break
        elif (level >= LeastLevel and value == '개틀링 건' and F == 1) :
            congratulation(level, value)
            break
        else:
            pyautogui.hotkey('alt', 'f4')

        time.sleep(Starttime)
        if not running:
            break

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TransparentWindow()
    window.show()

    thread = threading.Thread(target=maincode)
    thread.daemon = True
    thread.start()

    sys.exit(app.exec_())

