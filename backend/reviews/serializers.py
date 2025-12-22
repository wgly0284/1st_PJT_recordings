from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    # user 필드를 직접 보여주는 대신, user의 nickname을 보여주는 읽기 전용 필드 추가
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'user',
            'user_nickname',
            'store',
            'content',
            'rating',
            'photo_urls',
            'tags',
            'taste_tags',
            'created_at',
            'like_users',
        )
        # user 필드는 API를 통해 직접 입력받지 않고, 요청을 보낸 사용자로 자동 설정
        read_only_fields = ('user', 'like_users')
        # store는 선택적으로 허용 (빵집 추천 아니면 없어도 됨)
        extra_kwargs = {
            'store': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        # 요청한 user를 자동으로 세팅
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            validated_data['user'] = user
        return super().create(validated_data)
