from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import pandas as pd
from selenium.common.exceptions import TimeoutException
import sys

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False # plt 한글 글꼴

def get_driver(url, books, authors):
    driver.get(url) # 해당 url에 접속
    try:
        if url == url_aladin:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Myform"]/div[3]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[2]/a[1]'))
            )
        elif url == url_ypbooks:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[2]/section/div/ul/li[1]/div/div[1]/div/div[2]/a'))
            )
        elif url == url_kyobobooks:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/section/div/div/section/ol[1]/li[1]/div/div[2]/div[2]/a'))
            )
        elif url == url_yes24:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="yesBestList"]/li[1]/div/div[2]/div[2]/a[1]'))  # 각 1위 베스트셀러가 로딩될 때까지 대기
            )
    except TimeoutException:
        print("오류: 지정된 XPath의 요소가 제한된 시간 안에 로딩되지 않았습니다.")
        sys.exit() # 20초 안에 로딩이 안되면 오류와 함께 프로그램 종료...

    try:
        if url == url_aladin:
            a = 3
        else:
            a = 1     # 알라딘만 1위가 Xpath 기준 3부터 시작하고, 나머지는 1부터 시작
        
        for i in range(a, a + num):
            if url == url_aladin:
                book_name = driver.find_element(By.XPATH, f'//*[@id="Myform"]/div[{i}]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[2]/a[1]').text
            elif url == url_ypbooks:
                book_name = driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[2]/section/div/ul/li[{i}]/div/div[1]/div/div[2]/a').text
            elif url == url_kyobobooks:
                book_name = driver.find_element(By.XPATH, f'/html/body/div[1]/main/section/div/div/section/ol[1]/li[{i}]/div/div[2]/div[2]/a').text
            elif url == url_yes24:
                book_name = driver.find_element(By.XPATH, f'//*[@id="yesBestList"]/li[{i}]/div/div[2]/div[2]/a[1]').text
            books.append(book_name)   # 각 베스트셀러의 책 제목란의 Xpath를 인식해 books에 순위 순서대로 추가

        for i in range(a, a + num):
            if url == url_aladin:
                author_name = driver.find_element(By.XPATH, f'//*[@id="Myform"]/div[{i}]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[3]/a[1]').text
            elif url == url_ypbooks:
                author_name = driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[2]/section/div/ul/li[{i}]/div/div[1]/div/div[2]/ul[3]/li[1]/span').text
            elif url == url_kyobobooks:
                author_info = driver.find_element(By.XPATH, f'/html/body/div[1]/main/section/div/div/section/ol[1]/li[{i}]/div/div[2]/div[2]/div[2]').text
                author_name = author_info.split('·')[0].strip()  # 저자 이름만 추출.
            elif url == url_yes24:
                author_name = driver.find_element(By.XPATH, f'//*[@id="yesBestList"]/li[{i}]/div/div[2]/div[3]/span[1]/a').text
            authors.append(author_name)    # 각 베스트셀러의 책 작가란의 Xpath를 인식해 books에 순위 순서대로 추가

        if url == url_aladin:
                    print("\n====================================== 알라딘 =====================================")
        elif url == url_ypbooks:
                    print("\n===================================== 영풍문고 =====================================")
        elif url == url_kyobobooks:
                    print("\n===================================== 교보문고 =====================================")
        elif url == url_yes24:
                    print("\n====================================== yes24 ======================================")

        for i in range(0, len(books)):
            print(f"{i+1}위: {books[i]} - {authors[i]}")

    except Exception as e:
        print("오류 발생:", e)

# 책 제목 정규화 함수
def normalize_title(title):
    # 불필요한 부분 제거: [], (), 특정 단어 등
    title = re.sub(r"\[.*?\]|\(.*?\)", "", title)  # 대괄호와 소괄호 내용을 제거
    title = re.sub(r"리마스터판|개정판|트리플 특장판|무선 보급판| - .*", "", title)  # 기타 설명 제거
    title = title.replace(":", "") # : 제거
    title = title.strip()  # 앞뒤 공백 제거
    return title

# 작가 정규화 함수
def normalize_authors(author):
    if " 외" in author:
        author = author.replace(" 외", "") # " 외"를 지움
    return author.split(",")[0]  # ','가 나오면 앞쪽 글자만 사용


