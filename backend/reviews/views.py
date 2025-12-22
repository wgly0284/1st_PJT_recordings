from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    특정 가게의 리뷰 목록을 조회하거나 새 리뷰를 작성합니다.
    /stores/<store_pk>/reviews/ 같은 패턴에서 사용한다고 가정.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # URL에서 store_pk를 받아 해당 가게의 리뷰만 필터링
        store_pk = self.kwargs.get('store_pk')
        return Review.objects.filter(store_id=store_pk)

    def perform_create(self, serializer):
        # 리뷰를 작성할 때, 요청을 보낸 사용자를 user 필드에 자동으로 할당
        store_pk = self.kwargs.get('store_pk')
        serializer.save(user=self.request.user, store_id=store_pk)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    단일 리뷰를 조회, 수정, 삭제합니다.
    /reviews/<pk>/ 에 매핑.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # TODO: 작성자만 수정/삭제하도록 권한 설정 필요


class ReviewLikeView(APIView):
    """
    리뷰에 '좋아요'를 추가하거나 제거합니다.
    /reviews/<review_pk>/like/ 에 매핑.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, review_pk):
        try:
            review = Review.objects.get(pk=review_pk)
        except Review.DoesNotExist:
            return Response({"error": "Review not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            return Response({"status": "like removed"}, status=status.HTTP_200_OK)
        else:
            review.like_users.add(user)
            return Response({"status": "like added"}, status=status.HTTP_200_OK)


class UserReviewListView(generics.ListAPIView):
    """
    현재 로그인한 사용자가 작성한 리뷰 목록을 조회합니다.
    /reviews/my/ 에 매핑.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewCreateView(generics.CreateAPIView):
    """
    새 리뷰를 생성하는 전용 엔드포인트.
    /reviews/create/ 에 매핑.
    프론트의 NewReview.vue 에서 사용.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 필요에 따라 store_id 등 추가 필드를 함께 저장
        serializer.save(user=self.request.user)
