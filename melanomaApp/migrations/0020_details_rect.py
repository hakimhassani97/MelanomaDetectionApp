# Generated by Django 3.0.4 on 2020-05-13 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0019_merge_20200513_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='rect',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]