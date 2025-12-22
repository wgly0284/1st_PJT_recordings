# reviews/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review


@receiver(post_save, sender=Review)
def update_store_rating_on_save(sender, instance, **kwargs):
    # ✅ store가 없는 리뷰(빵 주저리, 빵 꿀팁 등)는 그냥 무시
    if instance.store is None:
        return

    store = instance.store
    avg_rating = Review.objects.filter(store=store).aggregate(avg=Avg('rating'))['avg']
    store.avg_rating = avg_rating if avg_rating is not None else 0.0
    store.save()


@receiver(post_delete, sender=Review)
def update_store_rating_on_delete(sender, instance, **kwargs):
    if instance.store is None:
        return

    store = instance.store
    avg_rating = Review.objects.filter(store=store).aggregate(avg=Avg('rating'))['avg']
    store.avg_rating = avg_rating if avg_rating is not None else 0.0
    store.save()
