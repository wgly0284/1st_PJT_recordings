from django.db import models
from django.conf import settings

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    
    # 좌표는 null 허용 (잘 되어 있음)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # [수정 1] null=True 추가 (데이터가 없어도 에러 안 나게)
    category = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    # [수정 2] auto_now_add=True 추가 (자동 생성)
    # JSON에 값이 있으면 그 값으로, 없으면 현재 시간으로 자동 저장됨
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    business_hours = models.CharField(max_length=100, blank=True, null=True)
    representative_tags = models.CharField(max_length=200, blank=True, null=True)
    
    # 평점 기본값 (잘 되어 있음)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    bookmarking_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_stores', blank=True) # blank=True 추가 권장 (즐겨찾기 없는 경우)

    def __str__(self):
        return self.name

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=50)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name