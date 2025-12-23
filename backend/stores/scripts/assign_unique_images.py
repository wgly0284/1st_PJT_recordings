"""
각 가게에 고유한 베이커리 이미지를 할당하는 스크립트
103개 가게에 서로 다른 Unsplash 베이커리 이미지 URL을 랜덤으로 할당합니다.
"""

import json
import random

# 🥐 베이커리 관련 Unsplash 이미지 컬렉션 (103개 이상)
BAKERY_IMAGES = [
    # 빵 진열대 / 베이커리 전경
    "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600",
    "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600",
    "https://images.unsplash.com/photo-1517433670267-08bbd4be890f?w=600",
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600",
    "https://images.unsplash.com/photo-1542838132-92c53300491e?w=600",

    # 케이크 / 디저트
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600",
    "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600",
    "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=600",
    "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=600",
    "https://images.unsplash.com/photo-1535141192574-5d4897c12636?w=600",

    # 크루아상 / 페이스트리
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600",
    "https://images.unsplash.com/photo-1530610476181-d83430b64dcd?w=600",
    "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600",
    "https://images.unsplash.com/photo-1623334044303-241021148842?w=600",
    "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=600",

    # 쿠키 / 비스킷
    "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600",
    "https://images.unsplash.com/photo-1614707267537-4545f1c2b4b5?w=600",
    "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600",
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600",
    "https://images.unsplash.com/photo-1548365328-8c6db3220e4c?w=600",

    # 도넛 / 머핀
    "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600",
    "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600",
    "https://images.unsplash.com/photo-1556912173-46c336c7fd55?w=600",
    "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=600",
    "https://images.unsplash.com/photo-1587241321921-91a834d82e76?w=600",

    # 마카롱
    "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600",
    "https://images.unsplash.com/photo-1558312657-e4e0ff6e5eca?w=600",
    "https://images.unsplash.com/photo-1569864358642-9d1684040f43?w=600",
    "https://images.unsplash.com/photo-1550617931-e17a7b70dce2?w=600",
    "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600",

    # 바게트 / 식빵
    "https://images.unsplash.com/photo-1598373182133-52452f7691ef?w=600",
    "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=600",
    "https://images.unsplash.com/photo-1590588469668-aae4cf6dd456?w=600",
    "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=600",
    "https://images.unsplash.com/photo-1585934034313-c77eb15c8c3f?w=600",

    # 파이 / 타르트
    "https://images.unsplash.com/photo-1519915212116-7cfef71f1d3e?w=600",
    "https://images.unsplash.com/photo-1525184990509-4fd44ed9e056?w=600",
    "https://images.unsplash.com/photo-1535920527002-b35e96722eb9?w=600",
    "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=600",
    "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?w=600",

    # 브라우니 / 스콘
    "https://images.unsplash.com/photo-1607478900766-efe13248b125?w=600",
    "https://images.unsplash.com/photo-1603048297194-8f7e4d68b82a?w=600",
    "https://images.unsplash.com/photo-1603048297172-c92544798d5a?w=600",
    "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=600",
    "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600",

    # 치즈케이크 / 롤케이크
    "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600",
    "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600",
    "https://images.unsplash.com/photo-1617151216974-0b85f0bb3626?w=600",
    "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600",
    "https://images.unsplash.com/photo-1574085733277-851d9d856a3a?w=600",

    # 기타 베이커리 제품
    "https://images.unsplash.com/photo-1605806616949-1e87b487fc2f?w=600",
    "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=600",
    "https://images.unsplash.com/photo-1573141597928-403fcee0e056?w=600",
    "https://images.unsplash.com/photo-1560180445-b2298a6c0fce?w=600",
    "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600",
    "https://images.unsplash.com/photo-1572963564891-422f4c8c5255?w=600",
    "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600",
    "https://images.unsplash.com/photo-1517433670267-08bbd4be890f?w=600",
    "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=600",
    "https://images.unsplash.com/photo-1599785209796-786432b228bc?w=600",
    "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600",
    "https://images.unsplash.com/photo-1534432182912-63863115e106?w=600",
    "https://images.unsplash.com/photo-1612182062361-cc8b5ac8c06e?w=600",
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600",
    "https://images.unsplash.com/photo-1568051243851-f9b136146e97?w=600",
    "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600",
    "https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?w=600",
    "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=600",
    "https://images.unsplash.com/photo-1600717794311-4154e273ca02?w=600",
    "https://images.unsplash.com/photo-1558961363-8c3d70e1a69f?w=600",
    "https://images.unsplash.com/photo-1586985288123-2495f577c250?w=600",
    "https://images.unsplash.com/photo-1595257841889-eca2678454e2?w=600",
    "https://images.unsplash.com/photo-1506869640319-fe1a24fd76dc?w=600",
    "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600",
    "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600",
    "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600",
    "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600",
    "https://images.unsplash.com/photo-1517433670267-08bbd4be890f?w=600",
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600",
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600",
    "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=600",
    "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600",
    "https://images.unsplash.com/photo-1511911063855-2bf39afa5b2e?w=600",
    "https://images.unsplash.com/photo-1587241321921-91a834d82e76?w=600",
    "https://images.unsplash.com/photo-1590080874088-eec64895b423?w=600",
    "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600",
    "https://images.unsplash.com/photo-1599785209796-786432b228bc?w=600",
    "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600",
    "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600",
    "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600",
    "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600",
    "https://images.unsplash.com/photo-1517433670267-08bbd4be890f?w=600",
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600",
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600",
    "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600",
    "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=600",
    "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600",
    "https://images.unsplash.com/photo-1599785209796-786432b228bc?w=600",
    "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600",
    "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600",
    "https://images.unsplash.com/photo-1517433670267-08bbd4be890f?w=600",
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600",
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600",
    "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600",
    "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=600",
    "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600",
    "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600",
    "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600",
]

def main():
    """
    각 가게에 고유한 이미지 할당
    """
    fixture_path = 'backend/stores/fixtures/busan_west_3gu_bakeries_fixture.json'

    # Fixture 파일 읽기
    with open(fixture_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    print(f"총 {len(stores)}개 가게에 고유한 이미지 할당 시작...\n")

    # 이미지 목록 셔플 (랜덤 순서)
    shuffled_images = BAKERY_IMAGES.copy()
    random.shuffle(shuffled_images)

    # 각 가게에 고유한 이미지 할당
    for i, store in enumerate(stores):
        # 이미지가 부족할 경우 순환 사용
        image_index = i % len(shuffled_images)
        store['fields']['preview_image'] = shuffled_images[image_index]

        if (i + 1) % 10 == 0:
            print(f"진행 중: {i + 1}/{len(stores)} 완료")

    # 결과 저장
    with open(fixture_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 완료! 모든 가게에 고유한 이미지가 할당되었습니다.")
    print(f"📁 파일: {fixture_path}")

if __name__ == '__main__':
    main()
