# Generated by Django 3.2.2 on 2021-05-10 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('better_drone_api', '0008_build_deploy_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='build',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', related_query_name='stage', to='better_drone_api.build'),
        ),
        migrations.AlterField(
            model_name='step',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', related_query_name='step', to='better_drone_api.stage'),
        ),
    ]
