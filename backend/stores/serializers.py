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
            "preview_image", 
        )

    def get_is_bookmarked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.bookmarking_users.filter(pk=user.pk).exists()
        return False

# ✅ [수정] StoreListSerializer에도 products 추가
class StoreListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    is_bookmarked = serializers.SerializerMethodField()
    product_keywords = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'address',
            'latitude',
            'longitude',
            'avg_rating',
            'products',
            'is_bookmarked',
            'representative_tags',
            'product_keywords',
            'image',
        )
    
    def get_is_bookmarked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.bookmarking_users.filter(pk=user.pk).exists()
        return False

    def get_product_keywords(self, obj):
        # 모든 제품의 모든 키워드를 하나로 합칩니다.
        keywords = set()
        for product in obj.products.all():
            for keyword in product.keywords.all():
                keywords.add(keyword.name)
        # 앞에서 3개만 잘라서 반환
        return list(keywords)[:3]

    def get_image(self, obj):
        # preview_image를 대표 이미지로 사용
        return obj.preview_image if obj.preview_image else None

class MapStoreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'address',
            'latitude',
            'longitude',
            'avg_rating',
            'preview_image',
            'products',
            'representative_tags',
            'business_hours',
            'contact',
        )
