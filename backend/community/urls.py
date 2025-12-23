from django.urls import path
from . import views

urlpatterns = [
    # 게시글 목록 및 생성
    path('', views.CommunityPostListView.as_view(), name='post_list'),
    path('create/', views.CommunityPostCreateView.as_view(), name='post_create'),

    # 내가 작성한 게시글 목록
    path('my/', views.my_posts, name='my_posts'),

    # 게시글 삭제
    path('<int:post_id>/', views.post_delete, name='post_delete'),

    # 게시글 좋아요
    path('<int:post_id>/like/', views.post_like, name='post_like'),

    # 게시글 댓글
    path('<int:post_id>/comments/', views.post_comments, name='post_comments'),
    path('<int:post_id>/comments/create/', views.post_comment_create, name='post_comment_create'),

    # 댓글/답글 삭제
    path('comments/<int:comment_id>/', views.comment_delete, name='comment_delete'),

    # 댓글 답글
    path('comments/<int:comment_id>/reply/', views.post_comment_reply, name='post_comment_reply'),
]
