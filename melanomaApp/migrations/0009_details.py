# Generated by Django 3.0.4 on 2020-05-10 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0008_caracteristic_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extract', models.ImageField(default=None, upload_to='segmentations')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='melanomaApp.Image')),
            ],
        ),
    ]
