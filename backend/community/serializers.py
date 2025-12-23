from rest_framework import serializers
from .models import Post, PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    """
    커뮤니티 게시글 댓글 시리얼라이저 (답글 포함)
    """
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = (
            'id',
            'post',
            'user',
            'user_nickname',
            'content',
            'created_at',
            'parent',
            'replies',
        )
        read_only_fields = ('user', 'post', 'parent')

    def get_replies(self, obj):
        """
        해당 댓글의 답글 목록 반환
        """
        if obj.replies.exists():
            return PostCommentSerializer(obj.replies.all(), many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    comments_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_nickname',
            'title',
            'content',
            'category',
            'photo_url',
            'created_at',
            'updated_at',
            'like_users',
            'comments_count',
            'like_count',
        ]
        read_only_fields = ['author', 'like_users']

    def get_comments_count(self, obj):
        """
        댓글 수 반환 (답글 제외, parent가 None인 댓글만 카운트)
        """
        return obj.comments.filter(parent__isnull=True).count()

    def get_like_count(self, obj):
        """
        좋아요 수 반환
        """
        return obj.like_users.count()
