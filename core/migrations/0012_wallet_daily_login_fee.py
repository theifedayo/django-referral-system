# Generated by Django 2.2 on 2020-09-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200916_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='daily_login_fee',
            field=models.FloatField(default='0'),
        ),
    ]