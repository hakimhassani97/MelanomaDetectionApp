# Generated by Django 3.0.4 on 2020-05-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0024_details_homologue'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='subregion',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
