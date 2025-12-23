from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .models import Post, PostComment
from .serializers import PostSerializer, PostCommentSerializer


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
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 작성 가능

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_like(request, post_id):
    """
    게시글 좋아요/좋아요 취소
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        return Response({'status': 'like removed'}, status=status.HTTP_200_OK)
    else:
        post.like_users.add(request.user)
        return Response({'status': 'like added'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def post_comments(request, post_id):
    """
    특정 게시글의 댓글 목록 조회
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # parent가 None인 최상위 댓글만 가져옴 (답글은 serializer에서 처리)
    comments = PostComment.objects.filter(post=post, parent__isnull=True)
    serializer = PostCommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_comment_create(request, post_id):
    """
    게시글에 댓글 작성
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_comment_reply(request, comment_id):
    """
    댓글에 답글 작성
    """
    try:
        parent_comment = PostComment.objects.get(id=comment_id)
    except PostComment.DoesNotExist:
        return Response({'error': '댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, post=parent_comment.post, parent=parent_comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, post_id):
    """
    게시글 삭제 (작성자만 가능)
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 작성자 확인
    if post.author != request.user:
        return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    post.delete()
    return Response({'message': '게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id):
    """
    댓글/답글 삭제 (작성자만 가능)
    """
    try:
        comment = PostComment.objects.get(id=comment_id)
    except PostComment.DoesNotExist:
        return Response({'error': '댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 작성자 확인
    if comment.user != request.user:
        return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_posts(request):
    """
    현재 로그인한 사용자가 작성한 게시글 목록
    """
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)