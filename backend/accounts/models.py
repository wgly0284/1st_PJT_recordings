from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
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

    profile_image_url = models.URLField(blank=True)
    
    # 빵 취향 저장을 위한 필드
    bread_preferences = models.CharField(max_length=255, blank=True)

    # '팔로우' 관계
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    # 주요 식별자를 email로 설정
    USERNAME_FIELD = 'email'
    # createsuperuser 시 필수 입력 필드 (email, password는 기본 포함)
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email