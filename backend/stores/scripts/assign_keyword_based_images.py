"""
가게명 키워드 기반으로 적합한 Unsplash 베이커리 이미지를 매핑하는 스크립트
"""

import json
import re

# 키워드별 Unsplash 이미지 매핑
KEYWORD_IMAGE_MAP = {
    # 케이크 관련
    'cake|케이크|치즈케이크|티라미수': [
        "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600",
        "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600",
        "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600",
        "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=600",
        "https://images.unsplash.com/photo-1574085733277-851d9d856a3a?w=600",
    ],

    # 마카롱 관련
    'macaron|마카롱': [
        "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600",
        "https://images.unsplash.com/photo-1558312657-e4e0ff6e5eca?w=600",
        "https://images.unsplash.com/photo-1569864358642-9d1684040f43?w=600",
    ],

    # 쿠키 관련
    'cookie|쿠키': [
        "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600",
        "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600",
        "https://images.unsplash.com/photo-1548365328-8c6db3220e4c?w=600",
    ],

    # 도넛 관련
    'donut|도넛': [
        "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600",
        "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600",
    ],

    # 크루아상/페이스트리
    'croissant|크루아상|페이스트리': [
        "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600",
        "https://images.unsplash.com/photo-1530610476181-d83430b64dcd?w=600",
        "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600",
    ],

    # 빵/베이커리
    'bread|빵|식빵|바게트|호두|통밀': [
        "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600",
        "https://images.unsplash.com/photo-1542838132-92c53300491e?w=600",
        "https://images.unsplash.com/photo-1517433670267-08bbd4be890f?w=600",
        "https://images.unsplash.com/photo-1598373182133-52452f7691ef?w=600",
    ],

    # 파이/타르트
    'pie|tart|파이|타르트': [
        "https://images.unsplash.com/photo-1519915212116-7cfef71f1d3e?w=600",
        "https://images.unsplash.com/photo-1535920527002-b35e96722eb9?w=600",
        "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=600",
    ],

    # 베이커리 진열대
    'bakery|베이커리|제과|빵집': [
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600",
        "https://images.unsplash.com/photo-1603048297194-8f7e4d68b82a?w=600",
        "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=600",
    ],
}

# 기본 이미지 풀 (키워드 매칭 안될 경우)
DEFAULT_IMAGES = [
    "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600",
    "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600",
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600",
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600",
    "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600",
]


def get_image_for_store(store_name, index):
    """
    가게 이름을 분석하여 적합한 이미지 URL을 반환합니다.

    Args:
        store_name: 가게 이름
        index: 가게 인덱스 (중복 방지용)

    Returns:
        적합한 Unsplash 이미지 URL
    """
    store_name_lower = store_name.lower()

    # 키워드 매칭
    for keyword_pattern, images in KEYWORD_IMAGE_MAP.items():
        if re.search(keyword_pattern, store_name_lower):
            # 같은 카테고리 내에서도 다양성을 위해 인덱스 기반 선택
            return images[index % len(images)]

    # 매칭되는 키워드가 없으면 기본 이미지 사용
    return DEFAULT_IMAGES[index % len(DEFAULT_IMAGES)]


def main():
    """
    가게명 키워드에 맞는 이미지를 할당합니다.
    """
    fixture_path = 'stores/fixtures/busan_west_3gu_bakeries_fixture.json'

    # Fixture 파일 읽기
    with open(fixture_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    print(f"총 {len(stores)}개 가게에 키워드 기반 이미지 할당 시작...\n")

    # 각 가게에 키워드 기반 이미지 할당
    updated_count = 0
    for i, store in enumerate(stores):
        name = store['fields']['name']
        old_image = store['fields'].get('preview_image', '')

        # 키워드 기반 이미지 선택
        new_image = get_image_for_store(name, i)
        store['fields']['preview_image'] = new_image

        if old_image != new_image:
            updated_count += 1

        if (i + 1) % 10 == 0:
            print(f"진행 중: {i + 1}/{len(stores)} 완료")

    # 결과 저장
    with open(fixture_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    print(f"\n완료!")
    print(f"총 {len(stores)}개 가게 처리")
    print(f"{updated_count}개 이미지 업데이트")
    print(f"파일: {fixture_path}")


if __name__ == '__main__':
    main()
