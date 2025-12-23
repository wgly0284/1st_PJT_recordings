from django.urls import path
from . import views
from reviews.views import ReviewListCreateView 
from .views import StoreAISummaryView

urlpatterns = [
    path('map/', views.MapStoreListView.as_view(), name='map_store_list'),
    path('', views.StoreListView.as_view(), name='store_list'),
    
    # 상세 페이지: /stores/1/
    path('<int:pk>/', views.StoreDetailView.as_view(), name='store_detail'),
    
    path('<int:store_pk>/bookmark/', views.BookmarkView.as_view(), name='bookmark'),
    
    # 리뷰: /stores/1/reviews/
    path('<int:store_pk>/reviews/', ReviewListCreateView.as_view(), name='review_list_create'),
    path('my_bookmarks/', views.UserBookmarkListView.as_view(), name='my_bookmarks'),
    
    path('weekly-pick/', views.WeeklyPickView.as_view(), name='weekly_pick'),

    # [수정] stores/ 를 제거했습니다.
    # 기존: path('stores/<int:pk>/ai-summary/', ...) -> 실제 URL: /stores/stores/1/ai-summary/ (404 원인)
    # 변경: path('<int:pk>/ai-summary/', ...)       -> 실제 URL: /stores/1/ai-summary/ (정상)
    path('<int:pk>/ai-summary/', StoreAISummaryView.as_view(), name='store-ai-summary'),
]