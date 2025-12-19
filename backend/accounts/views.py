from rest_framework import generics
from dj_rest_auth.views import UserDetailsView
from .serializers import CustomUserDetailsSerializer
from .models import User

# dj-rest-auth의 UserDetailsView를 상속받아 우리가 만든 Serializer를 사용하도록 설정
class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer
    queryset = User.objects.all()