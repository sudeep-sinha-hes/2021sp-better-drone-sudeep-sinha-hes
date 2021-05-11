from rest_framework import serializers
from .models import Build, Repo, Stage, Step


class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ('id', 'status', 'event', 'target', 'author_email', 'started', 'finished', 'deploy_to')


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    class Meta:
        model = Stage
        fields = '__all__'


class BuildDetailsSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True)

    class Meta:
        model = Build
        fields = '__all__'


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ('id', 'name', 'namespace')
