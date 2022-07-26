from django.db import models


class SoftDeletionManager(models.Manager):
    use_in_migrations = True

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def dead(self):
        """
        :return: QuerySet containing all instances that have been deleted
        """
        return self.get_queryset().dead()

    def alive(self):
        """
        :return: QuerySet containing all instances that have not been deleted
        """
        return self.get_queryset().alive()
