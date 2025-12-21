from django.db import models
from django.conf import settings

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    # ERD에 명시된 위도, 경도 자릿수에 맞게 수정
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    category = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    business_hours = models.CharField(max_length=100, blank=True)
    representative_tags = models.CharField(max_length=200, blank=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    bookmarking_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_stores')

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