from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

# 모델 임포트
from .models import Store
from reviews.models import Review

# 시리얼라이저 임포트
from .serializers import StoreListSerializer, StoreSerializer, MapStoreSerializer, StoreSearchSerializer

# ✅ utils에서 함수 2개 모두 임포트
from .utils import generate_store_summary, generate_chat_response

# 1. 지도용 API
class MapStoreListView(generics.ListAPIView):
    """
    지도에 표시할 가게 목록을 조회합니다.
    """
    queryset = Store.objects.all()
    serializer_class = MapStoreSerializer

# 2. 가게 목록 및 검색 API
class StoreListView(generics.ListAPIView):
    """
    가게 목록을 조회하고 검색합니다. (?search=키워드)
    """
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address', 'category', 'representative_tags', 'products__name', 'products__keywords__name']

# 2-1. ✅ [추가] 초고속 빵집 검색 API (이름, 주소만)
class StoreQuickSearchView(generics.ListAPIView):
    """
    빵집 이름/주소만 빠르게 검색합니다. (?search=키워드)
    커뮤니티 빵집 추천 글 작성용
    """
    serializer_class = StoreSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']  # 이름과 주소만 검색

    def get_queryset(self):
        # only()로 필요한 필드만 select
        return Store.objects.only('id', 'name', 'address')

