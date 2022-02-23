from django.core.management.base import BaseCommand, CommandError
from certifier.models import RunReconstruction, TrackerCertification
from . import _factories


class Command(BaseCommand):
    help = 'Populates the DB with fake data'

    def handle(self, *args, **options):

        pix_problems = _factories.PixelProblemFactory.create_batch(size=3)
        strip_problems = _factories.StripProblemFactory.create_batch(size=3)
        tracking_problems = _factories.TrackingProblemFactory.create_batch(
            size=3)
        ref_trackercert = _factories.TrackerCertificationFactory.create(
            runreconstruction__is_reference=True)
        test_trackercert = _factories.TrackerCertificationFactory.create_batch(
            size=10,
            pixel_problems=pix_problems,
            tracking_problems=tracking_problems,
            strip_problems=strip_problems)
        self.stdout.write(
            self.style.SUCCESS(f"Created pks: {repr(test_trackercert)}"))
