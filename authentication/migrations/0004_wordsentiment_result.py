# Generated by Django 4.1 on 2022-09-04 20:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_wordsentiment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordsentiment',
            name='result',
            field=models.CharField(default=django.utils.timezone.now, max_length=12),
            preserve_default=False,
        ),
    ]
