from django.db import models

from .BuildStatus import BuildStatus
from .Stage import Stage


class Step(models.Model):
    class Meta:
        db_table = 'steps'

    app_label = 'better_drone'

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    step_id = models.IntegerField()
    name = models.CharField(
        max_length=100
    )
    status = models.CharField(
        max_length=7,
        choices=[(c.name, c.value) for c in BuildStatus]
    )
    errignore = models.BooleanField(default=False)
    exit_code = models.IntegerField()
    started = models.DateTimeField()
    stopped = models.DateTimeField()

    def __str__(self):
        return self.name
