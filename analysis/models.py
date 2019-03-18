from django.db import models

# Create your models here.


class PrincipicalComponents(models.Model):
    run_number = models.PositiveIntegerField(unique=True, primary_key=True)
    reconstruction = models.CharField(max_length=10)

    pc1 = models.FloatField()