from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from .signals import create_auth_token

        post_save.connect(create_auth_token, sender=User)
