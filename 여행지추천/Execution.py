import cv2
from tkinter import Label
from io import BytesIO
from PIL import Image, ImageTk
import requests
import tkinter as tk
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import math
import turtle
import time

font_path = "C:/Windows/Fonts/malgun.ttf"
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()



def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구의 반지름 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def ma(df):
    try:
        root.destroy()
    except:
        pass

    while True:
        # 사용자 입력 받기
        user_input = input("\n 0을 입력하면 그래프 출력, 1을 입력하면 세부 입력칸 표시, 2를 입력하면 선택된 여행지 선정,  3을 입력하면 랜덤 여행지 선정, 4을 입력하면 전체 정보 출력, 5를 입력하면 종료: ")

        if user_input == '0':
            # 0을 입력하면 그래프 출력
            plot_graph(df)

        elif user_input == '1':
            # 1을 입력하면 세부 입력칸 표시
            additional_input(df)

        elif user_input == '2':
            #2를 입력하면 선택된 여행지 루트 출력
            get_wish_name_and_travel(df)

        elif user_input == '3':
            # 3을 입력하면 랜덤 여행지 루트트 출력
            find_closest_names(df)
        elif user_input == '4':
            print(df.head(10))
            if df.shape[0] > 10:
                print(f"등 {df.shape[0] - 10}개가 있습니다.")

        elif user_input == '5':
            # 3를 입력하면 뒤로 가기
            print("프로그램을 종료합니다.")
            quit()
        
        else:
            print("잘못된 입력입니다. 0, 1, 2, 3 중 하나를 입력하세요.")

def plot_graph(df):
    """경도(x)와 위도(y)를 이용해 그래프를 출력"""
    x = df['경도']
    y = df['위도']

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', label='위치')
    plt.title('경도와 위도의 분포')
    plt.xlabel('경도')
    plt.ylabel('위도')
    plt.legend()
    plt.grid()
    plt.show()


def safe_plot_turtle_graph(df2):
    scaling_factor = 10000

    def reset_turtle():
        try:
            turtle.bye()  # 기존 Turtle 창 닫기
        except turtle.Terminator:
            pass  # 이미 창이 닫혀 있으면 무시

        # Turtle 객체 초기화
        turtle.TurtleScreen._RUNNING = True  # 내부 상태 리셋

    # Turtle 실행 로직
    def plot_turtle_graph():
        screen = turtle.Screen()

        min_longitude = df2['경도'].min() - 127  # 기준점 보정
        max_longitude = df2['경도'].max() - 127
        min_latitude = df2['위도'].min() - 37.5
        max_latitude = df2['위도'].max() - 37.5

        screen.setworldcoordinates(
            (min_longitude * scaling_factor) - 100,
            (min_latitude * scaling_factor) - 100,
            (max_longitude * scaling_factor) + 100,
            (max_latitude * scaling_factor) + 100,
        )

        t = turtle.Turtle()

        # 출발점 설정
        t.penup()
        t.speed(100)
        t.goto((df2.iloc[0]['경도'] - 127) * scaling_factor, 
               (df2.iloc[0]['위도'] - 37.5) * scaling_factor)
        t.speed(2)
        t.pendown()

        for i in range(1, len(df2)):
            t.goto((df2.iloc[i]['경도'] - 127) * scaling_factor, 
                   (df2.iloc[i]['위도'] - 37.5) * scaling_factor)
            time.sleep(1)

        t.hideturtle()  # Turtle 숨기기
        screen.mainloop()  # GUI 유지

    try:
        plot_turtle_graph()
    except turtle.Terminator:
        reset_turtle()  # 기존 세션 초기화
        plot_turtle_graph()  # 다시 실행

desired_address = []

