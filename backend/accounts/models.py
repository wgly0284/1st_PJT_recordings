from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    # 1. 기존 필드 유지
    # 이메일 기반 인증을 위해 기존 username 필드는 고유하지 않게 설정
    username = models.CharField(
        max_length=150,
        unique=False,
        blank=True,
        null=True,
    )
    # nickname은 API 레벨에서 필수 입력으로 처리하되, DB에는 null을 허용하여 마이그레이션 문제 방지
    nickname = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    # email을 주요 식별자로 사용하고, 고유하게 설정
    email = models.EmailField(unique=True)

    profile_image_url = models.CharField(max_length=500, blank=True)
    
    # 빵 취향 저장을 위한 필드
    bread_preferences = models.CharField(max_length=255, blank=True)

    # '팔로우' 관계
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    # 2. [추가] 캐릭터 성장 시스템 (Gamification) 🐣
    level = models.IntegerField(default=1) # 레벨
    exp = models.IntegerField(default=0)   # 경험치
    # 캐릭터 타입: (예: hamster, bear, lion) - 기본값은 햄스터
    character_type = models.CharField(max_length=20, default='hamster')

    # 주요 식별자를 email로 설정
    USERNAME_FIELD = 'email'
    # createsuperuser 시 필수 입력 필드 (email, password는 기본 포함)
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

    # 3. [추가] 레벨업 로직 메서드
    def check_level_up(self):
        """
        경험치를 확인하고 레벨업 조건을 충족하면 레벨과 캐릭터를 변경합니다.
        (예: 레벨 * 100 경험치 도달 시 레벨업)
        """
        needed_exp = self.level * 100
        if self.exp >= needed_exp:
            self.level += 1
            self.exp -= needed_exp # 누적 경험치가 아니라 레벨업 시 차감 방식 (선택 사항)
            
            # 레벨에 따른 캐릭터 진화 (예시)
            if self.level >= 10: self.character_type = 'bear'
            if self.level >= 20: self.character_type = 'lion'
            
            self.save()
            return True # 레벨업 성공!
        return False