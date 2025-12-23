from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404

# 모델 임포트
from .models import Store
from reviews.models import Review  # Review 모델 명시적 임포트 (확실한 쿼리를 위해)

# 시리얼라이저 임포트
from .serializers import StoreListSerializer, StoreSerializer, MapStoreSerializer

# ✅ [수정] AI 요약 서비스 함수 임포트 (utils가 아닌 store_summary_service에서 가져옵니다)
from .utils import generate_store_summary

# 지도용 API
class MapStoreListView(generics.ListAPIView):
    """
    지도에 표시할 가게 목록을 조회합니다.
    """
    queryset = Store.objects.all()
    serializer_class = MapStoreSerializer

class StoreListView(generics.ListAPIView):
    """
    가게 목록을 조회하고 검색합니다.
    (?search=키워드 로 검색 가능)
    """
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    
    # 검색 필터 설정
    filter_backends = [filters.SearchFilter]
    
    # 검색할 모델 필드 지정
    search_fields = ['name', 'address', 'category', 'representative_tags', 'products__name', 'products__keywords__name']

class StoreDetailView(generics.RetrieveAPIView):
    """
    가게의 상세 정보를 조회합니다.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

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
            # 이미 북마크했다면 제거
            store.bookmarking_users.remove(user)
            return Response({"status": "bookmark removed"}, status=status.HTTP_200_OK)
        else:
            # 북마크하지 않았다면 추가
            store.bookmarking_users.add(user)
            return Response({"status": "bookmark added"}, status=status.HTTP_200_OK)

class UserBookmarkListView(generics.ListAPIView):
    """
    현재 로그인한 사용자가 북마크한 가게 목록을 조회합니다.
    """
    serializer_class = StoreListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.bookmarked_stores.all()
    
class WeeklyPickView(generics.ListAPIView):
    """
    이번 주 추천 가게 4개를 랜덤으로 조회합니다.
    """
    serializer_class = StoreListSerializer

    def get_queryset(self):
        # 랜덤으로 4개의 가게를 가져옵니다.
        return Store.objects.order_by('?').all()[:4]

class StoreAISummaryView(APIView):
    """
    특정 가게(pk)의 리뷰들을 모아 AI 요약을 반환합니다.
    GET /stores/<pk>/ai-summary/
    """
    def get(self, request, pk):
        store = get_object_or_404(Store, pk=pk)
        
        # ✅ [수정] 최신 리뷰 30개만 가져오기 (토큰 제한 및 성능 최적화)
        # Review 모델을 직접 쿼리하여 최신순 정렬 후 슬라이싱
        reviews = Review.objects.filter(store=store).order_by('-created_at')[:30]
        
        # 내용만 리스트로 추출
        reviews_list = [review.content for review in reviews]
        
        # ✅ [호출] 분리해둔 서비스 파일의 함수 실행
        ai_result = generate_store_summary(store.name, reviews_list)
        
        return Response(ai_result, status=status.HTTP_200_OK)