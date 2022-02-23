from django.core.management.base import BaseCommand, CommandError
from certifier.models import RunReconstruction, TrackerCertification
from . import _factories


class Command(BaseCommand):
    help = 'Populates the DB with fake data'

    # def add_arguments(self, parser):
    # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()
        # test = _factory.RandomTrackerCertification()
        # test_run = _factory.RunReconstructionFactory.build()
        pix_problems = _factories.PixelProblemFactory.create_batch(size=3)
        strip_problems = _factories.StripProblemFactory.create_batch(size=3)
        tracking_problems = _factories.TrackingProblemFactory.create_batch(
            size=3)
        ref_trackercert = _factories.TrackerCertificationFactory.create(
            runreconstruction__is_reference=True)
        test_trackercert = _factories.TrackerCertificationFactory.create_batch(
            size=10, pixel_problems=pix_problems)
        self.stdout.write(
            self.style.SUCCESS(f"Created pks: {repr(test_trackercert)}"))
