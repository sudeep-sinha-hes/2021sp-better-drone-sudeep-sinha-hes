from django.urls import path
from rest_framework.schemas import get_schema_view

from .views import ListBuilds, BuildDetails, ListCreateRepos, RepoDetails

schema_view = get_schema_view(title="Better Drone API")

urlpatterns = [
    path('repos/', ListCreateRepos.as_view(), name="list_create_repos"),
    path('repos/<int:pk>/', RepoDetails.as_view(), name="repo_detail"),
    path('repos/<int:pk>/builds/', ListBuilds.as_view(), name="list_builds"),
    path('repos/<int:repo_id>/builds/<int:pk>/', BuildDetails.as_view(), name='build_detail'),
]