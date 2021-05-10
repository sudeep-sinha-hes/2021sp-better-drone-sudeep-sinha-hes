from django.db import models
from .BuildStatus import BuildStatus
from .Repo import Repo


class Build(models.Model):
    class Meta:
        db_table = 'builds'
        ordering = ('-started', )

    class BuildObjects(models.Manager):
        def get_all_completed(self):
            return super().get_queryset().exclude(status='pending')

    app_label = 'better_drone_api'

    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    build_id = models.IntegerField(unique=True)
    status = models.CharField(
        max_length=7,
        choices=[(c.name, c.value) for c in BuildStatus]
    )
    event = models.CharField(
        max_length=20
    )
    deploy_to = models.CharField(
        max_length=50
    )
    message = models.CharField(
        max_length=50
    )
    before = models.CharField(
        max_length=40
    )
    after = models.CharField(
        max_length=40
    )
    ref = models.CharField(
        max_length=255
    )
    target = models.CharField(
        max_length=100
    )
    author_email = models.CharField(
        max_length=320
    )
    started = models.DateTimeField()
    finished = models.DateTimeField()
    objects = models.Manager()
    buildobjects = BuildObjects()

    def __str__(self):
        return self.after
