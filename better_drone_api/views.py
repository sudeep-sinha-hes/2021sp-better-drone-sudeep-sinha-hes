from rest_framework import generics

from .models import Build, Stage, Step, Repo, BuildStatus
from .serializers import BuildSerializer, RepoSerializer
from datetime import datetime


def apply_filters(qs, params):
    start = params.get('start')
    end = params.get('end')
    status = params.get('status')
    event = params.get('event')
    target = params.get('target')

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

    return qs


def apply_sort(qs, params):
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
    serializer_class = BuildSerializer


class ListCreateRepos(generics.ListCreateAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer


class RepoDetails(generics.RetrieveDestroyAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
