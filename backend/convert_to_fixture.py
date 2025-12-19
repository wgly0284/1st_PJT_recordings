import json
import os

def convert():
    # 1. 원본 데이터 로드
    raw_file_path = 'data/FINAL_DATA.json'
    if not os.path.exists(raw_file_path):
        print(f"❌ 에러: {raw_file_path} 파일이 없습니다.")
        return

    with open(raw_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixtures = []
    for i, item in enumerate(data, start=1):
        # 카테고리 추론 로직
        name = item.get('name', '')
        category = 'ETC'
        if '케이크' in name or '케익' in name:
            category = 'CAKE'
        elif '쿠키' in name:
            category = 'COOKIE'
        elif '베이커리' in name or '빵' in name:
            category = 'PASTRY'

        # 영업시간 기본값 처리 (요청하신 10:30 ~ 22:00)
        business_hours = item.get('operating_hours') or '10:30 ~ 22:00'

        # Django Fixture 구조 생성
        fixture_item = {
            "model": "stores.store",
            "pk": i,
            "fields": {
                "name": item['name'],
                "address": item['address'],
                "latitude": str(item['latitude']),
                "longitude": str(item['longitude']),
                "category": category,
                "business_hours": business_hours,
                "contact": item.get('contact_tel') or '',
                "description": item.get('description') or '',
                "avg_rating": 0.0,
                "created_at": "2024-01-01T00:00:00Z" # 기본값
            }
        }
        fixtures.append(fixture_item)

    # 2. Fixture 폴더 생성 및 저장
    output_dir = 'stores/fixtures'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/stores_data.json', 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, ensure_ascii=False, indent=2)

    print(f"✅ 성공: {len(fixtures)}개의 데이터를 stores/fixtures/stores_data.json으로 변환했습니다.")

if __name__ == "__main__":
    convert()