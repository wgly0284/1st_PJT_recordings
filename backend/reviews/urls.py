from django.urls import path
from . import views

urlpatterns = [
    # 단일 리뷰 조회/수정/삭제
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),

    # 리뷰 좋아요 토글
    path('<int:review_pk>/like/', views.ReviewLikeView.as_view(), name='review_like'),

    # 내 리뷰 목록
    path('my/', views.UserReviewListView.as_view(), name='my_reviews'),

    # 새 리뷰 생성 (NewReview.vue 에서 사용)
    path('create/', views.ReviewCreateView.as_view(), name='review_create'),
]
