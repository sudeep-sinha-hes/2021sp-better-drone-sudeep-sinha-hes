import os
import pandas as pd
import requests
import json

from dask import delayed, compute, dataframe as ddf
from luigi import Task, ExternalTask, Parameter, LocalTarget

from csci_utils.luigi.task import TargetOutput, Requires, Requirement
from csci_utils.luigi.dask.target import ParquetTarget, CSVTarget

from .targets import DateRangeTarget


class DateRange(ExternalTask):
    def output(self):
        return DateRangeTarget(
            host=os.environ.get('DB_HOST', default='127.0.0.1'),
            port=os.environ.get('DB_PORT', default='5432'),
            database='bdrone',
            user=os.environ.get('DB_USER_NAME', default='bdrone'),
            password=os.environ.get('DB_PASSWD', default='bdrone')
        )


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


class FetchBuilds(BaseBDroneTask):
    requires = Requires()
    date_range = Requirement(DateRange)
    timestamp = Parameter()

    columns = [
        "repo_id",
        "number",
        "status",
        "event",
        "message",
        "before",
        "after",
        "ref",
        "target",
        "author_email",
        "started",
        "finished",
    ]

    def __init__(self, timestamp):
        super(FetchBuilds, self).__init__(timestamp)
        self.output_path = os.path.join(os.getcwd(), "data", timestamp, "builds")

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
                dfs.append(ddf.from_pandas(pd.DataFrame(resp_json, columns=self.columns), npartitions=1))

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
        df = pd.DataFrame(date_range)

        df.columns = df.iloc[0]
        df = df[1:]

        s = df.groupby(['repo', 'repo_id']).agg({'start_date': ['min']})
        s.columns = s.columns.droplevel(1)

        print(s)
        targets = []

        for dfi in s.index:
            start_date = s.loc[dfi, :]['start_date']
            fetch_tasks = self.fetch_data(dfi[0], dfi[1], start_date)
            targets.append(fetch_tasks)

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
        df = pd.DataFrame(resp_json, columns=resp_json.keys())
        return ddf.from_pandas(df, npartitions=1)

    def __init__(self, timestamp):
        super(FetchBuildDetails, self).__init__(timestamp)
        self.output_path = os.path.join(os.getcwd(), "data", timestamp, "details")

    def run(self):
        print("########## Fetching Build Details ############")
        df = self.input()["builds"].read_dask()
        fetches = list(df
                       .apply(lambda r: self.fetch_build_details(r["repo_name"], r["number"], r["repo_id"]), axis=1)
                       .compute())

        dfs = ddf.concat([*compute(*fetches)], axis=0)
        self.output().write_dask(dfs)

    def output(self):
        return CSVTarget(
            path=self.output_path + os.path.sep
        )
