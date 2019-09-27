from django.db import models

# Create your models here.

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        try:
            self.__class__.objects.get().delete()
        except self.__class__.DoesNotExist:
            pass

        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

class ChartDataModel(SingletonModel):
    pca_data = models.TextField()
    t_sne_data = models.TextField()
    umap_data = models.TextField()
