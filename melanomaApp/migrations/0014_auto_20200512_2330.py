# Generated by Django 3.0.4 on 2020-05-12 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0013_auto_20200512_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='contour',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='details',
            name='extract',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]