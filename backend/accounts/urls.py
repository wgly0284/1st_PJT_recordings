from django.urls import path, include
from . import views

urlpatterns = [
    # 1) 내 정보: /accounts/user/  (dj-rest-auth 커스텀)
    path('user/', views.CustomUserDetailsView.as_view(), name='user_details'),

    # 2) 타 유저 프로필: /accounts/user/<int:user_id>/
    path('user/<int:user_id>/', views.user_detail_by_id, name='user_detail_by_id'),

    # 나머지 계정 관련
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('', include('dj_rest_auth.urls')),
    path('preferences/', views.update_preferences, name='update_preferences'),
    path('profile-image/', views.update_profile_image, name='update_profile_image'),
    path('check-nickname/', views.check_nickname, name='check_nickname'),

    # 팔로우 관련
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('followers/', views.followers_list, name='followers_list'),
    path('following/', views.following_list, name='following_list'),
]
