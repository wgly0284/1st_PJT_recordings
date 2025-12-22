from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings # allauth 설정 가져오기
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()


# dj-rest-auth의 기본 회원가입 시리얼라이저를 상속받아 커스텀 필드 처리 로직 추가
class CustomRegisterSerializer(RegisterSerializer):
    # username 필드를 명시적으로 오버라이드하여 필수가 아니도록 설정
    username = serializers.CharField(
        # User 모델의 username 필드에서 max_length 값을 직접 가져옴
        max_length=User._meta.get_field('username').max_length,
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=False,
        allow_blank=True
    )
    nickname = serializers.CharField(max_length=50)
    bread_preferences = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['bread_preferences'] = self.validated_data.get('bread_preferences', '')
        
        # username이 제공되지 않았다면 None으로 설정하여 allauth가 자동으로 생성하도록 유도
        if not self.validated_data.get('username'):
            data['username'] = None
        
        return data

    def save(self, request):
        # Call the parent save method to handle user creation and standard fields
        user = super().save(request)
        
        # Add the custom data
        user.nickname = self.validated_data.get('nickname', '')
        user.bread_preferences = self.validated_data.get('bread_preferences', '')
        user.save()
        
        return user

# 사용자 정보 조회/수정을 위한 시리얼라이저
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # API를 통해 보여주고 수정할 필드 목록
        fields = (
            'pk',
            'email',
            'nickname',
            'profile_image_url',
            'bread_preferences',
            # [추가] 캐릭터 성장 관련 필드
            'level',
            'exp',
            'character_type',
        )
        # API를 통해 직접 수정할 수 없는 읽기 전용 필드
        # 레벨과 경험치는 서버 로직에 의해서만 변경되어야 하므로 read_only에 추가
        read_only_fields = ('pk', 'email', 'level', 'exp', 'character_type')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'nickname', 'profile_image_url', 
            'bread_preferences', 'follows', 'followers',
            # [추가] 캐릭터 성장 관련 필드
            'level', 'exp', 'character_type'
        ]