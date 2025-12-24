#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
사용자 취향 기반 추천 테스트 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User
from stores.models import Store, Keyword, Product

print("=" * 50)
print("데이터베이스 확인")
print("=" * 50)

# 1. 키워드 확인
print("\n[1] 사용 가능한 키워드 (처음 10개):")
keywords = list(Keyword.objects.all()[:10])
for idx, kw in enumerate(keywords, 1):
    print(f"  {idx}. {kw.name}")

# 2. 제품과 키워드 매칭 확인
print("\n[2] 제품-키워드 매칭 샘플 (처음 5개):")
products = Product.objects.prefetch_related('keywords').all()[:5]
for p in products:
    kw_list = list(p.keywords.values_list('name', flat=True))
    print(f"  - {p.name} (가게: {p.store.name}): {kw_list}")

# 3. 테스트 사용자 생성 또는 업데이트
print("\n[3] 테스트 사용자 설정:")
test_email = "testuser@example.com"

# 처음 3개 키워드를 사용자 취향으로 설정
if keywords:
    user_prefs = ','.join([kw.name for kw in keywords[:3]])
else:
    user_prefs = "소금빵,크루아상,식빵"

user, created = User.objects.get_or_create(
    email=test_email,
    defaults={
        'nickname': 'test_user',
        'bread_preferences': user_prefs
    }
)

if not created:
    user.bread_preferences = user_prefs
    user.save()

print(f"  - 이메일: {user.email}")
print(f"  - 닉네임: {user.nickname}")
print(f"  - 취향 키워드: {user.bread_preferences}")
print(f"  - 사용자 {'생성됨' if created else '업데이트됨'}")

# 4. 추천 로직 시뮬레이션
print("\n[4] 추천 로직 시뮬레이션:")
bread_prefs = user.bread_preferences.strip()
if bread_prefs:
    keyword_names = [kw.strip() for kw in bread_prefs.split(',') if kw.strip()]
    print(f"  - 파싱된 키워드: {keyword_names}")

    matching_products = Product.objects.filter(keywords__name__in=keyword_names).distinct()
    print(f"  - 매칭된 제품 수: {matching_products.count()}")

    if matching_products.exists():
        store_ids = matching_products.values_list('store_id', flat=True).distinct()
        stores = Store.objects.filter(id__in=store_ids)
        print(f"  - 매칭된 빵집 수: {stores.count()}")

        if stores.exists():
            recommended_store = stores.order_by('?').first()
            print(f"  - 추천 빵집: {recommended_store.name} (ID: {recommended_store.id})")

            # 매칭된 키워드 확인
            matched_keywords = list(set(
                matching_products.filter(store=recommended_store)
                .values_list('keywords__name', flat=True)
            ) & set(keyword_names))
            print(f"  - 매칭된 키워드: {matched_keywords}")
        else:
            print("  - 매칭된 빵집이 없습니다.")
    else:
        print("  - 매칭된 제품이 없습니다. 랜덤 추천을 진행합니다.")
else:
    print("  - 사용자 취향 키워드가 없습니다.")

print("\n" + "=" * 50)
print("테스트 완료!")
print("=" * 50)
