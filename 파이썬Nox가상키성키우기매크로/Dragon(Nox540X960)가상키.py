import pygetwindow as gw
import pyautogui
import random
import time
from PIL import ImageGrab
import keyboard
import os
import pygame
import math
import subprocess
import sys
import threading
from pynput.mouse import Listener

# sys.setrecursionlimit(1000000)
pyautogui.FAILSAFE = False # 안전장치로 인한 프로그램 종료 비활성화


# ======================================= p 버튼을 누를 시 프로그램 종료 =======================================
def stop_program():
    os._exit(0)

keyboard.add_hotkey('p', stop_program)
# ============================================================================================================

# =============================================== 변수(색) 할당 ===============================================
blue = (84, 187, 255) # 스킬 사용 가능할 때 스킬바의 색
red = (232, 77, 77) # 성채 HP의 색
cleared = (255, 79, 79) # 드래곤을 물리쳤을 때 나오는 시간초의 색
brown = (98, 87, 72) # 매크로 방지 프로그램이 나왔을 때의 배경색
A_color = (23, 179, 196) # A 등급 장비 가루의 색
S_color = (198, 11, 185) # S 등급 장비 가루의 색. 현재는 사용하지 않으나 추후에 이를 구분할 일이 생길 듯 하여 할당함.
L_color = (227, 40, 44) # L 등급 장비 가루의 색. 현재는 사용하지 않으나 추후에 이를 구분할 일이 생길 듯 하여 할당함.
mainscreenbrown = (102, 82, 54) # 메인 화면의 UI를 인식하는 색
# ============================================================================================================

# ================ 만약 게임의 외부 창을 클릭할 시 0.4초 뒤 다시 게임 창(NoxPlayer)에 포커스 옮김 =================
def on_click(x, y, button, pressed):
    if pressed:
        game_window = windows[0]
        if game_window:
            # 클릭한 좌표가 게임 창의 영역 외부라면
            if not (game_window.left <= x <= game_window.right and game_window.top <= y <= game_window.bottom):
                # 약간의 지연 후 클릭
                time.sleep(0.4)
                # 게임 창으로 포커스 옮기기
                game_window.activate()

# 마우스 모니터링 스레드 함수
def monitor_mouse_clicks():
    with Listener(on_click=on_click) as listener:
        listener.join()

# ============================================================================================================



# ======= 매크로 감지에 걸리지 않게 주어진 좌표 안에서 랜덤 클릭하는 함수. 가상키 기능을 사용하지 않을 때 사용 ======
def click(hr) : # 더블 클릭
    pyautogui.moveTo(random.uniform(hr[0], hr[2]), random.uniform(hr[1], hr[3]))
    pyautogui.doubleClick()

def generalclick(hr) : # 그냥 클릭
    pyautogui.moveTo(random.uniform(hr[0], hr[2]), random.uniform(hr[1], hr[3]))
    pyautogui.click()

# ============================================================================================================


def press(hr): # 키를 누르고 랜덤한 시간 뒤에 다시 키를 누르는 함수(키 인식이 가끔 안 먹히는 오류 때문)
    pyautogui.press(hr)
    delay(0.001, 0.002)
    pyautogui.press(hr)



def delay(minimum, maximum): # 매크로 감지에 걸리지 않게 랜덤한 시간동안 기다리는 함수.
    delay = random.uniform(minimum, maximum)
    time.sleep(delay)

def check_color_at_position(position): # 주어진 위치의 화면을 캡처하여 그 픽셀의 color를 반환하는 함수
    x, y = position
    screen = ImageGrab.grab(bbox=(x, y, x+1, y+1))  # 해당 위치에서 1x1 픽셀을 캡처
    color = screen.getpixel((0, 0))  # 그 픽셀의 색상을 가져옴
    return color

def is_similar_to(her, color, t): # 정해진 색과 비교하려는 색이 t만큼 비슷한지 비교하는 함수
    return all(abs(her[i] - color[i]) <= t for i in range(3))


