# Generated by Django 3.0.4 on 2020-05-14 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0023_auto_20200514_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='homologue',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
