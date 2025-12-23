from django.urls import path, include
from .views import CustomUserDetailsView
from . import views

urlpatterns = [
    # /accounts/user/ -> 회원정보 조회/수정/탈퇴 (GET, PUT, DELETE)
    # dj-rest-auth의 기본 UserDetailsView 대신 우리가 만든 CustomUserDetailsView를 사용
    path('user/', CustomUserDetailsView.as_view(), name='user_details'),

    # [수정] 마이페이지 통합 데이터
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),

    # /accounts/signup/ -> 회원가입 (POST)
    # dj-rest-auth의 회원가입 기능을 포함
    path('signup/', include('dj_rest_auth.registration.urls')),

    # /accounts/login/, /accounts/logout/ 등 dj-rest-auth의 핵심 인증 기능 포함
    path('', include('dj_rest_auth.urls')),
    path('preferences/', views.update_preferences, name='update_preferences'),
    path('profile-image/', views.update_profile_image, name='update_profile_image'),
    path('user/', views.user_detail, name='user_detail'),
    path('check-nickname/', views.check_nickname, name='check_nickname'),

    # 팔로우 관련 API
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('followers/', views.followers_list, name='followers_list'),
    path('following/', views.following_list, name='following_list'),

]
