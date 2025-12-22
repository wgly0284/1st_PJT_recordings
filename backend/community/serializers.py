from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)

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
            'like_users'
        ]
        read_only_fields = ['author', 'like_users']
