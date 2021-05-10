from django.test import TestCase as DjangoTestCase
from datetime import date

from .models import FetchJob, Repo
from .targets import DateRangeTarget


# Create your tests here.
class TestDateRange(DjangoTestCase):
    def setUp(self) -> None:
        self.repo = Repo.objects.create(
            namespace='sqsp',
            name='composer'
        )
        self.fetchJob = FetchJob.objects.create(
            repo_id=self.repo.id,
            start_date=date.fromisoformat('2021-01-01'),
            end_date=date.fromisoformat('2021-01-05'),
            fetched=False
        )
        self.fetchJob1 = FetchJob.objects.create(
            repo_id=self.repo.id,
            start_date=date.fromisoformat('2021-01-10'),
            end_date=date.fromisoformat('2021-01-15'),
            fetched=False
        )

        self.target = DateRangeTarget()

    def _check_results(self, result_len, repo_name, start_date, repo_id):
        date_range = self.target.get_date_range()

        self.assertEqual(len(date_range), result_len)
        self.assertEqual(date_range[0]["repo"], repo_name)
        self.assertEqual(date_range[0]["repo_id"], repo_id)
        self.assertEqual(date_range[0]["start_date"], date.fromisoformat(start_date))

    def test_date_range(self):
        self.assertTrue(self.target.exists())
        self._check_results(1, 'sqsp/composer', '2021-01-01', self.repo.id)

    def test_1_job_fetched(self):
        # lets mark the first job fetched
        self.fetchJob.fetched = True
        self.fetchJob.save()

        self.assertTrue(self.target.exists())
        self._check_results(1, 'sqsp/composer', '2021-01-10', self.repo.id)

    def test_no_job(self):
        # lets mark both the jobs as fetched
        self.fetchJob1.fetched = True
        self.fetchJob1.save()
        self.fetchJob.fetched = True
        self.fetchJob.save()

        self.assertFalse(self.target.exists())
