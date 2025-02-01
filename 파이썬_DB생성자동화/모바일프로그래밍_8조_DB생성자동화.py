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

# Haversine 공식을 사용하여 두 지점 간의 거리 계산
def haversine(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (단위: km)
    R = 6371.0
    
    # 위도와 경도를 라디안으로 변환
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # 위도와 경도의 차이 계산
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine 공식 적용
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # 거리 계산 (단위: km)
    distance = R * c
    return distance

def businesshours():
    try:
        # 링크 클릭 (//*[@id="div_detail"]/div[2]/p/a)
        link_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='div_detail']/div[2]/p/a"))
        )
        link_element.click()

        # 페이지가 로드될 때까지 기다리기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='div_detail']"))
        )

        # 첫 번째 요소에서 텍스트 추출
        detail_element_1 = driver.find_element(By.XPATH, "//*[@id='div_detail']/div[1]/ul")
        text_1 = detail_element_1.text

        # 두 번째 요소에서 텍스트 추출
        detail_element_2 = driver.find_element(By.XPATH, "//*[@id='div_detail']/div[2]")
        text_2 = detail_element_2.text

        # 두 텍스트를 결합
        combined_text = text_1 + " " + text_2

        # 불필요한 문자열 제거
        cleaned_text = combined_text.replace("영업시간", "").replace("◷ 영업 중", "").replace("접기", "").replace("맛집태그", "").replace("[오늘] ", "")
        
        # 날짜 부분을 정규 표현식으로 제거하고 요일만 남기기
        cleaned_text = re.sub(r"\d{2}\.\d{2} \((\w{1,3})\)", r"\1", cleaned_text)
        
        # 줄바꿈 문자를 제거하고 공백으로 구분
        cleaned_text = re.sub(r"\n", " ", cleaned_text).strip()

        # '월'이 시작하는 위치 찾기
        index_of_wol = cleaned_text.find('월')

        # '월' 이전의 텍스트와 이후의 텍스트 추출
        cleaned_text2 = cleaned_text[:index_of_wol].strip()  # '월' 이전 텍스트
        cleaned_text = cleaned_text[index_of_wol:].strip()  # '월' 이후 텍스트

        # cleaned_text2를 cleaned_text 뒤에 합침
        cleaned_text = cleaned_text + " " + cleaned_text2

        business_hours.append(cleaned_text)
        
    except:
            business_hours.append("월 확인필요 화 확인필요 수 확인필요 목 확인필요 금 확인필요 토  확인필요 일 확인필요")

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # WARNING 이상의 로그 메시지 만 표시

service = Service('C:/Program Files/Google/Chrome/chromedriver-win64/chromedriver.exe')  # chromedriver의 경로 설정
driver = webdriver.Chrome(service=service, options=options)

latitude_kw = 37.6194277
longitude_kw = 127.05982

url1 = "https://diningcode.com/list.dc?query=광운대학교&keyword=한식&order=r_score"
url2 = "https://diningcode.com/list.dc?query=광운대학교&keyword=중식&order=r_score"
url3 = "https://diningcode.com/list.dc?query=광운대학교&keyword=일식&order=r_score"
url4 = "https://diningcode.com/list.dc?query=광운대학교&keyword=양식&order=r_score"
url5 = "https://diningcode.com/list.dc?query=광운대학교&keyword=분식&order=r_score"
url6_1 = "https://diningcode.com/list.dc?query=광운대학교&keyword=카페&order=r_score"
url6_2 = "https://diningcode.com/list.dc?query=광운대학교&keyword=브런치&order=r_score"

xpath_name = '//*[@id="div_profile"]/div[1]/div[2]'
xpath_name2 = '//*[@id="div_profile"]/div[1]/div[1]'
xpath_starrating = '//*[@id="lbl_review_point"]'
xpath_dacorating = '//*[@id="div_profile"]/div[1]/div[4]/p[1]/strong/span/span/span[1]'
xpath_dacorating2 = '//*[@id="div_profile"]/div[1]/div[3]/p[1]/strong/span/span/span[1]'
xpath_address = '//*[@id="div_profile"]/div[2]/ul/li[1]' 
xpath_entire = "//*[@id='__nuxt']/div"
xpath_tel = '//*[@id="div_profile"]/div[2]/ul/li[2]'
xpath_src = '//*[@id="div_profile"]/div[1]/div[1]/div[1]/img'
xpath_representative_menu = '//*[@id="div_profile"]/div[1]/div[3]'
xpath_representative_menu2 = '//*[@id="div_profile"]/div[1]/div[2]'
xpath_representative_exclude_menu = '//*[@id="div_profile"]/div[1]/div[3]/a[1]'
xpath_representative_exclude_menu2 = '//*[@id="div_profile"]/div[1]/div[2]/a[1]'
xpath_search = '//*[@id="__nuxt"]/div/div[2]/div/div/input'
xpath_search2 = '//*[@id="__nuxt"]/div/div[3]/div/div/input'