def additional_input(df):
    # '주소' 컬럼의 고유한 값 가져오기
    unique_addresses = df['주소'].unique()
    while True:
        user_input = input("주소에 포함된 특정 문자를 입력하세요(0을 입력하면 입력을 종료합니다.): ")

        if user_input == '0':
            # 원하는 주소에 해당하는 행만 필터링
            filtered_df = df[df['주소'].isin(desired_address)]
            print("입력을 종료합니다.")
            ma(filtered_df)  # ma 함수 호출
            return  # 함수 종료

        # 입력한 문자가 포함된 주소 필터링
        filtered_addresses = [address for address in unique_addresses if user_input in address]

        if len(filtered_addresses) == 1:
            if filtered_addresses[0] not in desired_address:
                desired_address.append(filtered_addresses[0])
                print(f"{filtered_addresses[0]}가 원하는 주소에 추가되었습니다.")
            else:
                print(f"{filtered_addresses[0]}는 이미 추가된 주소입니다.")
            print(f"현재까지 추가된 원하는 장소: {desired_address}")
        elif len(filtered_addresses) > 1:
            # 여러 배열이 결과로 나온 경우
            print("더 정확한 단어로 입력해주세요.")
        else:
            # 아무 결과도 나오지 않은 경우
            print("해당 문자가 포함된 주소를 찾을 수 없습니다.")


def next_travel(df, r, visited, is_first=False):
    random_name = r['이름']
    random_lat = r['위도']
    random_lon = r['경도']

    if is_first:  # 첫 번째 랜덤 선택된 이름은 출력
        print(f"\n선택된 이름: {random_name}")

    # 랜덤 선택된 행과 다른 행 간의 거리 계산
    distances = []
    for _, row in df.iterrows():
        if row['이름'] != random_name and row['이름'] not in visited:  # 이미 방문한 곳은 제외
            distance = haversine(random_lat, random_lon, row['위도'], row['경도'])
            distances.append((row['이름'], distance))

    # 가장 가까운 여행지 찾기
    if distances:
        closest_name, closest_distance = min(distances, key=lambda x: x[1])
        print(f"\n다음 여행지: {closest_name} (거리: {closest_distance:.2f} km)")

        # 경로 출력 (네이버 지도 API로 경로 조회)
        print(f"경로 확인: {random_name} -> {closest_name}")
        get_transit_route_info(random_lat, random_lon, df[df['이름'] == closest_name].iloc[0]['위도'],
                       df[df['이름'] == closest_name].iloc[0]['경도'])

        # 가장 가까운 여행지의 행을 반환
        closest_row = df[df['이름'] == closest_name].iloc[0]
        visited.add(closest_name)  # 방문한 장소 기록
        return closest_row
    else:
        print("다른 여행지가 없습니다.")
        return None

def get_transit_route_info(start_lat, start_lon, end_lat, end_lon, departure_time="now"):
    # Google Maps API 키 설정
    API_KEY = "AIzaSyBEKIxwQ05ddRKKSOs-ImlpTAeZRxVxd3M"
    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": f"{start_lat},{start_lon}",  # 출발 좌표
        "destination": f"{end_lat},{end_lon}",  # 도착 좌표
        "mode": "transit",  # 대중교통
        "departure_time": departure_time,  # 출발 시간
        "language": "ko",  # 한국어
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            # 첫 번째 경로를 선택
            route = data["routes"][0]
            legs = route["legs"][0]

            print(f"전체 경로 거리: {legs['distance']['text']}")
            print(f"전체 경로 소요 시간: {legs['duration']['text']}")
            # print(f"예상 도착 일시: {legs['arrival_time']['text']}")
            steps = legs["steps"]

            print("\n[세부 경로]")
            for step in steps:
                print(f"- {step['html_instructions']} ({step['duration']['text']})")
        else:
            print(f"API 에러: {data['status']}")
    else:
        print("대중교통 경로 정보를 가져오는 데 실패했습니다.")

