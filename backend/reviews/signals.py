from django.db.models import Avg

# 데코레이터를 사용하지 않는 일반 함수로 변경
def update_store_rating_on_save(sender, instance, **kwargs):
    """
    리뷰가 생성되거나 업데이트될 때 가게의 평균 평점을 다시 계산합니다.
    """
    store = instance.store
    # 해당 store에 연결된 모든 review의 rating 필드의 평균(Avg)을 계산
    avg_rating = sender.objects.filter(store=store).aggregate(Avg('rating'))['rating__avg']
    
    # 만약 계산된 평균값이 없으면(리뷰가 하나도 없으면) 0으로 설정
    store.avg_rating = avg_rating if avg_rating is not None else 0.00
    store.save()

def update_store_rating_on_delete(sender, instance, **kwargs):
    """
    리뷰가 삭제될 때 가게의 평균 평점을 다시 계산합니다.
    """
    store = instance.store
    avg_rating = sender.objects.filter(store=store).aggregate(Avg('rating'))['rating__avg']
    
    store.avg_rating = avg_rating if avg_rating is not None else 0.00
    store.save()