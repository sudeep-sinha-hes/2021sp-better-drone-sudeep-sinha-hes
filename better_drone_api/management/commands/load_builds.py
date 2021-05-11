from django.core.management import BaseCommand
from luigi import build
import datetime

from ...tasks import StoreBuilds


class Command(BaseCommand):
    help = "Load build data"

    def handle(self, *args, **options):
        """Populates the DB with review aggregations"""
        build([
            # StoreBuilds(datetime.datetime.now().strftime('%b_%d_%y_%H_%M'))
            StoreBuilds('May_10_21_14_19')
        ], local_scheduler=True)
