import factory
from factory import fuzzy
from certifier import models as certifier_models
from oms import models as oms_models
from allauth.socialaccount import models as socialaccount_models
from users import models as users_models


class UserFactory(factory.django.DjangoModelFactory):
    """
    Generic user creation factory with Guest privileges
    """
    class Meta:
        model = users_models.User
        django_get_or_create = ("username", )

    username = factory.Sequence(lambda n: "test%d" % n)
    password = factory.PostGenerationMethodCall("set_password", "1234")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda a: "{}.{}@cern.ch".format(a.first_name, a.last_name).lower())
    is_staff = False
    is_active = True
    date_joined = "2022-02-11 10:54:51.105115+00:00"
    extra_data = "{}"
    # Random user_privilege
    # user_privilege = fuzzy.FuzzyChoice(users_models.User.USER_PRIVILEGE_GROUPS,
    # getter=lambda c: c[0])

    # FixedPrivilege
    user_privilege = users_models.User.GUEST

    # groups =
    # user_permissions =


class ShifterFactory(UserFactory):
    """
    User creation factory with Shifter privileges
    """
    username = factory.Sequence(lambda n: "shifter%d" % n)
    user_privilege = users_models.User.SHIFTER


class ShiftLeaderFactory(UserFactory):
    """
    User creation factory with Shift Leader privileges
    """
    username = factory.Sequence(lambda n: "shiftleader%d" % n)
    user_privilege = users_models.User.SHIFTLEADER


class SocialAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = socialaccount_models.SocialAccount

    user = factory.SubFactory(UserFactory)


class OmsFillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = oms_models.OmsFill
        django_get_or_create = ("fill_number", )

    fill_number = factory.Sequence(lambda n: n)
    b_field = 0.1111
    bunches_beam1 = 1
    bunches_beam2 = 3
    bunches_colliding = 1111
    bunches_target = 8888
    crossing_angle = 1.222
    delivered_lumi = 92.11
    downtime = 999
    duration = 8
    efficiency_lumi = factory.Faker("random_int")
    efficiency_time = factory.Faker("random_int")
    energy = factory.Faker("random_int")
    era = factory.Faker("text")
    fill_type_party1 = "fill1"
    fill_type_party2 = "fill2"
    fill_type_runtime = "runtime"
    init_lumi = 2.1111
    injection_scheme = "injection"
    intensity_beam1 = factory.Faker("random_int")
    intensity_beam2 = factory.Faker("random_int")
    first_run_number = 2
    last_run_number = 3


class OmsRunFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = oms_models.OmsRun
        django_get_or_create = ("run_number", )

    run_number = factory.Sequence(lambda n: n + 348590)
    run_type = fuzzy.FuzzyChoice(oms_models.OmsRun.RUN_TYPE_CHOICES,
                                 getter=lambda c: c[0])
    fill = factory.SubFactory(OmsFillFactory)
    lumisections = factory.Faker("random_int")
    hlt_key = factory.Faker("country")


class RunReconstructionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = certifier_models.RunReconstruction
        django_get_or_create = ("run", )

    run = factory.SubFactory(OmsRunFactory)
    reconstruction = fuzzy.FuzzyChoice(
        certifier_models.RunReconstruction.RECONSTRUCTION_CHOICES,
        getter=lambda c: c[0])


class DatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = certifier_models.Dataset
        django_get_or_create = ("dataset", )

    dataset = factory.Faker("country")


class PixelProblemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = certifier_models.PixelProblem
        django_get_or_create = ("name", )

    name = factory.Sequence(lambda n: "Pixel Problem %d" % n)
    description = f"{name} description"


class StripProblemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = certifier_models.StripProblem
        django_get_or_create = ("name", )

    name = factory.Sequence(lambda n: "Strip Problem %d" % n)
    description = f"{name} description"


class TrackingProblemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = certifier_models.TrackingProblem
        django_get_or_create = ("name", )

    name = factory.Sequence(lambda n: "Tracking Problem %d" % n)
    description = f"{name} description"


class BadReasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = certifier_models.BadReason
        django_get_or_create = ("name", )

    name = factory.Sequence(lambda n: "Bad Reason %d" % n)
    description = f"{name} description"


class TrackerCertificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = certifier_models.TrackerCertification
        django_get_or_create = (
            "runreconstruction",
            "reference_runreconstruction",
            "bad_reason",
            "dataset",
        )

    # user = factory.SubFactory(UserFactory)
    user = factory.Iterator(users_models.User.objects.all())
    runreconstruction = factory.SubFactory(RunReconstructionFactory)
    reference_runreconstruction = factory.SubFactory(RunReconstructionFactory)
    dataset = factory.SubFactory(DatasetFactory)
    date = "2022-02-11"
    pixel = fuzzy.FuzzyChoice(
        certifier_models.TrackerCertification.SUBCOMPONENT_STATUS_CHOICES,
        getter=lambda c: c[0],
    )
    strip = fuzzy.FuzzyChoice(
        certifier_models.TrackerCertification.SUBCOMPONENT_STATUS_CHOICES,
        getter=lambda c: c[0],
    )
    tracking = fuzzy.FuzzyChoice(
        certifier_models.TrackerCertification.SUBCOMPONENT_STATUS_CHOICES,
        getter=lambda c: c[0],
    )
    bad_reason = factory.SubFactory(BadReasonFactory)
    # trackermap = factory.Faker('trackermap')

    # pixel_problems = factory.RelatedFactoryList(PixelProblemFactory, size=5)
    # strip_problems = factory.RelatedFactoryList(StripProblemFactory, size=5)
    # tracking_problems = factory.RelatedFactoryList(TrackingProblemFactory,
    # size=5)

    @factory.post_generation
    def pixel_problems(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of pix problems were passed in, use them
            for pix_problem in extracted:
                self.pixel_problems.add(pix_problem)

    @factory.post_generation
    def strip_problems(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of pix problems were passed in, use them
            for strip_problem in extracted:
                self.strip_problems.add(strip_problem)

    @factory.post_generation
    def tracking_problems(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of pix problems were passed in, use them
            for tracking_problem in extracted:
                self.tracking_problems.add(tracking_problem)


# class RandomTrackerCertification(factory.django.DjangoModelFactory):
#     class Meta:
#         model = models.TrackerCertification

#     trackermap = factory.Faker('trackermap')