def find_closest_names(df):
    # 방문한 장소를 기록할 집합
    visited = set()
    selected_rows = []  # 선택된 장소 정보를 저장할 리스트

    # 랜덤으로 이름 선택
    random_row = df.sample(n=1).iloc[0]
    visited.add(random_row['이름'])  # 첫 번째 장소를 방문한 장소로 기록
    selected_rows.append(random_row)  # 시작 장소 추가

    # 첫 번째 장소를 선택한 경우
    closest_row = next_travel(df, random_row, visited, is_first=True)
    if closest_row is not None:
        selected_rows.append(closest_row)
        closest_row2 = next_travel(df, closest_row, visited)
        if closest_row2 is not None:
            selected_rows.append(closest_row2)
            closest_row3 = next_travel(df, closest_row2, visited)
            if closest_row3 is not None:
                selected_rows.append(closest_row3)
                closest_row4 = next_travel(df, closest_row3, visited)
                if closest_row4 is not None:
                    selected_rows.append(closest_row4)

    # 선택된 행으로 새로운 데이터프레임 생성
    df2 = pd.DataFrame(selected_rows)

    # 이미지 URL을 Tkinter로 출력
    display_images_with_tkinter(df2)
    user_graph_input = input("\n1을 누르면 위치 그래프 출력, 0을 누르면 패스: ")
    if user_graph_input == '1':
        plot_graph(df2)
        safe_plot_turtle_graph(df2)

def get_wish_name_and_travel(df):
    print(df['이름'].unique())
    # 사용자가 원하는 이름을 저장할 리스트
    wish_name = []
    
    while True:
        user_input = input("\n여행지 이름(문자 포함) 입력 (0을 입력하면 종료): ")

        if user_input == '0':
            # 입력 종료
            if not wish_name:
                print("입력된 여행지가 없습니다. 메뉴로 돌아갑니다.")
                ma(df)  # 메뉴로 돌아가기
            break

        # 사용자 입력과 '이름' 열 비교
        matching_rows = df[df['이름'].str.contains(user_input, case=False, na=False)]

        if len(matching_rows) == 0:
            print("해당 문자가 포함된 이름을 찾을 수 없습니다. 다시 입력하세요.")
        elif len(matching_rows) > 1:
            print("해당 문자가 포함된 이름이 여러 개 있습니다. 더 정확한 단어로 입력해주세요.")
            print(f"가능한 여행지: {', '.join(matching_rows['이름'].tolist())}")
        else:
            # 이름이 정확히 1개일 때
            selected_name = matching_rows.iloc[0]['이름']
            print(f"여행지 '{selected_name}'을(를) 선택했습니다.")
            wish_name.append(selected_name)
            break

    # 선택된 이름으로 시작
    if wish_name:
        start_row = df[df['이름'] == wish_name[0]].iloc[0]
        print(f"\n시작 여행지: {start_row['이름']}")
        # 방문한 장소 기록
        visited = set()
        visited.add(start_row['이름'])

        # 경로를 저장할 리스트
        selected_rows = [start_row]

        # 여행 진행
        closest_row = next_travel(df, start_row, visited, is_first=True)
        if closest_row is not None:
            selected_rows.append(closest_row)
            closest_row2 = next_travel(df, closest_row, visited)
            if closest_row2 is not None:
                selected_rows.append(closest_row2)
                closest_row3 = next_travel(df, closest_row2, visited)
                if closest_row3 is not None:
                    selected_rows.append(closest_row3)
                    closest_row4 = next_travel(df, closest_row3, visited)
                    if closest_row4 is not None:
                        selected_rows.append(closest_row4)

        # 선택된 행들로 새로운 데이터프레임 생성
        df2 = pd.DataFrame(selected_rows)

        # Tkinter를 사용하여 이미지 출력
        display_images_with_tkinter(df2)
        user_graph_input = input("\n1을 누르면 위치 그래프 출력, 0을 누르면 패스: ")
        if user_graph_input == '1':
            plot_graph(df2)   
            safe_plot_turtle_graph(df2)

    else:
        print("여행지를 선택하지 않아 초기 메뉴로 돌아갑니다.")
        ma(df)


