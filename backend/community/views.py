from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializer

class CommunityPostListView(generics.ListAPIView):
    """
    커뮤니티 게시글 목록을 조회합니다.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommunityPostCreateView(generics.CreateAPIView):
    """
    새로운 커뮤니티 게시글을 생성합니다.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 로그인한 사용자만 작성 가능

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()

        # 이미지 파일 처리
        image_file = request.FILES.get('image')
        if image_file:
            filename = default_storage.save(f'community_photos/{image_file.name}', image_file)
            image_url = default_storage.url(filename)
            mutable_data['photo_url'] = image_url

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 현재 로그인한 사용자를 작성자로 자동 할당
        serializer.save(author=self.request.user)