# Generated by Django 4.0.4 on 2022-07-13 17:43

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remotescripts', '0002_scriptargumentbase_help_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptconfigurationbase',
            name='help_text',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Help text/instructions for users', max_length=600, null=True),
        ),
    ]
