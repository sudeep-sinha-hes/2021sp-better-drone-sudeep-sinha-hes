# Generated by Django 3.2.2 on 2021-05-10 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_pipeline', '0003_alter_build_build_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='ignore_error',
        ),
        migrations.AddField(
            model_name='step',
            name='errignore',
            field=models.BooleanField(default=False),
        ),
    ]