options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # WARNING 이상의 로그 메시지 만 표시

service = Service('C:/Program Files/Google/Chrome/chromedriver-win64/chromedriver.exe')  # chromedriver의 경로 설정
driver = webdriver.Chrome(service=service, options=options)

num = 10 # 베스트셀러 몇 위까지 출력할건지

url_aladin = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&start=we" # 알라딘 베스트셀러 사이트
url_ypbooks = "https://www.ypbooks.co.kr/bestseller/week" # 영풍문고 베스트셀러 사이트
url_kyobobooks = "https://store.kyobobook.co.kr/bestseller/total/weekly" # 교보문고 베스트셀러 사이트
url_yes24 = "https://www.yes24.com/Product/Category/BestSeller?pageNumber=1&pageSize=24&categoryNumber=001" # yes24 베스트셀러 사이트

aladin_books = [] # 알라딘 책 목록
ypbooks_books = [] # 영풍문고 책 목록
kyobobooks_books = [] # 교보문고 책 목록
yes24_books = [] # yes24 책 목록

aladin_authors = [] # 알라딘 책의 작가 목록
ypbooks_authors = [] # 영풍문고 책의 작가 목록
kyobobooks_authors = [] # 교보문고 책의 작가 목록
yes24_authors = [] # yes24 책의 작가 목록


get_driver(url_aladin, aladin_books, aladin_authors)
get_driver(url_ypbooks, ypbooks_books, ypbooks_authors)
get_driver(url_kyobobooks, kyobobooks_books, kyobobooks_authors)
get_driver(url_yes24, yes24_books, yes24_authors)

# 드라이버 종료
driver.quit()

# 정규화된 제목 리스트 생성
aladin_books_normalized = [normalize_title(title) for title in aladin_books]
ypbooks_books_normalized = [normalize_title(title) for title in ypbooks_books]
kyobobooks_books_normalized = [normalize_title(title) for title in kyobobooks_books]
yes24_books_normalized = [normalize_title(title) for title in yes24_books]


# print("정규화된 알라딘 책 목록:", aladin_books_normalized)
# print("정규화된 영풍문고 책 목록:", ypbooks_books_normalized)
# print("정규화된 교보문고 책 목록:", kyobobooks_books_normalized)
# print("정규화된 YES24 책 목록:", yes24_books_normalized)

# 모든 순위 데이터 통합
all_books = aladin_books_normalized + ypbooks_books_normalized + kyobobooks_books_normalized + yes24_books_normalized

# 책별 언급 횟수 계산
book_counts = Counter(all_books)

# 책별 순위를 저장할 딕셔너리
book_ranks = defaultdict(list)

# 각 책의 순위를 리스트에 저장
for i, book in enumerate(aladin_books_normalized):
    book_ranks[book].append(i + 1)  # 1위부터 시작

for i, book in enumerate(ypbooks_books_normalized):
    book_ranks[book].append(i + 1)

for i, book in enumerate(kyobobooks_books_normalized):
    book_ranks[book].append(i + 1)

for i, book in enumerate(yes24_books_normalized):
    book_ranks[book].append(i + 1)

# 각 책의 평균 순위 계산
average_ranks = {book: np.mean(ranks) for book, ranks in book_ranks.items()}

# 언급 횟수가 2번 이상인 책만 선택
filtered_books = [book for book, count in book_counts.items() if count >= 2]

# 언급 횟수에 따라 정렬
filtered_books.sort(key=lambda x: book_counts[x], reverse=True)

# 정렬된 책의 언급 횟수와 평균 순위
filtered_counts = [book_counts[book] for book in filtered_books]
filtered_avg_ranks = [average_ranks[book] for book in filtered_books]

# 시각화
fig, ax1 = plt.subplots(figsize=(12, 8))

# 첫 번째 y축 - 언급 횟수
ax1.bar(filtered_books, filtered_counts, color='skyblue', label='언급 횟수')
ax1.set_xlabel("책 제목")
ax1.set_ylabel("언급 횟수", color='skyblue')
ax1.tick_params(axis='y', labelcolor='skyblue')

