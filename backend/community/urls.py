from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommunityPostListView.as_view(), name='post_list'),
    path('create/', views.CommunityPostCreateView.as_view(), name='post_create'),
]