element_name = []
element_starrating = []
element_dacorating = []
element_address = []
element_tel = []
element_src = []

name_text = []
starrating_text = []
dacorating_text = []
address_text = []
tel_text = []
src_text = []
src_url = []
business_hours = []
classification = []
representative_menu = []

latitude = []
longitude = []
distance = []

i = 0
value = 1
num = 0
refresh = 1

while(True):
    if refresh == 1: 
        if value == 1:
            driver.get(url1)
        elif value == 2:
            driver.get(url2)
        elif value == 3:
            driver.get(url3)
        elif value == 4:
            driver.get(url4)
        elif value == 5:
            driver.get(url5)
        elif value == 6:
            driver.get(url6_1)
        elif value == 7:
            driver.get(url6_2)
    # 페이지 로드 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[3]'))
    )
        
    # 상위 요소에서 num 번째 하이퍼링크 추출
    parent_xpath = '//*[@id="root"]/div/div[1]/div[3]'
    parent_element = driver.find_element(By.XPATH, parent_xpath)
    all_links = parent_element.find_elements(By.XPATH, './/a')
    # 두 번째 하이퍼링크의 href 속성 추출
    if len(all_links) > num:  # 두 번째 링크가 있는지 확인
        second_link = all_links[num]  # 두 번째 링크는 인덱스 1
        href = second_link.get_attribute('href')
        print(f"{num + 1} 번째")
    else:
        print(f"{num + 1} 번째 하이퍼링크를 찾을 수 없습니다.")

        total = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/h1/span[2]/span'))
        )
        # 스크롤할 특정 영역 요소 가져오기
        scrollable_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]'))
        )
        total_number = int(total.text.strip())
        print(f"총 {total_number}개")
        if total_number > num + 1:
            # 스크롤 내리기
            driver.execute_script("arguments[0].scrollBy(0, 100);", scrollable_element)
            print("스크롤을 100만큼 내렸습니다.")
            refresh = 0
            continue
        else:
            print("조건에 맞지 않아 스크롤을 내리지 않습니다.")
        num = 0
        value += 1
        if value <= 7:
            continue
        else:
            break
    
    # 해당 링크로 이동
    driver.get(href)
    # 페이지 로드 대기
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="div_profile"]/div[1]/div[2]'))
    )

    # 지정된 XPath에서 텍스트 추출
    try:
        driver.find_element(By.XPATH, xpath_src)
        element_name.append(driver.find_element(By.XPATH, xpath_name))
    except NoSuchElementException:
            element_name.append(driver.find_element(By.XPATH, xpath_name2))
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="lbl_review_point"]'))
        ) 
        element_starrating.append(driver.find_element(By.XPATH, xpath_starrating))
    except:
        element_starrating.append("별점 없음")
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath_dacorating))
        ) 
        element_dacorating.append(driver.find_element(By.XPATH, xpath_dacorating))
    except:
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, xpath_dacorating2))
            ) 
            element_dacorating.append(driver.find_element(By.XPATH, xpath_dacorating2))
        except:
            element_dacorating.append("다코점수 없음")

    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath_tel))
        ) 
        element_tel.append(driver.find_element(By.XPATH, xpath_tel))
    except:
        element_tel.append("번호 없음")

    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath_address))
        ) 
        element_address.append(driver.find_element(By.XPATH, xpath_address))
    except:
        element_address.append("주소 없음")
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath_src))
        ) 
        element_src.append(driver.find_element(By.XPATH, xpath_src))
    except:
        element_src.append("사진 없음")

    # 텍스트를 리스트에 추가
    if isinstance(element_name[i], webdriver.remote.webelement.WebElement):
        name_text.append(element_name[i].text)
    else:
        name_text.append(element_name[i])
    if isinstance(element_starrating[i], webdriver.remote.webelement.WebElement):
        starrating_text.append(element_starrating[i].text)
    else:
        starrating_text.append(element_starrating[i])
    if isinstance(element_dacorating[i], webdriver.remote.webelement.WebElement):
        dacorating_text.append(element_dacorating[i].text)
    else:
        dacorating_text.append(element_dacorating[i])
    if isinstance(element_address[i], webdriver.remote.webelement.WebElement):
        address_text.append(element_address[i].text)
    else:
        address_text.append(element_address[i])
    if isinstance(element_tel[i], webdriver.remote.webelement.WebElement):
        tel_text.append(element_tel[i].text)
    else:
        tel_text.append(element_tel[i])
    if isinstance(element_src[i], webdriver.remote.webelement.WebElement):  # WebElement인지 확인
        src_url.append(element_src[i].get_attribute('src'))  # 'src' 속성 추출
    else:
        src_url.append("사진 없음")  # WebElement가 아니면 기본값 추가


    # '지번', '지도보기', '공유' 제거
    name_text[i] = name_text[i].replace("공유", "").strip()
    address_text[i] = address_text[i].replace("지번", "").replace("지도보기", "").strip()
    if value == 1:
        classification.append("한식")
    elif value == 2:
        classification.append("중식")
    elif value == 3:
        classification.append("일식")
    elif value == 4:
        classification.append("양식")
    elif value == 5:
        classification.append("패스트푸드/분식")
    elif value == 6 or value == 7:
        classification.append("카페/디저트")

    # 텍스트 출력
    print("Name:", name_text[i])
    print("Star Rating:", starrating_text[i])
    print("Daco Rating:", dacorating_text[i])
    print("Address:", address_text[i])
    print("tel:", tel_text[i])
    print("src:", src_url[i])
    print("분류: ", classification[i])

    businesshours()
    print(business_hours[i])

    # 부모 요소 가져오기
    try:
        driver.find_element(By.XPATH, xpath_src)
        parent_element = driver.find_element(By.XPATH, xpath_representative_menu)
    except NoSuchElementException:
            parent_element = driver.find_element(By.XPATH, xpath_representative_menu2)

    try:
        driver.find_element(By.XPATH, xpath_src)
        exclude_text = driver.find_element(By.XPATH, xpath_representative_exclude_menu).text
    except NoSuchElementException:
        exclude_text = driver.find_element(By.XPATH, xpath_representative_exclude_menu2).text

    # 부모 요소에서 모든 텍스트 가져오기
    parent_text = parent_element.text

    # 제외할 텍스트 제거
    filtered_text = parent_text.replace(exclude_text, "").strip()

    representative_menu.append(filtered_text)

    print(f"대표 메뉴: {representative_menu[i]}")

    # 'findlatlng.org' 접속
    driver.get('https://www.findlatlng.org/')

    # 페이지 로드 대기
    element_entire = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div"))
    )
    # 주소 검색
    try:
        input_element = driver.find_element(By.XPATH, xpath_search)
    except:
        input_element = driver.find_element(By.XPATH, xpath_search2)
    input_element.clear()
    input_element.send_keys(address_text[i])
    input_element.send_keys(Keys.RETURN)

    time.sleep(1)  # 페이지 로딩 대기

    # 텍스트를 추출하고, 위도와 경도를 정규표현식으로 찾기
    page_text = element_entire.text
    lat_lng_pattern = r"위도\(Latitude\) : ([0-9.-]+) / 경도\(Longitude\) : ([0-9.-]+)"
    match = re.search(lat_lng_pattern, page_text)

    latitude.append(float(match.group(1)))
    longitude.append(float(match.group(2)))
    print(f"위도: {latitude[i]}")
    print(f"경도: {longitude[i]}")
    distance.append(haversine(latitude_kw, longitude_kw, latitude[i], longitude[i]))
    print(f"거리: {distance[i]} km")
    i += 1
    num += 1
    refresh = 1


# 데이터 프레임 생성
data = {
    "이름": name_text,
    "주소": address_text,
    "분류": classification,
    "별점": starrating_text,
    "다코점수": dacorating_text,
    "전화번호": tel_text,
    "이미지 url": src_url,
    "위도": latitude,
    "경도": longitude,
    "거리": distance,
    "영업시간": business_hours,
    "대표메뉴": representative_menu
}
df = pd.DataFrame(data)
# AA.xls 파일로 저장
df.to_excel("./restaurantDB.xls", index=False, engine='openpyxl')