def display_images_with_tkinter(df2):
    # Tkinter 창 생성
    root2 = tk.Tk()
    root2.title("여행지 이미지")

    # 이미지와 이름을 출력
    for index, row in df2.iterrows():
        frame = tk.Frame(root2)
        frame.pack(pady=10)

        # 이미지 다운로드 및 변환
        image_url = row.get('이미지', None)
        if image_url:
            photo = download_and_convert_image(image_url, size=(100, 100))
            if photo:
                label_image = tk.Label(frame, image=photo)
                label_image.image = photo  # 참조 유지
                label_image.pack(side=tk.LEFT)

        # 여행지 이름 표시
        label_name = tk.Label(frame, text=row['이름'], font=("Arial", 12))
        label_name.pack(side=tk.LEFT, padx=10)

    # Tkinter 메인 루프 실행
    root2.mainloop()






# URL에서 이미지를 다운로드하고 ImageTk 객체로 변환하는 함수
def download_and_convert_image(url, size=(50, 50)):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 요청 상태 확인
        image = Image.open(BytesIO(response.content))  # 이미지 로드
        image = image.resize(size, Image.LANCZOS)  # 이미지 크기 조정
        return ImageTk.PhotoImage(image)  # ImageTk로 변환
    except Exception as e:
        print(f"이미지를 다운로드하거나 변환하는 중 오류 발생: {e}")
        return None

def load_and_resize_image(filepath, size):
    image = Image.open(filepath)
    return image.resize(size, Image.LANCZOS)


def submit():
    # Excel 파일 경로
    excel_path = "./tourDB3.xlsx"

    # Excel 파일 읽기
    df = pd.read_excel(excel_path)
    selected_types = []
    selected_places = []

    # 체크박스에서 선택된 장소 유형 출력
    if var_A.get() == 1:
        selected_types.append("박물관")
    if var_B.get() == 1:
        selected_types.append("공원")
    if var_C.get() == 1:
        selected_types.append("자연/지형")
    if var_D.get() == 1:
        selected_types.append("상업")
    if var_E.get() == 1:
        selected_types.append("문화/전통")
    if var_F.get() == 1:
        selected_types.append("강/수변공간")
    if var_G.get() == 1:
        selected_types.append("시장")
    if var_H.get() == 1:
        selected_types.append("종교/역사")
    if var_A.get() == 0 and var_B.get() == 0 and var_C.get() == 0 and var_D.get() == 0 and var_E.get() == 0 and var_F.get() == 0 and var_G.get() == 0 and var_H.get() == 0:
        selected_types.append("박물관")
        selected_types.append("공원")
        selected_types.append("자연/지형")
        selected_types.append("상업")
        selected_types.append("문화/전통")
        selected_types.append("강/수변공간")
        selected_types.append("시장")
        selected_types.append("종교/역사")
    # 선택된 장소 출력
    selected_place_index = place_var.get()
    if selected_place_index == 0:  # 전국을 선택했을 경우
        # 전국을 선택했으면 모든 장소를 선택한 것처럼 처리
        selected_places = [
            "서울", "경기", "인천", "대전", "대구", "광주", "부산", "울산",
            "강원", "충북", "충남", "경북", "경남", "전북", "전남", "제주", "세종"
        ]
    else:
        # 전국을 선택하지 않았다면 해당 장소만 선택
        selected_places.append(place_array[selected_place_index*2])

    print("선택된 장소 유형:", selected_types)
    print("선택된 장소:", selected_places)

    # '종류' 조건 필터링
    type_filter = df['종류'].isin(selected_types)

    if selected_place_index != 0:
        place_filter = df['주소'].str.startswith(selected_places[0], na=False)
        filtered_df = df[type_filter & place_filter]
    else:
        filtered_df = df[type_filter]

    # 결과 출력
    # print(filtered_df)
    print(f"선택한 종류의 여행지는 {filtered_df['주소'].unique()}에 있습니다.")
    ma(filtered_df)


print("체크박스를 체크한 후 시작 버튼을 눌러주세요.")
root = tk.Tk()
root.title("여행 정보 선택")


# 체크박스 변수 생성
var_A = tk.IntVar()
var_B = tk.IntVar()
var_C = tk.IntVar()
var_D = tk.IntVar()
var_E = tk.IntVar()
var_F = tk.IntVar()
var_G = tk.IntVar()
var_H = tk.IntVar()


