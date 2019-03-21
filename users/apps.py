from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import users.signals