def start(): # 메인 화면에서 드래곤 전투 화면으로 입장하기 위해 실행되는 함수
        pyautogui.press('v') # 메인 화면의 드래곤 석상
        delay(0.2, 0.3)
        
        pyautogui.press('v') # 레전더리 드래곤
        delay(0.05, 0.1)

        pyautogui.press('space') # BATTLE
        delay(0.15, 0.2)


def start_dragonhunt():
    start() # 메인 화면에서 드래곤 전투 화면으로 입장하기 위해 실행
    delay(0.5, 0.6) # 0.5 ~ 0.6초 랜덤 딜레이

    # ================================ 매크로 방지 프로그램이 실행되었는지 확인 ================================
    color_at_prevent_macro = check_color_at_position(prevent_macro) # prevent_macro 좌표의 색을 확인
    mecro_prevent = is_similar_to(color_at_prevent_macro, brown, 2) # 확인한 색이 brown과 2만큼 비슷한지 확인(거의 똑같아야 함)
    if mecro_prevent: # 색이 비슷하다고 확인된다면 mecro_prevent는 True의 값을 가짐. 아니면 False.
        subprocess.run(['python', 'C:/Visual_Studio_Code/GrowCastle/Prevent_macro.py']) # prevent_macro2.py(매크로 방지 프로그램 파훼) 실행
        delay(0.1, 0.2)
        color_at_prevent_macro = check_color_at_position(prevent_macro)
        mecro_prevent = is_similar_to(color_at_prevent_macro, brown, 2) 
        if mecro_prevent: # Prevent_macro.py가 실행되었음에도 여전히 True라면(매크로 방지 프로그램이 닫히지 않았다면)
            print("매크로 파훼 실패")
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load('C:/Visual_Studio_Code/GrowCastle/EnderDragonDie.mp3') # 알림이 울림
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10) # 알림이 끝날 때까지 기다림
            sys.exit(0) # 알림이 끝난 뒤에 프로그램 종료
        else: # 매크로 방지 프로그램 파훼에 성공하였다면
            monitor_heroes() # 본격적으로 드래곤과의 전투를 시작함
            delay(0.2, 0.25)
            start_dragonhunt() # 모든 단계가 끝난 뒤에 처음부터 다시 시작함
    else: # 매크로 방지 프로그램이 실행되지 않았다면
        monitor_heroes() # 본격적으로 드래곤과의 전투를 시작함
        delay(0.2, 0.25)
        start_dragonhunt() # 모든 단계가 끝난 뒤에 처음부터 다시 시작함

# =========================================================================================================

# ===================================== 드래곤과의 전투 로직 ================================================

