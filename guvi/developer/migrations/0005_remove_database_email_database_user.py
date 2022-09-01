# Generated by Django 4.1 on 2022-09-01 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('developer', '0004_alter_database_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database',
            name='email',
        ),
        migrations.AddField(
            model_name='database',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
