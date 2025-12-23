from django.urls import path
from . import views

urlpatterns = [
    # 전체 리뷰 목록
    path('', views.ReviewListView.as_view(), name='review_list'),

    # 단일 리뷰 조회/수정/삭제
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),

    # 리뷰 좋아요 토글
    path('<int:review_pk>/like/', views.ReviewLikeView.as_view(), name='review_like'),

    # 내 리뷰 목록
    path('my/', views.UserReviewListView.as_view(), name='my_reviews'),

    # 새 리뷰 생성
    path('create/', views.ReviewCreateView.as_view(), name='review_create'),

    # 댓글 관련
    path('<int:review_pk>/comments/', views.CommentListCreateView.as_view(), name='comment_list_create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('comments/<int:comment_pk>/reply/', views.ReplyCreateView.as_view(), name='reply_create'),
]