place_var = tk.IntVar(value=0)

size = (50, 50)  # 원하는 크기 지정 (예: 100x100)
All = load_and_resize_image("./pic/all.png", size)
Seoul = load_and_resize_image("./pic/Seoul.jpg", size)
Gyeonggi = load_and_resize_image("./pic/Gyeonggi.jpg", size)
Incheon = load_and_resize_image("./pic/Incheon.jpg", size)
Daejeon = load_and_resize_image("./pic/Daejeon.jpg", size)
Daegu = load_and_resize_image("./pic/Daegu.jpg", size)
Gwangju = load_and_resize_image("./pic/Gwangju.jpg", size)
Busan = load_and_resize_image("./pic/Busan.jpg", size)
Ulsan = load_and_resize_image("./pic/Ulsan.jpg", size)
Gangwon = load_and_resize_image("./pic/Gangwon.jpg", size)
Chungbuk = load_and_resize_image("./pic/Chungbuk.jpg", size)
Chungnam = load_and_resize_image("./pic/Chungnam.jpg", size)
Gyeongbuk = load_and_resize_image("./pic/Gyeongbuk.jpg", size)
Gyeongnam = load_and_resize_image("./pic/Gyeongnam.jpg", size)
Jeonbuk = load_and_resize_image("./pic/Jeonbuk.jpg", size)
Jeonnam = load_and_resize_image("./pic/Jeonnam.jpg", size)
Jeju = load_and_resize_image("./pic/Jeju.jpg", size)
Sejong = load_and_resize_image("./pic/Sejong.jpg", size)

# ImageTk 객체로 변환
image_All = ImageTk.PhotoImage(All)
image_Seoul = ImageTk.PhotoImage(Seoul)
image_Gyeonggi = ImageTk.PhotoImage(Gyeonggi)
image_Incheon = ImageTk.PhotoImage(Incheon)
image_Daejeon = ImageTk.PhotoImage(Daejeon)
image_Daegu = ImageTk.PhotoImage(Daegu)
image_Gwangju = ImageTk.PhotoImage(Gwangju)
image_Busan = ImageTk.PhotoImage(Busan)
image_Ulsan = ImageTk.PhotoImage(Ulsan)
image_Gangwon = ImageTk.PhotoImage(Gangwon)
image_Chungbuk = ImageTk.PhotoImage(Chungbuk)
image_Chungnam = ImageTk.PhotoImage(Chungnam)
image_Gyeongbuk = ImageTk.PhotoImage(Gyeongbuk)
image_Gyeongnam = ImageTk.PhotoImage(Gyeongnam)
image_Jeonbuk = ImageTk.PhotoImage(Jeonbuk)
image_Jeonnam = ImageTk.PhotoImage(Jeonnam)
image_Jeju = ImageTk.PhotoImage(Jeju)
image_Sejong = ImageTk.PhotoImage(Sejong)


url_dict = {
    "박물관": "https://cdn.visitkorea.or.kr/img/call?cmd=VIEW&id=db57ed01-0281-4826-8bba-d9526eeabf83",
    "공원": "https://cdn.visitkorea.or.kr/img/call?cmd=VIEW&id=1da5aec8-9e48-4012-8e32-52d5e1895a3f",
    "자연/지형": "https://cdn.visitkorea.or.kr/img/call?cmd=VIEW&id=4a302ec7-8a96-4414-bde5-9c930da19f71",
    "상업": "https://cdn.visitkorea.or.kr/img/call?cmd=VIEW&id=e7882449-3fb8-48d5-a99b-9ac6d4a0a772",
    "문화/전통": "https://cdn.visitkorea.or.kr/img/call?cmd=VIEW&id=68465502-1beb-4da7-9823-d1fdf01f2246",
    "강/수변공간": "https://cdn.visitkorea.or.kr/img/call?cmd=VIEW&id=89c2f735-d9d7-42f1-84df-c7a20c294314",
    "시장": "https://cdn.visitkorea.or.kr/img/call?cmd=VIEW&id=37e6e02c-2469-4f99-bb0e-efe86da41c7e",
    "종교/역사": "https://cdn.visitkorea.or.kr/img/call?cmd=VIEW&id=01f3a33d-e812-4818-ad81-c64417071c62",
}

