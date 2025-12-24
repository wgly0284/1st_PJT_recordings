from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Badge

# ⚠️ [필수] 실제 프로젝트의 앱 이름에 맞춰서 import 경로를 수정해주세요.
# 예: posts 앱의 Post 모델, reviews 앱의 Review 모델
from reviews.models import Review
from community.models import Post 

User = get_user_model()
# 1. 🐣 회원가입 시 신입 뱃지 지급
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        welcome_badge, _ = Badge.objects.get_or_create(
            name='신입 빵쥐',
            defaults={
                'image_url': '', # 필요한 경우 이미지 경로 추가
                'description': '빵터 가입을 환영합니다!', 
                'category': 'EVENT'
            }
        )
        instance.badges.add(welcome_badge)

# 2. 📝 리뷰 작성 시 (50 EXP + 첫 리뷰 뱃지)
if Review:
    @receiver(post_save, sender=Review)
    def award_exp_on_review(sender, instance, created, **kwargs):
        if created:
            user = instance.user  # Review 모델은 보통 user 필드 사용 (확인 필요)
            
            # [최적화] User 모델의 메서드 직접 호출
            if hasattr(user, 'gain_exp'):
                user.gain_exp(50)
            
            # 첫 리뷰 뱃지 지급
            user_review_count = Review.objects.filter(user=user).count()
            if user_review_count == 1:
                first_badge, _ = Badge.objects.get_or_create(
                    name='첫 리뷰',
                    defaults={
                        'description': '설레는 첫 리뷰 작성',
                        'category': 'ACTION',
                        'condition_threshold': 1
                    }
                )
                if not user.badges.filter(id=first_badge.id).exists():
                    user.badges.add(first_badge)

# 3. 💬 게시글 작성 시 (30 EXP)
if Post:
    @receiver(post_save, sender=Post)
    def award_exp_on_post(sender, instance, created, **kwargs):
        """
        커뮤니티 글 작성 시 경험치 지급
        """
        if created:
            # 🚨 [중요] Post 모델은 'author' 필드를 사용합니다.
            user = instance.author  
            
            # [최적화] User 모델의 메서드 직접 호출
            if hasattr(user, 'gain_exp'):
                user.gain_exp(30)