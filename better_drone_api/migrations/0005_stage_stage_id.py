# Generated by Django 3.2.2 on 2021-05-10 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('better_drone_api', '0004_auto_20210510_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='stage_id',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