# x축 tick 위치 설정
ax1.set_xticks(np.arange(len(filtered_books)))  # 필터된 작가 수에 맞춰 tick 위치 설정

# x축 tick 레이블 설정
ax1.set_xticklabels(filtered_books, rotation=45, ha="right")

# 두 번째 y축 - 평균 순위
ax2 = ax1.twinx()
ax2.plot(filtered_books, filtered_avg_ranks, color='coral', marker='o', label='평균 순위')
ax2.set_ylabel("평균 순위", color='coral')
ax2.invert_yaxis()  # 순위는 낮을수록 상위이므로 축 반전
ax2.tick_params(axis='y', labelcolor='coral')

# 그래프 제목과 레이블 추가
plt.title("언급 횟수가 2번 이상인 책의 언급 횟수와 평균 순위")



# 정규화된 작가 리스트 생성
aladin_authors_normalized = [normalize_authors(author) for author in aladin_authors]
ypbooks_authors_normalized = [normalize_authors(author) for author in ypbooks_authors]
kyobobooks_authors_normalized = [normalize_authors(author) for author in kyobobooks_authors]
yes24_authors_normalized = [normalize_authors(author) for author in yes24_authors]


# print("정규화된 알라딘 작가 목록:", aladin_authors_normalized)
# print("정규화된 영풍문고 작가 목록:", ypbooks_authors_normalized)
# print("정규화된 교보문고 작가 목록:", kyobobooks_authors_normalized)
# print("정규화된 YES24 작가 목록:", yes24_authors_normalized)

# 작가 통합
all_authors = aladin_authors_normalized + ypbooks_authors_normalized + kyobobooks_authors_normalized + yes24_authors_normalized

# 작가별 언급 횟수 계산
author_counts = Counter(all_authors)

# 작가별 순위를 저장할 딕셔너리
author_ranks = defaultdict(list)

# 각 작가의 순위를 리스트에 저장 (임의의 순위 할당)
for i, author in enumerate(aladin_authors_normalized):
    author_ranks[normalize_authors(author)].append(i + 1)

for i, author in enumerate(ypbooks_authors_normalized):
    author_ranks[normalize_authors(author)].append(i + 1)

for i, author in enumerate(kyobobooks_authors_normalized):
    author_ranks[normalize_authors(author)].append(i + 1)

for i, author in enumerate(yes24_authors_normalized):
    author_ranks[normalize_authors(author)].append(i + 1)

# 각 작가의 평균 순위 계산
average_ranks = {author: np.mean(ranks) for author, ranks in author_ranks.items()}

# 언급 횟수가 2번 이상인 작가만 선택
filtered_authors = [author for author, count in author_counts.items() if count >= 2]

# 언급 횟수에 따라 정렬
filtered_authors.sort(key=lambda x: author_counts[x], reverse=True)

# 정렬된 작가의 언급 횟수와 평균 순위
filtered_counts = [author_counts[author] for author in filtered_authors]
filtered_avg_ranks = [average_ranks[author] for author in filtered_authors]

# 시각화
fig, ax1 = plt.subplots(figsize=(12, 8))

# 첫 번째 y축 - 언급 횟수
ax1.bar(filtered_authors, filtered_counts, color='skyblue', label='언급 횟수')
ax1.set_xlabel("작가 이름")
ax1.set_ylabel("언급 횟수", color='skyblue')
ax1.tick_params(axis='y', labelcolor='skyblue')

# x축 tick 위치 설정
ax1.set_xticks(np.arange(len(filtered_authors)))  # 필터된 작가 수에 맞춰 tick 위치 설정

# x축 tick 레이블 설정
ax1.set_xticklabels(filtered_authors, rotation=45, ha="right")

# 두 번째 y축 - 평균 순위
ax2 = ax1.twinx()
ax2.plot(filtered_authors, filtered_avg_ranks, color='coral', marker='o', label='평균 순위')
ax2.set_ylabel("평균 순위", color='coral')
ax2.invert_yaxis()  # 순위는 낮을수록 상위이므로 축 반전
ax2.tick_params(axis='y', labelcolor='coral')

# 그래프 제목과 레이블 추가
plt.title("언급 횟수가 2번 이상인 작가의 언급 횟수와 평균 순위")
fig.tight_layout()
plt.show()