import pandas as pd

# 엑셀 파일 경로
file_path = './tourDB2.xlsx'

# 분류 함수 정의
def classify_place(place):
    if any(keyword in place for keyword in [
        "공원", "숲", "산", "하늘", "수목원", "정원", "꽃", "마루", "광장", "파크", "수풀"
        "유원지", "군락지", "놀이터", "도시공원", "생태공원", "휴식공간", "식물원", "공원길", "분수", "대왕암", "뜰", "청남대"]) or (place.endswith("길") and "메타세쿼이아" in place):
        return "공원"
    elif any(keyword in place for keyword in [
        "박물관", "미술관", "역사관", "문학관", "전시관", "과학관", "기념관", "자원관", 
        "물문화관", "천문대", "생태관", "생태원", "맨숀", "기록관", "뮤지엄", "체험관", "문화재관", "역사박물관", "아트", 
        "학습원", "연구소", "카멜리아힐", "태권도", "다빈치", "빛의"]) or place.endswith("관"):
        return "박물관"
    elif any(keyword in place for keyword in [
        "시장", "마켓", "백화점", "상가", "쇼핑몰", "아울렛", "거리", "장수장", "고창장", "해리장", "김제장", "마량장", "일로장", "경화장", "밀양장", "의령장", "거창장", "김포장", "용인장",
        "미원장", "청양장", "판교장", "광천장", "풍기장", "풍각장", "영덕장", "흥해장", "자인장", "함창장", "청도장","왜관장", "장기장",
        "장터", "트래블라운지", "골목", "마트", "전통시장", "상점가", "도매시장", "합덕장", "아랫장", "신령장", "진천장", "구룡포장", "무안장", "창평장","군위장","함평장", "고흥장", "함열장", "5일장",
        "영천장", "통리장","신탄진장", "대야장", "직매장"]):
        return "시장"
    elif any(keyword in place for keyword in [
        "호텔", "빌딩", "타워", "몰", "갤러리", "컨벤션센터", "아쿠아", "리조트", 
        "아이파크", "롯데월드", "테마파크", "랜드", "트리플스트리트", 
        "트라이볼", "트래블라운지", "크루즈터미널", "월드", "온천", "체육관", "스퀘어", "체험장", "센터",
        "극장", "방송", "쇼핑몰", "레스토랑", "가든", "동물원","쥬", "스튜디오", "농장", "목장", "농원", "베이", "도시", "스카이", 
        "경기장", "해수", "터미널", "카페", "플랫폼", "엑스코", "집", "로드", "단지", "신세계", "벡스코", "프라자", "클럽", 
        "시티", "스파", "리움", "소금", "스타", "스토어", "우체국", "양모리", "쉼터", "MBC", "양조장", "바이크", "레일", "공방", 
        "서바이벌", "샵", "포레스트", "와이어", "짚", "코스터", "플레이", "시네마", "마켙", "신라스테이", "더", "컨벤", "초록잎", 
        "창고", "책방", "쇼", "순솝",  "팜", "상회", "공장","체험", "피아크", 
        "쁘띠", "킨텍스", "농부",  "커피", "크래프트", "휴게소", "찜질", "탕", "직판",  "스페이스", 
        "밭","열차", "조합", "협동", "키자", "야구", "오레", "그라운드", "케이슨", "코스모", 
        "참치", "오래", "디움", "하우스", "프렐류드", "MRNW", "오남제", "폴리", "허심청", "F", "웨이브서프", "루덴", "로만", "피아", "스몹", 
        "그리팅", "K", "와글", "스토리", "오아시스", "카포레", "이함", "캠프", "코리아", "라베", "올드타임", "양주르", "테르", "휘닉스", 
        "하트", "메이즈", "해피주", "알펜", "슬라이드", "리솜", "밸리", "어드벤처", "냉풍", "굿밤", "소노벨", "프로방스", "주렁", "구미코", "복만네", 
        "파머스", "아난티", "디피랑", "배건네", "샤또", "트리스쿨", "타루비", "전주일몽", "녹테마레", "슈퍼", "떼", "대합실", "쉼한모금", "위판장", "꿈누리터"]) or place.endswith("점") or place.endswith("원"):
        return "상업"
    elif any(keyword in place for keyword in [
        "한강", "섬", "돔", "해변", "해수욕장", "강", "바다", "포구", "선착장", 
        "수변", "해안도로", "부두", "갑문", "항", "대청호", "습지", "저수지", "수원지", "호수", "강변", "수변공원", "수로", "해안", "유람선", "여객선", "우도", "댐", "못", "늪", "잠수", "요트", "크루즈", "하화도", "상화도", "파로호", "해협", "소양호", "경포호", "서핑", "비치", 
        "캠핑", "증도", "송도코마린", "청평호반", "추도", "죽도", "수륙양용"]) or place.endswith("도")  or place.endswith("천") or place.endswith("호") or place.endswith("지"):
        return "강/수변공간"
    elif any(keyword in place for keyword in [
        "궁", "마을", "한옥마을", "민속", "타운", "전통", "고분", "유적", "전적지", 
        "둘레길", "묘소", "문화", "문화유산", "유적지", "사찰", "생가", "석빙고", "옛", "암각화", "성", "처용암", 
        "갑곶돈대", "판문점", "척화비", "세트장", "염전", "릉", "기념비", "다리", "유엔", "촬영", "고을", "대왕", 
        "첨성대", "묘", "관광", "고가", "한복", "가옥", "동해역", "석실", "동네", "관문", "망향대", "도가" ,"도예", 
        "두물머리", "옥수영장", "여주도자세상", "덕포진", "동해비", "서운재", "대장간", "금병헌", "초전댁", "고백비", 
        "직물", "도석" ,"국조전", "최참판댁", "벽골제", "난장", "통문", "목물", "등기소", "통일전", "통제영", "만인의총", 
        "오송제", "홍주아문", "경기전"]) or place.endswith("촌") or place.endswith("역") or place.endswith("골") or place.endswith("택"):
        return "문화/전통"
    elif any(keyword in place for keyword in [
        "바위", "폭포", "굴", "계곡", "산책로", "휴양림", "나무", "길", "산림", "산", "등산로", "화석", "두무진", 
        "케이블카", "알프스", "고개", "언덕", "암", "약수", "터널", "주상절리", "섭지코지", "쇠소깍", "오름", "적벽", 
        "담", "봉", "전망", "고드름", "이기대", "계단", "간월재", "우체통", "해우재", "반룡송", "파주임진팔경",
        "수연목서", "8경", "노송지대", "수풀로", "개울", "맑은물", "마지기", "하조대", "핀란드", "오색령", "청령포", "비선대", 
        "보발재", "구곡", "제림", "박달재", "석문", "도마령", "9경", "단양노트", "팔경", "눈바래다", "유구천", "천수만", "합덕제", "방조제",
        "고북제", "부용대", "회룡포", "진남교반", "계림", "문장대", "돌할매", "협곡", "선몽대", "죽령", "석송령", "울진토염",
        "위양지", "보타니아", "수승대", "지안재", "어부림", "임경대", "연화도", "하동송림", "방초", "충돌구", "다초지", "33경",
        "오목대", "원림", "죽화경", "도리포", "비자림", "외돌개", "보롬왓", "별방진"]) or (place.endswith("로") or place.endswith("탑") or place.endswith("루")):
        return "자연/지형"
    elif any(keyword in place for keyword in [
        "사", "성당", "교회", "묘지", "사찰", "초지진", "순교", "성지", "현충원", "당", "정", "향교", "서원", "여래입상", "미륵", "불병좌상", 
        "석불", "원불"]) or place.endswith("각"):
        return "종교/역사"
    else:
        return "기타"
# 엑셀 파일 읽기
df = pd.read_excel(file_path)

# "종류" 열 추가
df["종류"] = df["이름"].apply(classify_place)

# 엑셀 파일 저장
output_file = './tourDB3.xlsx'
df.to_excel(output_file, index=False)

print(f"분류된 데이터가 '{output_file}' 파일에 저장되었습니다.")