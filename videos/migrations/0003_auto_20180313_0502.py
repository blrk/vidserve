# Generated by Django 2.0.2 on 2018-03-13 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20180313_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
