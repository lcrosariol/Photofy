# Generated by Django 4.0.3 on 2022-05-24 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='paid',
        ),
        migrations.AddField(
            model_name='transaction',
            name='paid',
            field=models.BooleanField(default=1, verbose_name='Paid'),
            preserve_default=False,
        ),
    ]