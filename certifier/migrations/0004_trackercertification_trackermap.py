# Generated by Django 2.1.7 on 2019-04-10 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certifier', '0003_trackercertification_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackercertification',
            name='trackermap',
            field=models.CharField(choices=[('Exists', 'Exists'), ('Missing', 'Missing')], default='Exists', max_length=7),
            preserve_default=False,
        ),
    ]
