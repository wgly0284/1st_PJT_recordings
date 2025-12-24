from rest_framework import serializers
from .models import Review, Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    댓글 시리얼라이저 (답글 포함)
    """
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'review',
            'user',
            'user_nickname',
            'content',
            'created_at',
            'parent',
            'replies',
        )
        read_only_fields = ('user', 'review', 'parent')

    def get_replies(self, obj):
        """
        해당 댓글의 답글 목록 반환
        """
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class ReviewSerializer(serializers.ModelSerializer):
    # user 필드를 직접 보여주는 대신, user의 nickname을 보여주는 읽기 전용 필드 추가
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comments_count = serializers.SerializerMethodField()

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
            'menu_items',
            'created_at',
            'like_users',
            'comments_count',
        )
        # user 필드는 API를 통해 직접 입력받지 않고, 요청을 보낸 사용자로 자동 설정
        read_only_fields = ('user', 'like_users')
        # store는 선택적으로 허용 (빵집 추천 아니면 없어도 됨)
        extra_kwargs = {
            'store': {'required': False, 'allow_null': True},
        }

    def get_comments_count(self, obj):
        """
        댓글 수 반환 (답글 제외, parent가 None인 댓글만 카운트)
        """
        return obj.comments.filter(parent__isnull=True).count()

    def create(self, validated_data):
        # 요청한 user를 자동으로 세팅
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            validated_data['user'] = user
        return super().create(validated_data)
