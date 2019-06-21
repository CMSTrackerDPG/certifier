from django.db.models import QuerySet
from django.utils import timezone

class SoftDeletionQuerySet(QuerySet):
    """
    QuerySet that marks objects as deleted rather than
    irrevocably deleting objects as default behavior
    """

    def delete(self):
        """
        only pretend to delete (mark as deleted)
        """
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        """
        irrevocably delete all objects in the QuerySet
        """
        return super(SoftDeletionQuerySet, self).delete()

    def restore(self):
        """
        only pretend to delete (mark as deleted)
        """
        return super(SoftDeletionQuerySet, self).update(deleted_at=None)

    def alive(self):
        """
        return only objects that are not deleted
        """
        return self.filter(deleted_at=None)

    def dead(self):
        """
        return only objects that are marked as deleted
        """
        return self.exclude(deleted_at=None)

