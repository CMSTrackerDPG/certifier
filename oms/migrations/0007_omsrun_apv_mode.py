# Generated by Django 4.0.4 on 2022-07-06 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oms', '0006_alter_omsrun_b_field_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='omsrun',
            name='apv_mode',
            field=models.CharField(choices=[('DECO', 'DECO'), ('PEAK', 'PEAK')], default=None, help_text='APV mode', max_length=4, null=True),
        ),
    ]