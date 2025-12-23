from django.db import models
from django.conf import settings


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 앱 간의 순환 참조를 방지하기 위해 'stores.Store' 문자열로 참조
    # ❗ 이제 선택 필드 (빵집 추천 아닐 때는 null 허용)
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
    )
    content = models.TextField()
    rating = models.IntegerField()  # 1~5점과 같은 정수형 평점
    photo_urls = models.TextField(blank=True)  # 여러 이미지 URL 저장

    # 기존 일반 태그 (예: #데이트 #분위기좋은)
    tags = models.CharField(max_length=200, blank=True)

    # ✅ [추가] 빵 맛/식감 태그 (Idea 3: 취향 분석용)
    # 예: "달달함,바삭함,촉촉함" (콤마로 구분하여 저장)
    taste_tags = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # '리뷰 좋아요' 관계
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_reviews',
        blank=True,
    )

    class Meta:
        # ✅ 중복 리뷰 작성 허용 (unique_together 제거)
        # 최신순으로 정렬
        ordering = ['-created_at']

    def __str__(self):
        if self.store:
            return f'Review by {self.user.username} for {self.store.name}'
        return f'Review by {self.user.username}'


class Comment(models.Model):
    """
    리뷰에 대한 댓글 모델
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
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
            return f'Reply by {self.user.username} to comment {self.parent.id}'
        return f'Comment by {self.user.username} on review {self.review.id}'
