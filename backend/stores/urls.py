from django.urls import path, include
from . import views
from reviews.views import ReviewListCreateView # reviews 앱의 뷰를 가져옴
from .views import StoreAISummaryView

urlpatterns = [
    path('map/', views.MapStoreListView.as_view(), name='map_store_list'),
    path('', views.StoreListView.as_view(), name='store_list'),
    path('<int:pk>/', views.StoreDetailView.as_view(), name='store_detail'),
    path('<int:store_pk>/bookmark/', views.BookmarkView.as_view(), name='bookmark'),
    
    # /stores/<store_pk>/reviews/ 경로에 대한 URL 패턴 추가
    path('<int:store_pk>/reviews/', ReviewListCreateView.as_view(), name='review_list_create'),
    path('my_bookmarks/', views.UserBookmarkListView.as_view(), name='my_bookmarks'), # 추가된 URL

    path('weekly-pick/', views.WeeklyPickView.as_view(), name='weekly_pick'),
    path('stores/<int:pk>/ai-summary/', StoreAISummaryView.as_view(), name='store-ai-summary'),
]

