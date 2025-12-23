from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        앱이 시작될 때 signals.py를 임포트하여 신호를 등록합니다.
        """
        import accounts.signals