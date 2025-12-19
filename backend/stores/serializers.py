from rest_framework import serializers
from .models import Store, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

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

class StoreListSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'address',
            'avg_rating',
            'is_bookmarked',
        )
    
    def get_is_bookmarked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.bookmarking_users.filter(pk=user.pk).exists()
        return False
