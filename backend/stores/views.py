from rest_framework import generics, status, filters  # ✅ filters 추가
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Store
from .serializers import StoreListSerializer, StoreSerializer, MapStoreSerializer

# 지도용 API (가볍게 전체 마커용으로 사용한다면 유지, 아니면 StoreListView 하나로 통합 가능)
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
    
    # ✅ [추가] 검색 필터 설정
    filter_backends = [filters.SearchFilter]
    
    # ✅ [추가] 검색할 모델 필드 지정
    # name: 가게 이름
    # address: 주소
    # category: 카테고리
    # representative_tags: 태그 (만약 모델에 있다면)
    search_fields = ['name', 'address', 'category', 'representative_tags']

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