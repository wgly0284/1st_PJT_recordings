"""
Google Places API를 사용하여 실제 빵집 사진을 가져오는 스크립트

사용 전 준비사항:
1. Google Cloud Console에서 프로젝트 생성
2. Places API 활성화
3. API 키 발급
4. pip install googlemaps 설치

주의: API 사용량에 따라 비용이 발생할 수 있습니다
무료 할당량: 월 $200 크레딧 (약 28,000개 요청)
"""

import os
import json
import googlemaps
from datetime import datetime

# API 키 설정 (환경변수 또는 직접 입력)
API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', 'YOUR_API_KEY_HERE')

def fetch_bakery_photos(bakery_name, bakery_address):
    """
    Google Places API를 사용하여 빵집 사진 URL을 가져옵니다.

    Args:
        bakery_name: 빵집 이름
        bakery_address: 빵집 주소

    Returns:
        사진 URL 리스트 (최대 3개)
    """
    try:
        gmaps = googlemaps.Client(key=API_KEY)

        # 1. 장소 검색
        places_result = gmaps.places(
            query=f"{bakery_name} {bakery_address}",
            language='ko'
        )

        if not places_result.get('results'):
            print(f"❌ {bakery_name}: 검색 결과 없음")
            return []

        place = places_result['results'][0]
        place_id = place['place_id']

        # 2. 장소 상세 정보 가져오기 (사진 포함)
        place_details = gmaps.place(
            place_id=place_id,
            fields=['photos'],
            language='ko'
        )

        photos = place_details.get('result', {}).get('photos', [])

        if not photos:
            print(f"⚠️ {bakery_name}: 사진 없음")
            return []

        # 3. 사진 URL 생성 (최대 3개)
        photo_urls = []
        for photo in photos[:3]:
            photo_reference = photo['photo_reference']
            # Google Places Photo API URL
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=600&photo_reference={photo_reference}&key={API_KEY}"
            photo_urls.append(photo_url)

        print(f"✅ {bakery_name}: {len(photo_urls)}개 사진 발견")
        return photo_urls

    except Exception as e:
        print(f"❌ {bakery_name} 오류: {str(e)}")
        return []


def update_fixture_with_photos():
    """
    fixture 파일의 모든 가게에 대해 Google Places에서 사진을 가져와 업데이트합니다.
    """
    fixture_path = 'stores/fixtures/busan_west_3gu_bakeries_fixture.json'

    # fixture 파일 읽기
    with open(fixture_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    print(f"총 {len(stores)}개 가게 처리 시작...\n")

    # 각 가게에 대해 사진 가져오기
    for i, store in enumerate(stores, 1):
        name = store['fields']['name']
        address = store['fields']['address']

        print(f"[{i}/{len(stores)}] 처리 중: {name}")

        photo_urls = fetch_bakery_photos(name, address)

        if photo_urls:
            # 첫 번째 사진을 preview_image로 설정
            store['fields']['preview_image'] = photo_urls[0]
            print(f"  → preview_image 업데이트 완료")
        else:
            # 사진을 찾지 못한 경우 기본 이미지 유지
            print(f"  → 기본 이미지 유지")

        # API 할당량 보호를 위해 잠시 대기
        import time
        time.sleep(0.5)  # 초당 2개 요청으로 제한

    # 업데이트된 fixture 파일 저장
    with open(fixture_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 완료! {fixture_path} 파일이 업데이트되었습니다.")


if __name__ == '__main__':
    if API_KEY == 'YOUR_API_KEY_HERE':
        print("⚠️ Google Places API 키를 설정해주세요!")
        print("1. https://console.cloud.google.com/ 접속")
        print("2. 프로젝트 생성 및 Places API 활성화")
        print("3. API 키 발급")
        print("4. 환경변수 설정: export GOOGLE_PLACES_API_KEY='your-api-key'")
        print("   또는 스크립트에 직접 입력")
    else:
        update_fixture_with_photos()
