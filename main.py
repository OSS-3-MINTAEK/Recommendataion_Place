import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance

# csv 데이터 불러오기
cafe_data = pd.read_csv('cafe_place_data.csv', encoding='utf-8')
food_data = pd.read_csv('food_place_data.csv', encoding='utf-8')
tour_data = pd.read_csv('tourist_place_data.csv', encoding='utf-8')
hotel_data = pd.read_csv('hotel_place_data.csv', encoding='utf-8')

def extract_data(data, location):
    result = data[data['지역'].str.contains(location)]
    return result

# 사용자의 위치 입력
locations = ['제주시', '애월읍', '한림읍', '한경면', '대정읍', '인덕면', '중문', '서귀포시', '남원읍', '표선면', '성산읍', '우도', '구좌읍', '조천읍']
print(locations)

while True:
    user_location = input("위치를 입력하세요: ")
    if user_location in locations:
        break

# 사용자의 위치 근처 데이터 추출
near_user_cafe = cafe_data[cafe_data['지역'].str.contains(user_location)]
near_user_food = food_data[food_data['지역'].str.contains(user_location)]
near_user_tour = tour_data[tour_data['지역'].str.contains(user_location)]
near_user_hotel = hotel_data[hotel_data['지역'].str.contains(user_location)]

# 사용자의 위치 위도 경도 불러오기
geolocator = Nominatim(user_agent="geopy")
location = geolocator.geocode(user_location)
if location:
    user_lat, user_lon = location.latitude, location.longitude

# 사용자의 위치와 가게의 거리 차 구하기
def add_distance_row(data, user_lat, user_lon):
    data['거리 차'] = data['위치'].apply(
        lambda x: distance.distance((user_lat, user_lon), geolocator.geocode(x).point).km
        if geolocator.geocode(x) is not None else None)
    
add_distance_row(near_user_cafe, user_lat, user_lon)
add_distance_row(near_user_food, user_lat, user_lon)
add_distance_row(near_user_tour, user_lat, user_lon)
add_distance_row(near_user_hotel, user_lat, user_lon)

# 거리 차가 적은 순으로 정렬하여 상위 5개 추출
result_cafe = near_user_cafe.sort_values(by='거리 차', ascending=True).head(5)[['이름', '거리 차']]
result_food = near_user_food.sort_values(by='거리 차', ascending=True).head(5)[['이름', '거리 차']]
result_tour = near_user_tour.sort_values(by='거리 차', ascending=True).head(5)[['이름', '거리 차']]
result_hotel = near_user_hotel.sort_values(by='거리 차', ascending=True).head(5)[['이름', '거리 차']]

# 결과 출력 함수 정의
def print_results(category, result):
    print(f"--- {category} 순위 ---")
    for i, row in result.iterrows():
        print(f"{i + 1}. {row['이름']}: {row['거리 차']:.4f} km")

# 결과 출력
while True:
    try:
        category = input("확인 하고 싶은 항목을 입력하세요 (카페, 음식점, 관광지, 호텔): ")
        
        if category == "카페":
            result = result_cafe
        elif category == "음식점":
            result = result_food
        elif category == "관광지":
            result = result_tour
        elif category == "호텔":
            result = result_hotel
        else:
            print("잘못된 입력입니다. 다시 시도해주세요.")
            continue
        
        print_results(category, result)
        
    except ValueError:
        print("잘못된 입력입니다. 다시 시도해주세요.")

    row_number = int(input("몇번째 순위를 보고싶은지 입력해주세요 (1~5 입력, 0을 입력하면 종료): "))
    
    if row_number == 0:
        break
    
    try:
        if category == "카페":
            row = result_cafe.iloc[row_number - 1]
        elif category == "음식점":
            row = result_food.iloc[row_number - 1]
        elif category == "관광지":
            row = result_tour.iloc[row_number - 1]
        elif category == "호텔":
            row = result_hotel.iloc[row_number - 1]

        print(f"{category} '{row['이름']}'은/는 {row['거리 차']:.4f} km 만큼 {user_location}로부터 떨어져있습니다.")
    except IndexError:
        print("잘못된 입력입니다. 다시 시도해주세요.")
