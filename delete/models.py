from certifier.manager import SoftDeletionManager
from django.db import models
from django.utils import timezone

class SoftDeletionModel(models.Model):
    """
    Marks object as deleted rather than irrevocably deleting that object
    Also adds timestamps for creation time and update time

    check https://medium.com/@adriennedomingus/soft-deletion-in-django-e4882581c340
    for further information
    """

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(SoftDeletionModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()

    def restore(self):
        self.deleted_at = None
        self.save()
