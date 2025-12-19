from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

    def ready(self):
        # 순환 참조를 피하기 위해 ready() 메소드 안에서 import
        from django.db.models.signals import post_save, post_delete
        from . import signals

        # 현재 앱의 'Review' 모델을 가져옴
        Review = self.get_model('Review')

        # 시그널 핸들러를 직접 연결
        post_save.connect(signals.update_store_rating_on_save, sender=Review)
        post_delete.connect(signals.update_store_rating_on_delete, sender=Review)