# Generated by Django 3.0.4 on 2020-05-06 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0004_auto_20200506_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='url',
            new_name='image',
        ),
    ]
