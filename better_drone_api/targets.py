import ast
from luigi import Target
from django.db.models import Value, F, Min
from django.db.models.functions import Concat
from django.db.transaction import atomic
from datetime import datetime

from .models import FetchJob, Build, Repo, Stage, Step, BuildStatus


class DateRangeTarget(Target):
    def __init__(self):
        self.jobs_to_fetch_ids = [d['id'] for d in FetchJob.objects.filter(
            fetched=False,
            fetching=False,
        ).values('id')]

    def exists(self):
        return len(self.jobs_to_fetch_ids) > 0

    def get_date_range(self):
        print("#### Getting Date Range ####")

        return FetchJob.objects.filter(
            id__in=self.jobs_to_fetch_ids
        ).annotate(
            repo_name=Concat('repo__namespace', Value('/'), 'repo__name'),
        ).values(
            'repo_name'
        ).annotate(
            repo_id=F('repo_id'),
            repo=F('repo_name'),
            start_date=Min('start_date')
        )

    def mark_fetching(self):
        print("#### Marking all the fetchable jobs as fetching ####")
        return FetchJob.objects.filter(id__in=self.jobs_to_fetch_ids).update(fetching=True)


def extract_set_val(data, col_name):
    return next(iter(data[col_name]))


def extract_obj_values(data, cols, overrides):
    return {
        col: overrides[col](data) if col in overrides.keys() else extract_set_val(data, col)
        for col in cols
    }


def insert_build(build_id, data):
    # check if the build exists
    if Build.objects.filter(build_id=build_id).exists():
        print('Build Exists ######### ')
        return Build.objects.get(build_id=build_id)

    params = extract_obj_values(data, [
        'build_id',
        'repo_id',
        'status',
        'event',
        'message',
        'before',
        'after',
        'ref',
        'target',
        'author_email',
        'started',
        'finished',
        'deploy_to',
    ], {
        'build_id': lambda d: build_id,
        'started': lambda d: datetime.fromtimestamp(int(extract_set_val(d, "started"))),
        'finished': lambda d: datetime.fromtimestamp(int(extract_set_val(d, "finished")))
    })

    build = Build.objects.create(**params)
    return build


def insert_stages(build, data):
    for stage in iter(data["stages"]):
        stage = ast.literal_eval(stage)
        if not Stage.objects.filter(
            stage_id=stage['id']
        ).exists():
            params = {
                'repo_id': build.repo.id,
                'build_id': build.id,
                'stage_id': stage['id'],
                'name': stage['name'],
                'kind': stage['kind'],
                'type': stage['type'],
                'status': stage['status'],
                'started': datetime.fromtimestamp(int(stage['started'])),
                'stopped': datetime.fromtimestamp(int(stage['stopped'])),
                'on_success': stage['on_success'],
                'on_failure': stage['on_failure'],
            }
            stage_obj = Stage.objects.create(**params)

            if 'steps' in stage:
                for step in stage['steps']:
                    params = {
                        'stage_id': stage_obj.id,
                        'step_id': step['id'],
                        'name': step['name'],
                        'status': step['status'],
                        'errignore': step['errignore'] if 'errorignore' in step else False,
                        'exit_code': step['exit_code'],
                        'started': datetime.fromtimestamp(int(step['started'])),
                        'stopped': datetime.fromtimestamp(int(step['stopped'])),
                    }
                    Step.objects.create(**params)


class StoreBuildsTarget(Target):
    def __init__(self):
        self.fetching_jobs_ids = [d['id'] for d in FetchJob.objects.filter(
            fetching=False,
            fetched=False
        ).values()]

    def insert_data(self, ddf):
        for n in range(0, ddf.npartitions):
            print(f"### Reading partition: {n} ###")
            df = ddf.get_partition(n).compute()
            dfg = df.groupby('id').agg(set)

            for idx in dfg.index.values:
                with atomic():
                    build = insert_build(build_id=idx, data=dfg.loc[idx])
                    insert_stages(build, data=dfg.loc[idx])

    def exists(self):
        return len(self.fetching_jobs_ids) == 0

    def mark_fetched(self):
        print("#### Marking all the fetching jobs as fetched ####")
        return FetchJob.objects.filter(id__in=self.fetching_jobs_ids).update(fetching=False, fetched=True)
