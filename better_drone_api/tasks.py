import os
import pandas as pd
import requests

from dask import delayed, compute, dataframe as ddf
from luigi import Task, ExternalTask, Parameter

from csci_utils.luigi.task import Requires, Requirement
from csci_utils.luigi.dask.target import CSVTarget

from .targets import DateRangeTarget, StoreBuildsTarget


def get_base_output_path():
    return os.path.join(os.getcwd(), os.environ.get('BASE_OUTPUT_PATH', 'data'))


class DateRange(ExternalTask):
    def output(self):
        return DateRangeTarget()


class BaseBDroneTask(Task):
    drone_url = os.environ.get('DRONE_URL')
    headers = {"Authorization": f"Bearer {os.environ.get('DRONE_KEY')}"}

    def get_result(self, path, payload={}):
        response = requests.get(
            f"{self.drone_url}/api/repos/{path}", headers=self.headers, params=payload
        )
        return response.json()

    def run(self):
        raise NotImplementedError()

    def output(self):
        raise NotImplementedError()

    def requires(self):
        raise NotImplementedError()


columns = [
    "id",
    "repo_id",
    "number",
    "status",
    "event",
    "deploy_to",
    "message",
    "before",
    "after",
    "ref",
    "target",
    "author_email",
    "started",
    "finished",
]


class FetchBuilds(BaseBDroneTask):
    requires = Requires()
    date_range = Requirement(DateRange)
    timestamp = Parameter()

    def __init__(self, timestamp):
        super(FetchBuilds, self).__init__(timestamp)
        self.output_path = os.path.join(get_base_output_path(), timestamp, "builds")

    @delayed
    def fetch_data(self, repo, repo_id, start_date):
        page_no = 1

        dfs = []

        while True:
            payload = {"page": page_no, "branch": "main"}
            resp_json = self.get_result(
                f"{repo}/builds",
                payload
            )

            if len(resp_json) > 0:
                pd_df = pd.DataFrame(resp_json, columns=columns).fillna('None')
                dfs.append(ddf.from_pandas(pd_df, npartitions=1))

                if resp_json[:-1][0]["started"] < int(start_date.strftime('%s')):
                    break

                page_no += 1
            else:
                break

        df = ddf.concat(dfs)
        df["repo_id"] = repo_id
        df["repo_name"] = repo

        return df

    def run(self):
        print("########## Fetching Builds ############")
        date_range = self.input()["date_range"].get_date_range()
        self.input()["date_range"].mark_fetching()

        targets = [
            self.fetch_data(dr["repo"], dr["repo_id"], dr["start_date"])
            for dr in date_range
        ]

        dfs = ddf.concat([*compute(*targets)], axis=0)
        self.output().write_dask(dfs)

    def output(self):
        return CSVTarget(
            path=self.output_path + os.path.sep,
            glob="*.part"
        )


class FetchBuildDetails(BaseBDroneTask):
    requires = Requires()
    builds = Requirement(FetchBuilds)
    timestamp = Parameter()

    @delayed
    def fetch_build_details(self, repo, build_id, repo_id):
        resp_json = self.get_result(f"{repo}/builds/{build_id}")
        df = pd.DataFrame(resp_json, columns=[*columns, 'stages']).fillna('None')
        df['repo_id'] = repo_id

        return ddf.from_pandas(df, npartitions=1)

    def __init__(self, timestamp):
        super(FetchBuildDetails, self).__init__(timestamp)
        self.output_path = os.path.join(get_base_output_path(), timestamp, "details")

    def run(self):
        print("########## Fetching Build Details ############")
        df = self.input()["builds"].read_dask()
        fetches = list(df
                       .apply(lambda r: self.fetch_build_details(r["repo_name"], r["number"], r["repo_id"]), axis=1)
                       .compute())

        dfs = ddf.concat([*compute(*fetches)], axis=0)\
            .set_index('number')\
            .map_partitions(lambda x: x.sort_index())

        self.output().write_dask(dfs)

    def output(self):
        return CSVTarget(
            path=self.output_path + os.path.sep,
            glob="*.part"
        )


class StoreBuilds(Task):
    requires = Requires()
    details = Requirement(FetchBuildDetails)
    timestamp = Parameter()

    def run(self):
        df = self.input()['details'].read_dask()
        df.set_index('number')
        df = df.map_partitions(lambda x: x.sort_index())
        self.output().insert_data(df)
        self.output().mark_fetched()

    def output(self):
        return StoreBuildsTarget()
