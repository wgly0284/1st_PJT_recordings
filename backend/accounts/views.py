from rest_framework import generics
from dj_rest_auth.views import UserDetailsView
from .serializers import CustomUserDetailsSerializer
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()


# dj-rest-auth의 UserDetailsView를 상속받아 우리가 만든 Serializer를 사용하도록 설정
class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer
    queryset = User.objects.all()
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_preferences(request):
    """빵 선호도 업데이트"""
    bread_preferences = request.data.get('bread_preferences', '')
    
    # 사용자 모델에 직접 저장
    request.user.bread_preferences = bread_preferences
    request.user.save()
    
    return Response({
        'bread_preferences': bread_preferences,
        'message': '빵 선호도 업데이트 완료'
    }, status=status.HTTP_200_OK)
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_image(request):
    """프로필 이미지 업데이트"""
    if 'profile_image' not in request.FILES:
        return Response({'error': '이미지 파일이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    profile_image = request.FILES['profile_image']
    
    # media/profile_images/ 폴더에 저장
    filename = default_storage.save(
        f'profile_images/{request.user.id}_{profile_image.name}', 
        profile_image
    )
    image_url = default_storage.url(filename)
    
    # DB에 URL만 저장
    request.user.profile_image_url = image_url
    request.user.save()
    
    return Response({
        'profile_image_url': image_url,
        'message': '프로필 이미지가 업데이트되었습니다.'
    }, status=status.HTTP_200_OK)
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    """현재 로그인한 사용자 정보 반환"""
    serializer = UserSerializer(request.user)  # UserSerializer 필요
    return Response(serializer.data)



def check_nickname(request):
    nickname = request.GET.get('nickname', '').strip()

    # 비어있으면 사용 불가로 처리
    if not nickname:
        return JsonResponse({'available': False}, status=200)

    # 현재 로그인 유저는 자기 닉네임 그대로 쓰는 건 허용
    if request.user.is_authenticated and request.user.nickname == nickname:
        return JsonResponse({'available': True}, status=200)

    exists = User.objects.filter(nickname=nickname).exists()
    return JsonResponse({'available': not exists}, status=200)