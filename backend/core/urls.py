from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('stores/', include('stores.urls')),
    path('reviews/', include('reviews.urls')),
]