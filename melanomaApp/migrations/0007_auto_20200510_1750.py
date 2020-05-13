# Generated by Django 3.0.4 on 2020-05-10 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('melanomaApp', '0006_auto_20200510_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='doctor',
        ),
        migrations.AddField(
            model_name='image',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='melanomaApp.Patient'),
        ),
    ]