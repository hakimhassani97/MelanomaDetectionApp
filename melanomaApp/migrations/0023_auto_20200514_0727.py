# Generated by Django 2.1.15 on 2020-05-14 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0022_details_posttraitement'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='enclosingCircle',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='details',
            name='lengtheningIndex',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='details',
            name='openCircle',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]