from django.db import models

from .BuildStatus import BuildStatus
from .Build import Build
from .Repo import Repo


class Stage(models.Model):
    class Meta:
        db_table = 'stages'

    app_label = 'better_drone_api'

    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name="stages", related_query_name="stage")
    stage_id = models.IntegerField(unique=True)
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
    started = models.DateTimeField()
    stopped = models.DateTimeField()
    on_success = models.BooleanField()
    on_failure = models.BooleanField()

    def __str__(self):
        return self.name

