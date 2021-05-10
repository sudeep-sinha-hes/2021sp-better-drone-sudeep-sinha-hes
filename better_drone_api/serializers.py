from rest_framework import serializers
from .models import Build, Repo


class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ('id', 'status', 'event', 'target', 'author_email', 'started', 'finished')


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ('id', 'name', 'namespace')