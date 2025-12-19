from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Store
from .serializers import StoreListSerializer, StoreSerializer

class StoreListView(generics.ListAPIView):
    """
    가게 목록을 조회합니다.
    """
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer

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
