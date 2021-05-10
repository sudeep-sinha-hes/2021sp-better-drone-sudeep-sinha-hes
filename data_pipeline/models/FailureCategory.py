from django.db import models

from .Repo import Repo


class FailureCategory(models.Model):
    class Meta:
        db_table = 'failure_categories'

    app_label = 'better_drone'

    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30
    )
    regexp = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name
