from rest_framework import generics

from .models import Build, Stage, Step, Repo, BuildStatus
from .serializers import BuildSerializer, RepoSerializer, BuildDetailsSerializer
from datetime import datetime


def apply_filters(qs, params):
    start = params.get('start')
    end = params.get('end')
    status = params.get('status')
    event = params.get('event')
    target = params.get('target')
    deploy_to = params.get('deploy_to')
    fail_type = params.get('fail_type')

    if start is not None:
        qs = qs.filter(
            started__gte=datetime.fromtimestamp(start)
        )
    if end is not None:
        qs = qs.filter(
            started__lt=datetime.fromtimestamp(end)
        )
    if status is not None:
        qs = qs.filter(
            status=status
        )
    if event is not None:
        qs = qs.filter(
            event=event
        )
    if target is not None:
        qs = qs.filter(
            target=target
        )
    if deploy_to is not None:
        qs = qs.filter(
            deploy_to=deploy_to
        )
    if fail_type is not None:
        qs = qs.filter(
            stage__step__status='failure',
            stage__step__name__startswith=fail_type,
        )

    return qs


def apply_sort(qs, params):
    sort = params.get('sort')

    if sort is not None:
        qs = qs.order_by(*sort.split(','))

    return qs


# Create your views here.
class ListBuilds(generics.ListAPIView):
    serializer_class = BuildSerializer

    def get_queryset(self):
        qs = Build.objects.all()
        params = self.request.query_params
        qs = apply_filters(qs, params)
        qs = apply_sort(qs, params)

        return qs


class BuildDetails(generics.RetrieveAPIView):
    queryset = Build.objects.all()
    serializer_class = BuildDetailsSerializer


class ListCreateRepos(generics.ListCreateAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer


class RepoDetails(generics.RetrieveDestroyAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
