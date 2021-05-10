from luigi import Target
from django.db.models import Value, F, Min
from django.db.models.functions import Concat

from .models import FetchJob


class DateRangeTarget(Target):
    def exists(self):
        return FetchJob.objects.filter(fetched=False).exists()

    def get_date_range(self):
        return FetchJob.objects.filter(
            fetched=False
        ).annotate(
            repo_name=Concat('repo__namespace', Value('/'), 'repo__name'),
        ).values(
            'repo_name'
        ).annotate(
            repo_id=F('repo_id'),
            repo=F('repo_name'),
            start_date=Min('start_date'),
        )
