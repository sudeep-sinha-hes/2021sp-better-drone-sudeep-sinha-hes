from django.db import models

from .Repo import Repo


class FetchJob(models.Model):
    class Meta:
        db_table = 'fetch_jobs'

    app_label = 'better_drone'

    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    fetched = models.BooleanField(default=False)
