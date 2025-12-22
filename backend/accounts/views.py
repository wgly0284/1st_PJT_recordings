from rest_framework import generics
from dj_rest_auth.views import UserDetailsView
from .serializers import CustomUserDetailsSerializer, UserSerializer
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView  # APIView 추가
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from stores.models import Store # Store 모델 필요 (스탬프용)

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


# [추가] 마이페이지용 통합 데이터 조회 API (스탬프, 취향 분석 등 포함)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. 📜 스탬프 데이터: 내가 리뷰를 남긴 가게들 (중복 제거)
        # Store 모델과 연결된 reviews 역참조 활용
        visited_stores = Store.objects.filter(reviews__user=user).distinct().values('id', 'name', 'category')
        
        # 2. 🔮 취향 분석 데이터: 내가 쓴 리뷰들의 taste_tags 집계
        all_tags = []
        for review in user.review_set.all():
            if review.taste_tags:
                # 콤마로 구분된 태그들을 분리해서 리스트에 추가
                tags = [t.strip() for t in review.taste_tags.split(',') if t.strip()]
                all_tags.extend(tags)
        
        # 태그 빈도수 계산
        from collections import Counter
        taste_counts = Counter(all_tags)
        # 예: {'달달함': 5, '바삭함': 2}
        
        # 많이 나온 순서대로 정렬 (상위 5개 정도만 보내줘도 됨)
        sorted_taste = dict(sorted(taste_counts.items(), key=lambda item: item[1], reverse=True)[:5])

        return Response({
            "username": user.username,
            "nickname": user.nickname,
            "level": user.level,
            "exp": user.exp,
            "max_exp": user.level * 100, # 다음 레벨까지 필요한 경험치 (공식은 변경 가능)
            "character_type": user.character_type,
            "profile_image_url": user.profile_image_url,
            "visit_count": len(visited_stores), # 방문 수
            "review_count": user.review_set.count(), # 리뷰 수
            "visited_stores": list(visited_stores), # 스탬프 목록
            "taste_stats": sorted_taste, # 취향 분석 결과
        }, status=status.HTTP_200_OK)


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