from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('<int:review_pk>/like/', views.ReviewLikeView.as_view(), name='review_like'),
    path('my/', views.UserReviewListView.as_view(), name='my_reviews'), # 추가된 URL
]
