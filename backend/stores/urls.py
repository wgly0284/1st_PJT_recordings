from django.urls import path
from .views import (
    StoreListView, 
    StoreDetailView, 
    MapStoreListView,
    StoreAISummaryView,
    BookmarkView,
    UserBookmarkListView,
    WeeklyPickView,
    DailyRecommendationView,
    BakeryChatBotView  # ✅ 챗봇 뷰 추가
)

urlpatterns = [
    # 1. 가게 목록 및 상세
    path('', StoreListView.as_view(), name='store-list'),
    path('<int:pk>/', StoreDetailView.as_view(), name='store-detail'),
    
    # 2. 지도용 목록
    path('map/', MapStoreListView.as_view(), name='map-store-list'),
    
    # 3. 북마크 관련
    path('<int:store_pk>/bookmark/', BookmarkView.as_view(), name='store-bookmark'),
    path('bookmarks/', UserBookmarkListView.as_view(), name='user-bookmarks'),
    
    # 4. 추천 및 AI 요약
    path('weekly-pick/', WeeklyPickView.as_view(), name='weekly-pick'),
    path('<int:pk>/ai-summary/', StoreAISummaryView.as_view(), name='store-ai-summary'),
    path('daily-recommendation/', DailyRecommendationView.as_view(), name='daily-recommendation'),

    # 5. ✅ 챗봇 API
    path('chatbot/', BakeryChatBotView.as_view(), name='bakery-chatbot'),
]