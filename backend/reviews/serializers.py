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
            'created_at',
            'like_users',
        )
        # user 필드는 API를 통해 직접 입력받지 않고, 요청을 보낸 사용자로 자동 설정할 것이므로 읽기 전용으로
        read_only_fields = ('user', 'like_users')