image_dict = {}
for name, url in url_dict.items():
    image_dict[name] = download_and_convert_image(url)


tk.Label(root, text="장소 유형:").grid(row=0, column=0, sticky='w')

checkbutton1 = tk.Checkbutton(root, text="박물관", variable=var_A)
checkbutton1.grid(row=1, column=0, sticky='w')
image_label1 = Label(root, image=image_dict["박물관"])
image_label1.grid(row=1, column=1, sticky='e')

checkbutton2 = tk.Checkbutton(root, text="공원", variable=var_B)
checkbutton2.grid(row=2, column=0, sticky='w')
image_label2 = Label(root, image=image_dict["공원"])
image_label2.grid(row=2, column=1, sticky='e')

checkbutton3 = tk.Checkbutton(root, text="자연/지형", variable=var_C)
checkbutton3.grid(row=3, column=0, sticky='w')
image_label3 = Label(root, image=image_dict["자연/지형"])
image_label3.grid(row=3, column=1, sticky='e')

checkbutton4 = tk.Checkbutton(root, text="상업", variable=var_D)
checkbutton4.grid(row=4, column=0, sticky='w')
image_label4 = Label(root, image=image_dict["상업"])
image_label4.grid(row=4, column=1, sticky='e')

checkbutton5 = tk.Checkbutton(root, text="문화/전통", variable=var_E)
checkbutton5.grid(row=5, column=0, sticky='w')
image_label5 = Label(root, image=image_dict["문화/전통"])
image_label5.grid(row=5, column=1, sticky='e')

checkbutton6 = tk.Checkbutton(root, text="강/수변공간", variable=var_F)
checkbutton6.grid(row=6, column=0, sticky='w')
image_label6 = Label(root, image=image_dict["강/수변공간"])
image_label6.grid(row=6, column=1, sticky='e')

checkbutton7 = tk.Checkbutton(root, text="시장", variable=var_G)
checkbutton7.grid(row=7, column=0, sticky='w')
image_label7 = Label(root, image=image_dict["시장"])
image_label7.grid(row=7, column=1, sticky='e')

checkbutton8 = tk.Checkbutton(root, text="종교/역사", variable=var_H)
checkbutton8.grid(row=8, column=0, sticky='w')
image_label8 = Label(root, image=image_dict["종교/역사"])
image_label8.grid(row=8, column=1, sticky='e')


tk.Label(root, text="장소 위치:").grid(row=0, column=2, sticky='w')

place_array = [
    "전국", image_All,
    "서울", image_Seoul,
    "경기", image_Gyeonggi,
    "인천", image_Incheon,
    "대전", image_Daejeon,
    "대구", image_Daegu,
    "광주", image_Gwangju,
    "부산", image_Busan,
    "울산", image_Ulsan,
    "강원", image_Gangwon,
    "충북", image_Chungbuk,
    "충남", image_Chungnam,
    "경북", image_Gyeongbuk,
    "경남", image_Gyeongnam,
    "전북", image_Jeonbuk,
    "전남", image_Jeonnam,
    "제주", image_Jeju,
    "세종", image_Sejong
]
checkbutton = []
image_label = []

for i in range(len(place_array)//2):
    checkbutton.append(tk.Radiobutton(root, text=place_array[i*2], variable=place_var, value=i))
    checkbutton[i].grid(row=i+1, column=2, sticky='w')
    image_label.append(Label(root, image=place_array[i*2 + 1]))
    image_label[i].grid(row=i+1, column=3, sticky='e')


tk.Button(root, text="시작", command=submit).grid(row=27, column=0, columnspan=4, sticky='ew')

# 창 실행
root.mainloop()