# 3. 가게 상세 조회 API
class StoreDetailView(generics.RetrieveAPIView):
    """
    가게의 상세 정보를 조회합니다.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

# 4. 북마크 토글 API
class BookmarkView(APIView):
    """
    가게를 북마크에 추가하거나 제거합니다.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, store_pk):
        try:
            store = Store.objects.get(pk=store_pk)
        except Store.DoesNotExist:
            return Response({"error": "Store not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if store.bookmarking_users.filter(pk=user.pk).exists():
            store.bookmarking_users.remove(user)
            return Response({"status": "bookmark removed"}, status=status.HTTP_200_OK)
        else:
            store.bookmarking_users.add(user)
            return Response({"status": "bookmark added"}, status=status.HTTP_200_OK)

# 5. 내 북마크 목록 API
class UserBookmarkListView(generics.ListAPIView):
    """
    현재 로그인한 사용자가 북마크한 가게 목록을 조회합니다.
    """
    serializer_class = StoreListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.bookmarked_stores.all()

# 6. 이번 주 추천 가게 API
class WeeklyPickView(generics.ListAPIView):
    """
    이번 주 추천 가게 4개를 랜덤으로 조회합니다.
    """
    serializer_class = StoreListSerializer

    def get_queryset(self):
        return Store.objects.order_by('?').all()[:4]

# 7. AI 가게 요약 API
class StoreAISummaryView(APIView):
    """
    특정 가게(pk)의 리뷰들을 모아 AI 요약을 반환합니다.
    """
    def get(self, request, pk):
        store = get_object_or_404(Store, pk=pk)
        # 최신 리뷰 30개만 가져오기
        reviews = Review.objects.filter(store=store).order_by('-created_at')[:30]
        reviews_list = [review.content for review in reviews]

        # utils의 요약 함수 실행
        ai_result = generate_store_summary(store.name, reviews_list)

        return Response(ai_result, status=status.HTTP_200_OK)

# 8. 사용자 맞춤 일일 추천 API
class DailyRecommendationView(APIView):
    """
    사용자의 취향 키워드(bread_preferences)를 기반으로 매일 빵집을 추천합니다.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1) bread_preferences에서 키워드 추출 (쉼표로 구분된 문자열 파싱)
        bread_prefs = user.bread_preferences.strip() if user.bread_preferences else ""

        # 2) 키워드가 없는 경우: 랜덤 추천
        if not bread_prefs:
            recommended_store = Store.objects.order_by('?').first()
            if not recommended_store:
                return Response({"error": "No stores available"}, status=status.HTTP_404_NOT_FOUND)
            serializer = StoreSerializer(recommended_store, context={'request': request})
            return Response({**serializer.data, 'reason': '신규 회원 추천', 'matched_keywords': []})

        # 3) 쉼표로 구분된 키워드들을 리스트로 변환
        keyword_names = [kw.strip() for kw in bread_prefs.split(',') if kw.strip()]

        if not keyword_names:
            recommended_store = Store.objects.order_by('?').first()
            serializer = StoreSerializer(recommended_store, context={'request': request})
            return Response({**serializer.data, 'reason': '새로운 발견', 'matched_keywords': []})

        # 4) 키워드 매칭 로직
        from .models import Product  # Circular import 방지
        matching_products = Product.objects.filter(keywords__name__in=keyword_names).distinct()

        if not matching_products.exists():
            recommended_store = Store.objects.order_by('?').first()
            serializer = StoreSerializer(recommended_store, context={'request': request})
            return Response({**serializer.data, 'reason': '새로운 발견', 'matched_keywords': []})

        # 5) 매칭된 상품이 있는 빵집들 중 랜덤 선택
        store_ids = matching_products.values_list('store_id', flat=True).distinct()
        stores = Store.objects.filter(id__in=store_ids)
        recommended_store = stores.order_by('?').first()

        # 6) 매칭된 키워드 추출
        matched_keywords = list(set(
            matching_products.filter(store=recommended_store)
            .values_list('keywords__name', flat=True)
        ) & set(keyword_names))

        serializer = StoreSerializer(recommended_store, context={'request': request})
        return Response({
            **serializer.data,
            'reason': '취향 저격',
            'matched_keywords': matched_keywords[:3]
        })

# 9. ✅ [신규] 빵집 추천 챗봇 API
class BakeryChatBotView(APIView):
    """
    빵집 추천 챗봇과 대화합니다.
    POST /stores/chatbot/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        messages = request.data.get('messages', [])

        if not messages:
            return Response({"error": "메시지 내역이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # utils의 AI 챗봇 함수 호출
        bot_reply = generate_chat_response(messages)

        return Response({"role": "assistant", "content": bot_reply}, status=status.HTTP_200_OK)

# 10. 시/도 목록 조회 API
class RegionCityListView(APIView):
    """
    가게 주소에서 시/도 목록을 추출하여 반환합니다.
    GET /stores/regions/cities/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # address 필드에서 시/도 추출 (첫 번째 공백 또는 첫 단어)
        addresses = Store.objects.values_list('address', flat=True)
        cities = set()

        for addr in addresses:
            if addr:
                # "서울 강남구 ..."에서 "서울" 추출
                parts = addr.split()
                if parts:
                    city = parts[0]
                    cities.add(city)

        return Response(sorted(list(cities)), status=status.HTTP_200_OK)

# 11. 구 목록 조회 API
class RegionDistrictListView(APIView):
    """
    선택된 시/도에 해당하는 구 목록을 반환합니다.
    GET /stores/regions/districts/?city=서울
    """
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city', '')

        if not city:
            return Response({"error": "city 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        addresses = Store.objects.filter(address__startswith=city).values_list('address', flat=True)
        districts = set()

        for addr in addresses:
            parts = addr.split()
            if len(parts) >= 2:
                district = parts[1]
                districts.add(district)

        return Response(sorted(list(districts)), status=status.HTTP_200_OK)

# 12. 동 목록 조회 API
class RegionNeighborhoodListView(APIView):
    """
    선택된 시/도와 구에 해당하는 동 목록을 반환합니다.
    GET /stores/regions/neighborhoods/?city=서울&district=강남구
    """
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city', '')
        district = request.query_params.get('district', '')

        if not city or not district:
            return Response({"error": "city와 district 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        addresses = Store.objects.filter(
            address__startswith=f"{city} {district}"
        ).values_list('address', flat=True)

        neighborhoods = set()

        for addr in addresses:
            parts = addr.split()
            if len(parts) >= 3:
                neighborhood = parts[2]
                neighborhoods.add(neighborhood)

        return Response(sorted(list(neighborhoods)), status=status.HTTP_200_OK)