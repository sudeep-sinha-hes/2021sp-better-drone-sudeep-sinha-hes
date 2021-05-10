from django.db import models


class Repo(models.Model):
    class Meta:
        db_table = 'repos'

    app_label = 'better_drone'
    namespace = models.CharField(
        max_length=50
    )
    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name

