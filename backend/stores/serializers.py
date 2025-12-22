from rest_framework import serializers
from .models import Store, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # 1. fields를 '__all__'에서 필요한 필드만 선택하도록 변경할 수 있지만, 
        # 여기서는 프론트엔드에서 image_url을 안 쓰면 되므로 유지해도 무방합니다.
        # 다만, 질문의 취지가 '대표 메뉴란(시리얼라이저 결과)'에서 사진 정보를 뺄 수도 있다는 것이라면
        # 아래와 같이 수정 가능합니다.
        fields = ['id', 'name', 'price', 'category'] # image_url 제외

class StoreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'address',
            'latitude',
            'longitude',
            'business_hours',
            'representative_tags',
            'avg_rating',
            'products',
            'is_bookmarked',
        )

    def get_is_bookmarked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.bookmarking_users.filter(pk=user.pk).exists()
        return False

# ✅ [수정] StoreListSerializer에도 products 추가
class StoreListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True) # 여기 추가!
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'address',
            'latitude', # 지도에 마커 찍으려면 좌표도 필요할 수 있음
            'longitude',
            'avg_rating',
            'products', # 필드 목록에도 추가!
            'is_bookmarked',
            'representative_tags', # 태그 정보도 리스트에서 쓰면 좋음
        )
    
    def get_is_bookmarked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.bookmarking_users.filter(pk=user.pk).exists()
        return False

class MapStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'address',
            'latitude',
            'longitude',
            'avg_rating',
        )