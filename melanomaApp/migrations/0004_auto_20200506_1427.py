# Generated by Django 3.0.4 on 2020-05-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0003_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.ImageField(default=None, upload_to='melanomaApp/images'),
        ),
    ]
