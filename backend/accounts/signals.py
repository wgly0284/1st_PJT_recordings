from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Badge

# User 모델 가져오기
User = get_user_model()

# ⚠️ [주의] Review 모델은 실제 위치에서 import 해야 합니다.
# 예: from reviews.models import Review 
# 여기서는 코드가 깨지지 않도록 주석 처리하거나 가상의 모델로 가정합니다.

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    유저가 처음 생성(회원가입)될 때 실행되는 로직
    """
    if created:
        # 예: 가입 환영 뱃지 지급
        welcome_badge, _ = Badge.objects.get_or_create(
            name='신입 빵쥐',
            defaults={'description': '빵터 가입을 환영합니다!', 'category': 'EVENT'}
        )
        # add()는 M2M 관계에서 바로 저장됨
        instance.badges.add(welcome_badge)

# @receiver(post_save, sender=Review)  <-- 실제 Review 모델을 import 후 주석 해제
def award_exp_on_review(sender, instance, created, **kwargs):
    """
    리뷰가 작성될 때마다 경험치를 지급하는 로직
    """
    if created:
        user = instance.user
        
        # 1. 경험치 20 지급 (레벨업 체크 포함)
        user.gain_exp(20)
        
        # 2. 활동 뱃지 체크 (예: 리뷰 10개)
        # review_count = Review.objects.filter(user=user).count()
        # if review_count == 10:
        #     badge = Badge.objects.get(name='크루아상 헌터')
        #     user.badges.add(badge)