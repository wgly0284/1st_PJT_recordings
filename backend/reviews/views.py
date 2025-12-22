from django.core.files.storage import default_storage
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


class ReviewListView(generics.ListAPIView):
    """
    전체 리뷰 목록을 조회합니다.
    /reviews/ 에 매핑.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()

        # 1. 이미지 처리
        image_file = request.FILES.get('image')
        if image_file:
            filename = default_storage.save(f'review_photos/{image_file.name}', image_file)
            image_url = default_storage.url(filename)
            mutable_data['photo_urls'] = image_url

        # 2. 제목(title)과 내용(content) 합치기
        title = mutable_data.get('title')
        content = mutable_data.get('content', '')
        if title:
            # 마크다운 형식으로 제목을 내용 상단에 추가
            mutable_data['content'] = f"**{title}**\n\n{content}"

        # 3. CreateAPIView의 기본 create 로직 다시 호출
        serializer = self.get_serializer(data=mutable_data)
        if not serializer.is_valid():
            # 디버깅용: 서버 로그에 에러 출력
            print('ReviewCreateView errors:', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 리뷰를 작성할 때, 요청을 보낸 사용자를 user 필드에 자동으로 할당
        serializer.save(user=self.request.user)