def monitor_heroes(): # 본격적으로 드래곤과의 전투를 시작하는 함수
    global hero1skill, hero2skill, hero3skill, hero4skill, hero5skill, hero6skill, hero7skill, hero8skill, hero9skill, hero10skill, hero11skill, hero12skill, villagearcher1skill, villagearcher2skill, hpdanger, dragonhp0, mainscreen
    while True: # 다른 함수로 빠져 나가지 않는 한(승리 or 패배), 계속 반복
        color_at_hero1s = check_color_at_position(hero1s) # hero1(도로시)의 스킬바의 좌표(hero1s)의 색을 확인
        color_at_hero2s = check_color_at_position(hero2s) # hero2(앨리스)의 스킬바의 좌표(hero2s)의 색을 확인...
        color_at_hero3s = check_color_at_position(hero3s)
        color_at_hero4s = check_color_at_position(hero4s)
        color_at_hero5s = check_color_at_position(hero5s)
        color_at_hero6s = check_color_at_position(hero6s)
        color_at_hero7s = check_color_at_position(hero7s)
        color_at_hero8s = check_color_at_position(hero8s)
        color_at_hero9s = check_color_at_position(hero9s)
        color_at_hero10s = check_color_at_position(hero10s)
        color_at_hero11s = check_color_at_position(hero11s)
        color_at_hero12s = check_color_at_position(hero12s)
        color_at_villagearcher1s = check_color_at_position(villagearcher1s)
        color_at_villagearcher2s = check_color_at_position(villagearcher2s)
        color_at_hpdanger = check_color_at_position(hpdanger)  # 성채 HP의 중간 부분의 좌표(hpdanger)의 색 확인.
        color_at_dragonhp0 = check_color_at_position(dragonhp0) # 드래곤과의 전투가 끝났을 때 나오는 시간초 부분 좌표(dragonhp0)의 색을 확인
        color_at_mainscreen = check_color_at_position(mainscreen) # 메인 화면에만 나오는 UI 좌표(mainscreen)의 색을 확인

        hero1skill = is_similar_to(color_at_hero1s, blue, 20) # hero1(도로시)의 스킬바의 색이 blue와 20만큼 비슷한지(스킬 사용이 가능한지) 확인. 가능하다면 True, 불가능하다면 False.
        hero2skill = is_similar_to(color_at_hero2s, blue, 20) # hero2(앨리스)의 스킬바의 색이 blue와 20만큼 비슷한지(스킬 사용이 가능한지) 확인. 가능하다면 True, 불가능하다면 False...
        hero3skill = is_similar_to(color_at_hero3s, blue, 20)
        hero4skill = is_similar_to(color_at_hero4s, blue, 20)
        hero5skill = is_similar_to(color_at_hero5s, blue, 20)
        hero6skill = is_similar_to(color_at_hero6s, blue, 20)
        hero7skill = is_similar_to(color_at_hero7s, blue, 20)
        hero8skill = is_similar_to(color_at_hero8s, blue, 20)
        hero9skill = is_similar_to(color_at_hero9s, blue, 20)
        hero10skill = is_similar_to(color_at_hero10s, blue, 20)
        hero11skill = is_similar_to(color_at_hero11s, blue, 20)
        hero12skill = is_similar_to(color_at_hero12s, blue, 20)
        villagearcher1skill = is_similar_to(color_at_villagearcher1s, blue, 20)
        villagearcher2skill = is_similar_to(color_at_villagearcher2s, blue, 20)
        hpfull = is_similar_to(color_at_hpdanger, red, 20) # 성채 HP의 중간 부분 좌표의 색이 red와 20만큼 비슷한지(성채 HP가 절반 이상인지) 확인. 절반 이상이라면 True, 절반 이하라면 False.
        dragondie = is_similar_to(color_at_dragonhp0, cleared, 1) # 드래곤과의 전투가 끝났을 때 나오는 시간초 부분 좌표의 색이 cleared와 1만큼 비슷한지(거의 같은지) 확인. True라면 드래곤을 해치우고 보상을 기다리는 시간. False면 아직 드래곤을 해치우지 않음.
        defeat = is_similar_to(color_at_mainscreen, mainscreenbrown, 10) # 성채 HP가 0이 될 시 전투에서 패배하고 메인 화면으로 진입함. dragondie가 False임에도 defeat가 True라면(메인 화면에 진입했다면) 드래곤과의 전투에서 패배하였음을 표시. 
        if defeat: # 드래곤과의 전투에서 패배했다면
            start_dragonhunt() # 다시 드래곤 사냥 시작
        if dragondie: # 드래곤과의 전투에서 승리했다면
            receive_compensation() # 보상을 받는 함수

        # hp 적을 때 스미스 2세 스킬 1순위로 사용
        if hero10skill and not hpfull: # 스미스 2세의 스킬이 사용 가능하면서 성채 HP가 절반 이하라면
            press('z') # 스미스 2세의 스킬 사용(성채 HP 60% 회복)
            delay(0.001, 0.002)

        color_at_dragonhp0 = check_color_at_position(dragonhp0)
        dragondie = is_similar_to(color_at_dragonhp0, cleared, 1) # dragon의 생사 여부 상태 갱신

        if defeat: # 스킬 사용 사이사이에 꾸준히 패배 혹은 승리 확인.
            start_dragonhunt() # 패배했다면 다시 드래곤 사냥 시작
        if dragondie :  # 드래곤과의 전투에서 승리했다면
            receive_compensation() # 보상을 받는 함수

        # 크로노 스킬 높은 순위로 사용
        if hero6skill: # 크로노의 스킬 사용이 가능하다면
            press('q') # 크로노의 스킬 사용(게임 속도(배속) 증가)
            delay(0.002, 0.003)

        color_at_dragonhp0 = check_color_at_position(dragonhp0)
        dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)

        if defeat:
            start_dragonhunt()
        if dragondie :
            receive_compensation()


        # 3마녀 한번에 스킬 사용
        if hero1skill and hero2skill and hero3skill: # 도로시, 앨리스, 리사의 스킬 사용이 모두 가능하다면
            
            press('3') # 리사의 스킬 사용 (해골 전사 소환)
            delay(0.001, 0.002)

            color_at_dragonhp0 = check_color_at_position(dragonhp0)
            dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)

            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()

            press('2') # 앨리스의 스킬 사용 (해골 궁수 소환)
            delay(0.001, 0.002)

            color_at_dragonhp0 = check_color_at_position(dragonhp0)
            dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)

            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()


            press('1') # 도로시의 스킬 사용 (해골 마법사 소환)
            delay(0.002, 0.005)

            color_at_dragonhp0 = check_color_at_position(dragonhp0)
            dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)

            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()

        # 클레릭,  다크 네크로맨서, 다크 스켈레톤 한번에 스킬 사용
        if hero7skill and hero8skill and hero9skill: # 클레릭, 다크 네크로맨서, 다크 스켈레톤의 스킬 사용이 모두 가능할 때
            press('a') # 클레릭 스킬 사용 (아군 영웅 데미지 증가)
            delay(0.001, 0.002)

            color_at_dragonhp0 = check_color_at_position(dragonhp0)
            dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)

            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()

            press('s') # 다크 네크로맨서 스킬 사용 (적군 받는 데미지 증가)
            delay(0.001, 0.002)

            color_at_dragonhp0 = check_color_at_position(dragonhp0)
            dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)

            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()


            press('d') # 다크 스켈레톤 스킬 사용 (적군 보스에게 강한 데미지)
            delay(0.001, 0.002)

            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()

            color_at_dragonhp0 = check_color_at_position(dragonhp0)
            dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)

            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()


        # 포세이돈 스킬 사용
        if hero6skill: # 포세이돈의 스킬 사용이 가능할 때
            press('e') # 포세이돈 스킬 사용(적군 보스에게 강한 데미지. 쿨타임(스킬 재사용 대기시간)이 혼자 길어서 혼자 사용.)
            delay(0.001, 0.002)
            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()

            color_at_dragonhp0 = check_color_at_position(dragonhp0)
            dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)
            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()

        #앨리스(3마녀 대표), 닼스(닼스, 네크 , 비숍 대표), 크로노 쿨이면서, 퓨위(자신) 스킬 쓸 수 있을 때 퓨위 스킬 사용
        if not hero2skill and not hero4skill and not hero9skill and hero5skill: # 앨리스, 다크 스켈레톤, 크로노의 스킬 사용이 불가능하면서 퓨어 위자드의 스킬 사용이 가능할 때
            press('w') # 퓨어 위자드의 스킬 사용(스킬 쿨타임 중인 아군의 쿨타임 6초 감소)
            delay(0.002, 0.003)

            color_at_dragonhp0 = check_color_at_position(dragonhp0)
            dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)
            if defeat:
                start_dragonhunt()
            if dragondie :
                receive_compensation()

        # 마을아처 한번에 스킬 사용
        if villagearcher1skill and villagearcher2skill: # 마을 아처 2소대가 모두 스킬 사용 가능할 때
            press('4')
            delay(0.001, 0.002)
            press('5')
            delay(0.001, 0.002)

        color_at_dragonhp0 = check_color_at_position(dragonhp0)
        dragondie = is_similar_to(color_at_dragonhp0, cleared, 1)
        if defeat:
            start_dragonhunt()
        if dragondie :
            receive_compensation()

        delay(0.01, 0.02)  # 색상 확인 주기 (0.5초마다)

