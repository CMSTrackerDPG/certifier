# Generated by Django 4.0.4 on 2022-07-11 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oms', '0008_alter_omsfill_first_run_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='omsrun',
            name='apv_mode',
            field=models.CharField(choices=[('DECO', 'DECO'), ('PEAK', 'PEAK')], help_text='APV mode', max_length=4, null=True),
        ),
    ]
