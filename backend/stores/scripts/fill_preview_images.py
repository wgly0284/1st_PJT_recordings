# backend/stores/scripts/fill_preview_images.py

from stores.models import Store

# 🥐 빵/쿠키/케이크 전용 이미지 목록 (모두 Unsplash 고정 URL)
BAKERY_IMAGES = [
    # 빵 진열대
    "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&h=533&fit=crop",

    # 식빵/바게트
    "https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&h=533&fit=crop",

    # 케이크 / 디저트 접시
    "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&h=533&fit=crop",

    # 반죽/베이킹 장면
    "https://images.unsplash.com/photo-1603048297194-8f7e4d68b82a?w=800&h=533&fit=crop",

    # 롤/파운드케이크 진열
    "https://images.unsplash.com/photo-1603048297172-c92544798d5a?w=800&h=533&fit=crop",

    # 크루아상 + 커피
    "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=800&h=533&fit=crop",

    # 쿠키 / 브라우니
    "https://images.unsplash.com/photo-1614707267537-4545f1c2b4b5?w=800&h=533&fit=crop",

    # 도넛/머핀 진열
    "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&h=533&fit=crop",
]


def choose_bakery_image(name: str) -> str:
    """
    가게 이름을 기준으로 항상 같은 이미지가 선택되도록 해시 사용.
    """
    idx = hash(name) % len(BAKERY_IMAGES)
    return BAKERY_IMAGES[idx]


def main():
    """
    모든 Store 객체의 preview_image 필드를
    베이커리 전용 이미지로 채워 넣는 함수.
    manage.py shell 안에서 호출해서 사용.
    """
    qs = Store.objects.all()
    updated = 0

    for store in qs:
        store.preview_image = choose_bakery_image(store.name)
        store.save(update_fields=["preview_image"])
        updated += 1

    print(f"미리보기 이미지 채운 가게 수: {updated}")