# ======================================================================================================================

def receive_compensation(): # 드래곤과의 전투 승리 시 보상을 받는 함수
    time.sleep(2.5)
    while True: # 다른 함수로 진입하지 않는 한(보상을 획득함), 계속 반복
        color_at_resultcall = check_color_at_position(resultcall)
        if is_similar_to(color_at_resultcall, brown, 1): # 드래곤을 해치우고 보상 창이 뜬다면
            delay(0.4, 0.5)
            color_at_rating = check_color_at_position(rating) # 보상의 등급 색을 확인
            if is_similar_to(color_at_rating, A_color, 20): # 보상의 등급 색이 A_color와 20만큼 비슷하다면(A등급이라면)
                pyautogui.press('n') # 보상을 가루로 분해함
                delay(0.1, 0.2)
                pyautogui.press('n') # 보상을 가루로 분해함(2차 확인)
            else : # 보상의 등급 색이 A_color와 20만큼 비슷하지 않다면(S등급이나 L등급이라면)
                pyautogui.press('m') # 보상을 인벤토리 내에 받음
            
            delay(0.2, 0.3)
            start_dragonhunt() # 모든 단계를 끝마치면 다시 드래곤 사냥 시작

# 창 크기와 위치
window = pyautogui.getActiveWindow()

window_title = 'NoxPlayer' # NoxPlayer 앱이 켜져있어야 이 창의 크기를 확인하고 변수 좌표를 할당함

