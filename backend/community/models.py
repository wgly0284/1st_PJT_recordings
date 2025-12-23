from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)

    # 이미지 (선택 사항)
    photo_url = models.URLField(max_length=500, blank=True, null=True)

    # 생성 및 수정 시간
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # '좋아요' 기능
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.category}] {self.title} by {self.author.username}'


class PostComment(models.Model):
    """
    커뮤니티 게시글에 대한 댓글 모델
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 답글 기능을 위한 자기 참조
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        if self.parent:
            return f'Reply by {self.user.nickname} to comment {self.parent.id}'
        return f'Comment by {self.user.nickname} on post {self.post.id}'