import pandas as pd
import googlemaps

# Google Maps API 클라이언트 설정
API_KEY = "AIzaSyBEKIxwQ05ddRKKSOs-ImlpTAeZRxVxd3M"
gmaps = googlemaps.Client(key=API_KEY)

# 엑셀 파일 읽기
file_path = "./tourDB.xls"  # 엑셀 파일 경로
df = pd.read_excel(file_path)

# 상세주소, 위도, 경도 추가할 컬럼 생성
df['상세주소'] = ""
df['위도'] = ""
df['경도'] = ""

# Geocoding 함수 정의
def get_location_info(place_name):
    try:
        geocode_result = gmaps.geocode(place_name, language="ko")  # 언어를 한국어로 설정
        if geocode_result:
            formatted_address = geocode_result[0]['formatted_address']
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            return formatted_address, latitude, longitude
        else:
            return None, None, None
    except Exception as e:
        print(f"Error processing {place_name}: {e}")
        return None, None, None

# 각 장소에 대해 Geocoding 실행
for index, row in df.iterrows():
    place_name = f"{row['이름']} {row['주소']}"
    detailed_address, lat, lng = get_location_info(place_name)
    df.at[index, '상세주소'] = detailed_address
    df.at[index, '위도'] = lat
    df.at[index, '경도'] = lng

# 결과를 엑셀로 저장
output_path = "./tourDB2.xlsx"  # 저장할 파일 경로
df.to_excel(output_path, index=False)

print(f"결과가 저장되었습니다: {output_path}")