# 모든 창 목록을 가져옵니다.
windows = gw.getWindowsWithTitle(window_title)

# 창이 발견되면 위치를 출력합니다.
if windows: # NoxPlayer 앱이 켜져있다면
    window = windows[0]
    # print(f'Window "{window_title}" is located at:')
    # print(f'왼쪽: {window.left}')
    # print(f'위: {window.top}')
    # print(f'오른쪽: {window.right}')
    # print(f'아래: {window.bottom}')
    # print(f'가로길이: {window.width}')
    # print(f'세로길이: {window.height}') # 디버깅용 NoxPlayer 창의 크기 확인

    hero1 = (((window.width)*0.2053)+window.left, 
             ((window.height)*0.1406)+window.top, 
             ((window.width)*0.2364)+window.left, 
             ((window.height)*0.2039)+window.top) # hero1(도로시)의 클릭 범위. (x1, y1, x2, y2)로 이루어져 있으며, 가상키가 없을 때 랜덤 클릭을 위해 사용. 이를 클릭 시 hero1의 스킬을 사용한다.
    
    hero1s = ((hero1[0]+hero1[2])/2, 
              hero1[1]-(window.height)*0.016) # hero1(도로시)의 스킬 사용 가능 여부를 판단하기 위한 좌표. 해당 좌표의 색을 판별해 hero1의 스킬 사용 가능 여부를 조사한다.
    hero1skill = True # hero1(도로시)의 스킬 사용 가능 여부. True일 시 스킬 사용 가능, False일 시 쿨타임 중이라 불가능하다는 뜻이다.

    hero2 = (((window.width)*0.2707)+window.left, 
             hero1[1], 
             ((window.width)*0.2966)+window.left, 
             hero1[3])  # hero2(앨리스)의 클릭 범위. (x1, y1, x2, y2)로 이루어져 있으며, 가상키가 없을 때 랜덤 클릭을 위해 사용. 이를 클릭 시 hero2의 스킬을 사용한다. hero1과 같은 높이에 있기에 y 좌표는 hero1의 것을 그대로 사용한다.
    
    hero2s = ((hero2[0]+hero2[2])/2, 
              hero1s[1])  # hero2(앨리스)의 스킬 사용 가능 여부를 판단하기 위한 좌표. 해당 좌표의 색을 판별해 hero2의 스킬 사용 가능 여부를 조사한다. 마찬가지로 hero1s와 같은 높이에 있기에 y 좌표는 hero1s의 것을 그대로 사용한다.
    hero2skill = True  # hero2(앨리스)의 스킬 사용 가능 여부. True일 시 스킬 사용 가능, False일 시 쿨타임 중이라 불가능하다는 뜻이다.

    hero3 = (((window.width)*0.3289)+window.left, 
             hero1[1], 
             ((window.width)*0.3583)+window.left, 
             hero1[3])
    
    hero3s = ((hero3[0]+hero3[2])/2, 
              hero1s[1])
    hero3skill = True


    hero4 = (hero1[0], 
            ((window.height)*0.2636)+window.top, 
             hero1[2], 
            ((window.height)*0.3374)+window.top)

    hero4s = ((hero4[0]+hero4[2])/2, 
              hero4[1]-(window.height)*0.017)
    hero4skill = True


    hero5 = (hero2[0], 
             hero4[1], 
             hero2[2], 
             hero4[3])
    
    hero5s = ((hero5[0]+hero5[2])/2, 
              hero4s[1])
    hero5skill = True

    hero6 = (hero3[0], 
             hero4[1], 
             hero3[2], 
             hero4[3])

    hero6s = ((hero6[0]+hero6[2])/2, 
              hero4s[1])
    hero6skill = True

    hero7 = (hero1[0], 
            ((window.height)*0.3869)+window.top, 
             hero1[2], 
            ((window.height)*0.4569)+window.top)
    
    hero7s = ((hero7[0]+hero7[2])/2, 
              hero7[1]-(window.height)*0.016)
    hero7skill = True

    hero8 = (hero2[0], 
             hero7[1], 
             hero2[2], 
             hero7[3])
    
    hero8s = ((hero8[0]+hero8[2])/2, 
              hero7s[1])
    hero8skill = True

    hero9 = (hero3[0], 
             hero7[1], 
             hero3[2], 
             hero7[3])
    
    hero9s = ((hero9[0]+hero9[2])/2, 
              hero7s[1])
    hero9skill = True


    hero10 = (hero1[0], 
            ((window.height)*0.5088)+window.top, 
             hero1[2], 
            ((window.height)*0.5676)+window.top)
    
    hero10s = ((hero10[0]+hero10[2])/2, 
              hero10[1]-(window.height)*0.016)
    hero10skill = True

    hero11 = (hero2[0], 
             hero10[1], 
             hero2[2], 
             hero10[3])
    
    hero11s = ((hero11[0]+hero11[2])/2, 
              hero10s[1])
    hero11skill = True

    hero12 = (hero3[0], 
             hero10[1], 
             hero3[2], 
             hero10[3])
    
    hero12s = ((hero12[0]+hero12[2])/2, 
              hero10s[1])
    hero12skill = True

    villagearcher1 = (((window.width)*0.0846)+window.left, 
                     ((window.height)*0.5472)+window.top, 
                     ((window.width)*0.1206)+window.left, 
                     ((window.height)*0.6132)+window.top)
    
    villagearcher1s = ((villagearcher1[0]+villagearcher1[2])/2, 
                        villagearcher1[1]-(window.height)*0.016)
    villagearcher1skill = True

    villagearcher2 = (villagearcher1[0], 
                     ((window.height)*0.7012)+window.top, 
                     villagearcher1[2], 
                     ((window.height)*0.7635)+window.top)

    villagearcher2s = ((villagearcher2[0]+villagearcher2[2])/2, 
                        villagearcher2[1]-(window.height)*0.016)
    villagearcher2skill = True

    ent = (((window.width)*0.4482)+window.left, 
             ((window.height)*0.3342)+window.top, 
             ((window.width)*0.4825)+window.left, 
             ((window.height)*0.3343)+window.top) # 메인 화면에서 드래곤 석상의 좌표 범위이다. 가상키 사용이 불가능할 때 해당 범위를 랜덤 클릭하여 화면을 이동한다.

    ent5 = (((window.width)*0.44)+window.left, 
             ((window.height)*0.37)+window.top, 
             ((window.width)*0.48)+window.left, 
             ((window.height)*0.45)+window.top) # 메인 화면에서 ent를 눌러 2번째 화면으로 들어갔을 때 레전더리 드래곤 버튼의 좌표이다. 가상키 사용이 불가능할 때 해당 범위를 랜덤 클릭하여 화면을 이동한다.

    battle = (((window.width)*0.65)+window.left, 
             ((window.height)*0.82)+window.top, 
             ((window.width)*0.72)+window.left, 
             ((window.height)*0.90)+window.top) # 2번째 화면에서 레전더리 드래곤 버튼을 눌렀을 때 battle 버튼의 좌표이다. 가상키 사용이 불가능할 때 해당 범위를 랜덤 클릭하여 화면을 이동한다.

    hpdanger = (((window.width)*0.5787)+window.left, 
            ((window.height)*0.08)+window.top) # 성채 HP의 중간 어느 부분의 좌표이다. 해당 좌표의 색을 판별해 스미스 2세의 스킬 사용 여부를 결정한다.

    resultcall = (((window.width)*0.515)+window.left, 
            ((window.height)*0.655)+window.top) # 드래곤을 해치우고 보상 창이 뜨는 것을 인식하는 좌표. 해당 좌표의 색을 판별해 이를 조사한다.

    receive = (((window.width)*0.583)+window.left, 
            ((window.height)*0.661)+window.top, 
            ((window.width)*0.584)+window.left, 
            ((window.height)*0.662)+window.top) # 보상 장비를 받는 버튼 좌표 범위이다. 가상키 사용이 불가능할 때 사용한다.

    dragonhp0 = (((window.width)*0.4761)+window.left, 
            ((window.height)*0.2107)+window.top) # 드래곤을 해치웠는지 여부를 인식하는 좌표. 해당 좌표의 색을 판별해 이를 조사한다.
    
    prevent_macro = (((window.width)*0.3761)+window.left, 
            ((window.height)*0.7507)+window.top) # 매크로 방지 프로그램이 실행되었는지 여부를 인식하는 좌표. 해당 좌표의 색을 판별해 이를 조사한다.
    
    rating = (((window.width)*0.4296)+window.left, 
            ((window.height)*0.6532)+window.top) # 보상의 등급을 인식하는 좌표. 해당 좌표의 색을 판별해 이를 조사한다.

    ingredient = (((window.width)*0.4036)+window.left, 
            ((window.height)*0.6415)+window.top, 
            ((window.width)*0.4513)+window.left, 
            ((window.height)*0.7012)+window.top) # 보상 장비를 분해하는 좌표 범위이다. 가상키 사용이 불가능할 때 사용한다.

    mainscreen = (((window.width)*0.6081)+window.left, 
            ((window.height)*0.4727)+window.top) # 메인 화면의 UI를 인식하는 좌표. 해당 좌표의 색을 판별해 이를 조사한다.

    # 마우스 모니터링 스레드 시작
    mouse_thread = threading.Thread(target=monitor_mouse_clicks)
    mouse_thread.daemon = True  # 메인 프로그램이 끝나면 이 스레드도 종료
    mouse_thread.start() # 게임 창(NoxPlayer) 바깥의 창을 눌러 게임 창이 포커스에서 벗어나면, 0.4초 뒤 다시 게임 창을 포커스하는 함수를 다른 스레드에서 계속 실행시킨다.

    window.activate() # 게임 창(NoxPlayer) 에 포커스를 맞춤
    start_dragonhunt() # 드래곤 사냥을 시작함.
else:
    print(f"{window_title} 창을 키고 해당 프로그램을 실행해주세요.") # 게임 창(NoxPlayer)을 키지 않았음을 알리고 프로그램 종료.