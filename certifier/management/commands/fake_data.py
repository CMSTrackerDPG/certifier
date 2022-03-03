from django.core.management.base import BaseCommand, CommandError
from certifier.models import RunReconstruction, TrackerCertification
from . import _factories


class Command(BaseCommand):
    help = 'Populates the DB with fake data (users, tracker certification entries etc.)'

    def handle(self, *args, **options):

        # Create 3x Pixel, Strip and Tracking problems
        pix_problems = _factories.PixelProblemFactory.create_batch(size=3)
        strip_problems = _factories.StripProblemFactory.create_batch(size=3)
        tracking_problems = _factories.TrackingProblemFactory.create_batch(
            size=3)

        # Create a single Runreconstruction which is also a reference one
        ref_runreconstruction = _factories.RunReconstructionFactory.create(
            is_reference=True)

        shifters = _factories.ShifterFactory.create_batch(size=5)
        shiftleaders = _factories.ShiftLeaderFactory.create_batch(size=2)

        # Create 10x TrackerCertification entries.
        # This should create all the required entries on related tables
        # like users, OmsRuns etc.
        # Use the previously created Runreconstruction as reference.
        test_trackercert = _factories.TrackerCertificationFactory.create_batch(
            size=10,
            pixel_problems=pix_problems,
            tracking_problems=tracking_problems,
            strip_problems=strip_problems,
            reference_runreconstruction=ref_runreconstruction)
        self.stdout.write(
            self.style.SUCCESS(f"Created pks: {repr(test_trackercert)}"))
