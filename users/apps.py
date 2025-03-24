from typing import override
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name: str = 'users'

    @override
    def ready(self) -> None:
        import users.signals
