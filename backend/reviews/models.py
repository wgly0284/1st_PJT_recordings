from django.db import models
from django.conf import settings

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 앱 간의 순환 참조를 방지하기 위해 'stores.Store' 문자열로 참조
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField() # 1~5점과 같은 정수형 평점
    photo_urls = models.TextField(blank=True) # 여러 이미지 URL 저장
    tags = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # '리뷰 좋아요' 관계
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_reviews', blank=True)

    class Meta:
        # 한 사용자는 가게 하나당 하나의 리뷰만 작성 가능
        unique_together = ('user', 'store')
        # 최신순으로 정렬
        ordering = ['-created_at']

    def __str__(self):
        return f'Review by {self.user.username} for {self.store.name}'