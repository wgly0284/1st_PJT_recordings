from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings
from django.contrib.auth import get_user_model
from .models import Badge

User = get_user_model()

# -------------------------------------------------------------------------
# 1. 뱃지 시리얼라이저
# -------------------------------------------------------------------------
class BadgeSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'category', 'image_url', 'icon']

    def get_icon(self, obj):
        return "🏅"

# -------------------------------------------------------------------------
# 2. 회원가입 시리얼라이저
# -------------------------------------------------------------------------
class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(
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
        
        if not self.validated_data.get('username'):
            data['username'] = None
        
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname', '')
        user.bread_preferences = self.validated_data.get('bread_preferences', '')
        user.save()
        return user

# -------------------------------------------------------------------------
# 3. 유저 정보 수정용 시리얼라이저 (내 정보 수정)
# -------------------------------------------------------------------------
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'nickname',
            'profile_image_url',
            'bread_preferences',
            'level',
            'exp',
            'level_title',
        )
        read_only_fields = ('pk', 'email', 'level', 'exp', 'level_title')

# -------------------------------------------------------------------------
# 4. 상세 프로필 시리얼라이저 (마이페이지 조회용)
# -------------------------------------------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    badges = BadgeSerializer(many=True, read_only=True)
    next_exp = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    visited_stores = serializers.SerializerMethodField()
    taste_stats = serializers.SerializerMethodField()
    bookmarked_stores = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'nickname', 'profile_image_url',
            'level', 'exp', 'level_title', 'next_exp',
            'badges', 'review_count', 'post_count',
            'visited_stores', 'bookmarked_stores', 'taste_stats',
            'follower_count', 'following_count',
            'date_joined'
        ]
        read_only_fields = ['email', 'level', 'exp', 'level_title', 'date_joined']

    def get_next_exp(self, obj):
        from .models import User
        return User.LEVEL_SYSTEM.get(obj.level, {}).get('next_exp', 100)

    def get_review_count(self, obj):
        return getattr(obj, 'reviews', []).count() if hasattr(obj, 'reviews') else 0

    def get_post_count(self, obj):
        return getattr(obj, 'posts', []).count() if hasattr(obj, 'posts') else 0

    def get_visited_stores(self, obj):
        return []

    def get_bookmarked_stores(self, obj):
        from stores.serializers import StoreListSerializer
        stores = obj.bookmarked_stores.all()
        return StoreListSerializer(stores, many=True, context=self.context).data

    def get_taste_stats(self, obj):
        return {"크림빵": 5, "하드계열": 3}
    
    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.follows.count()

# -------------------------------------------------------------------------
# 5. 기본 유저 시리얼라이저 (views.py에서 참조 중인 것) - [복구 완료]
# -------------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'nickname', 'profile_image_url', 
            'bread_preferences', 'follows', 'followers',
            'level', 'exp', 'level_title' # character_type 대신 level_title 사용
        ]