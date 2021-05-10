from django.db import models

from .BuildStatus import BuildStatus
from .Build import Build
from .Repo import Repo


class Stage(models.Model):
    class Meta:
        db_table = 'stages'

    app_label = 'better_drone'

    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100
    )
    kind = models.CharField(
        max_length=50
    )
    type = models.CharField(
        max_length=50
    )
    status = models.CharField(
        max_length=7,
        choices=[(c.name, c.value) for c in BuildStatus]
    )
    ignore_error = models.BooleanField()
    started = models.DateTimeField()
    stopped = models.DateTimeField()
    on_success = models.BooleanField()
    on_failure = models.BooleanField()

    def __str__(self):
        return self.name

