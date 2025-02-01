from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import math
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import random
from selenium.common.exceptions import TimeoutException

def delay(minimum, maximum): # 매크로 감지에 걸리지 않게 랜덤한 시간동안 기다리는 함수.
    delay = random.uniform(minimum, maximum)
    time.sleep(delay)


options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # WARNING 이상의 로그 메시지 만 표시

service = Service('C:/Program Files/Google/Chrome/chromedriver-win64/chromedriver.exe')  # chromedriver의 경로 설정
driver = webdriver.Chrome(service=service, options=options)
url = "https://korean.visitkorea.or.kr/main/area_list.do?type=Place&areaCode=38&sigunguCode="

tour_name = []
tour_add = []
tour_img = []

for value in range(1, 18):
    driver.get(url)
    # 버튼이 로딩될 때까지 대기
    try:
        refuse = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='locationServicePop']/div[1]/div/div[2]/a[1]"))
        )
        delay(0.8, 1.0)
        refuse.click()
        delay(0.8, 1.0)
    except Exception as e:
        print("로딩 오류: ", e)  
        driver.quit()

    num = 0
    word = ""
    if value == 1:
        word = "Seoul"
        num = 1
    elif value == 2:
        word = "Incheon"
        num = 2
    elif value == 3:
        word = "Daejeon"
        num = 3
    elif value == 4:
        word = "Daegu"
        num = 4
    elif value == 5:
        word = "Gwangju"
        num = 5
    elif value == 6:
        word = "Busan"
        num = 6
    elif value == 7:
        word = "Ulsan"
        num = 7
    elif value == 8:
        word = "Gyeonggi"
        num = 31
    elif value == 9:
        word = "Gangwon"
        num = 32
    elif value == 10:
        word = "Chungbuk"
        num = 33
    elif value == 11:
        word = "Chungnam"
        num = 34
    elif value == 12:
        word = "Gyeongbuk"
        num = 35
    elif value == 13:
        word = "Gyeongnam"
        num = 36
    elif value == 14:
        word = "Jeonbuk"
        num = 37
    elif value == 15:
        word = "Jeonnam"
        num = 38
    elif value == 16:
        word = "Jeju"
        num = 39
    elif value == 17:
        word = "Sejong"
        num = 8

    # 버튼이 로딩될 때까지 대기
    try:
        seoul = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="zone{num}"]'))
        )
        delay(0.8, 1.0)
        seoul.click()
        delay(0.8, 1.0)
    except Exception as e:
        print("로딩 오류: ", e)  
        driver.quit()

    try:
        sellect_all = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submainMapPop"]/div[1]/div/div[2]/label'))
        )
        delay(0.2, 0.4)
        sellect_all.click()
        delay(0.2, 1.4)
    except Exception as e:
        print("로딩 오류: ", e)  
        driver.quit()


    try:
        sellect = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submainMapPop"]/div[1]/div/div[3]/a'))
        )
        delay(0.8, 1.0)
        sellect.click()
        delay(0.8, 1.0)
    except Exception as e:
        print("로딩 오류: ", e)  
        driver.quit()




    i = 1
    a = 1
    while True:
        delay(1.4, 1.7)
        try:
            # 버튼 다시 찾기
            seemore_xpath = '//*[@id="contents"]/div/div[2]/div[2]/button'
            seemore = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, seemore_xpath))
            )
            
            delay(0.4, 0.7)
            # 버튼 클릭
            seemore.click()
            print(f"{word} {i}번 더보기를 눌렀습니다.")
            delay(0.4, 0.7)
            i += 1

        except Exception as e:
            print(f"{word}의 모든 여행지가 출력되었습니다.")
            print(f"총 출력된 여행지 수: {(i - 1) * 16}")
            print("오류 내용:", e)
            break

    while True:
        print(f"{word} {a}번째 여행지")
        try: 
            name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="contentList"]/li[{a}]/a'))
            )
            tour_name.append(name_element.text)

            add_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="contentList"]/li[{a}]/div/span'))
            )
            tour_add.append(add_element.text)
            try:
                img_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="contentList"]/li[{a}]/a/span/img'))
                )
                tour_img.append(img_element.get_attribute('src'))
            except TimeoutException:
                tour_img.append("사진 없음")
        except Exception as e:
            print(f"{word}의 모든 여행지가 저장되었습니다.")
            break
        a += 1


    # print("Tour Name:", tour_name)
    # print("Tour Address:", tour_add)
    # driver.quit()


print("엑셀 파일 저장중..")
data = {
    "이름": tour_name,
    "주소": tour_add,
    "이미지": tour_img
}
df = pd.DataFrame(data)
df.to_excel(f"./tourDB.xls", index=False, engine='openpyxl')
print("엑셀 파일 저장 완료")

