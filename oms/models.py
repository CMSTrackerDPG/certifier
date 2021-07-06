from django.db import models

# Create your models here.


class OmsFill(models.Model):
    """
    CMS Online Monitoring System Fill
    """

    fill_number = models.PositiveIntegerField(
        unique=True, primary_key=True, help_text="Fill number", verbose_name="Fill"
    )

    b_field = models.FloatField(
        help_text="Magnetic field", verbose_name="B Field", null=True
    )
    beta_star = models.FloatField(help_text="β*", verbose_name="β*", null=True)
    bunches_beam1 = models.PositiveIntegerField(
        help_text="Number of bunches beam 1", verbose_name="Bunches Beam1", null=True
    )
    bunches_beam2 = models.PositiveIntegerField(
        help_text="Number of bunches beam 2", verbose_name="Bunches Beam2", null=True
    )
    bunches_colliding = models.PositiveIntegerField(
        help_text="Number of colliding bunches measured by CMS",
        verbose_name="nCollidingBunches",
        null=True,
    )
    bunches_target = models.PositiveIntegerField(
        help_text="Target number of colliding bunches by LHC configuration",
        verbose_name="nTargetBunches",
        null=True,
    )
    crossing_angle = models.FloatField(
        help_text="Crossing angle by LHC configuration",
        verbose_name="Crossing Angle",
        null=True,
    )
    delivered_lumi = models.FloatField(
        help_text="Integrated stable luminosity delivered by LHC",
        verbose_name="Delivered Lumi",
        null=True,
    )
    downtime = models.PositiveIntegerField(
        help_text="Total downtime during the Fill", verbose_name="Downtime", null=True
    )

    # dump_ready_to_dump_time = models.DateTimeField(
    #     help_text="Time from all tracker HV off to beam dumped",
    #     verbose_name="dumpReadyToDump",
    # )

    duration = models.PositiveIntegerField(
        help_text="Duration of the Fill", verbose_name="Duration", null=True
    )
    efficiency_lumi = models.FloatField(
        help_text="The efficiency calculated by luminosity",
        verbose_name="Efficiency by Luminosity",
        null=True,
    )
    efficiency_time = models.FloatField(
        help_text="The efficiency calculated by time",
        verbose_name="Efficiency by Time",
        null=True,
    )

    # end_stable_beam = models.DateTimeField(
    #     help_text="Time when the stable beam was stopped (Warning from LHC)",
    #     verbose_name="End Time (stable beam)",
    # )
    # end_time = models.DateTimeField(
    #     help_text="Time when the beams were dumped or start of new fill",
    #     verbose_name="End Time (dumped)",
    # )

    energy = models.FloatField(
        help_text="LHC target energy", verbose_name="Energy", null=True
    )
    era = models.CharField(
        max_length=40, help_text="Era Name", verbose_name="Era", null=True
    )

    fill_type_party1 = models.CharField(
        max_length=25,
        help_text="Fill Type Party 1",
        verbose_name="Fill Type Party 1",
        null=True,
    )
    fill_type_party2 = models.CharField(
        max_length=25,
        help_text="Fill Type Party 2",
        verbose_name="Fill Type Party 2",
        null=True,
    )
    fill_type_runtime = models.CharField(
        max_length=25, help_text="Fill type", verbose_name="Fill Type", null=True
    )
    init_lumi = models.FloatField(
        help_text="Luminosity at the beginning of the fill",
        verbose_name="InitialLumi",
        null=True,
    )
    injection_scheme = models.CharField(
        max_length=100,
        help_text="Injection scheme",
        verbose_name="Injection scheme",
        null=True,
    )
    intensity_beam1 = models.FloatField(
        help_text="Beam 1 peak intensity", verbose_name="IntensityBeam1", null=True
    )
    intensity_beam2 = models.FloatField(
        help_text="Beam 2 peak intensity", verbose_name="IntensityBeam2", null=True
    )
    peak_lumi = models.FloatField(
        help_text="Peak of instantaneous luminosity during the fill",
        verbose_name="PeakLumi",
        null=True,
    )
    peak_pileup = models.FloatField(
        help_text="Peak pileup", verbose_name="PeakPileup (interactions/BX)", null=True
    )
    peak_specific_lumi = models.FloatField(
        help_text="Peak value of average specific luminosity ",
        verbose_name="PeakSpecificLumi",
        null=True,
    )
    recorded_lumi = models.FloatField(
        help_text="Integrated stable luminosity recorded by CMS",
        verbose_name="Recorded Lumi",
        null=True,
    )

    # start_stable_beam = models.DateTimeField(
    #     help_text="Time when the stable beam was declared",
    #     verbose_name="Begin Time (stable)",
    # )
    # start_time = models.DateTimeField(
    #     help_text="Time when the fill was created",
    #     verbose_name="Create Time (declared)",
    # )
    # to_dump_ready_time = models.DateTimeField(
    #     help_text="Time from LHC message regarding the planned dump of beams to all tracker HV off",
    #     verbose_name="toDumpReady",
    # )
    # to_ready_time = models.DateTimeField(
    #     help_text="Time from stable beam declared to all tracker HV on",
    #     verbose_name="toReady (to HV on)",
    # )

    b_field_unit = models.CharField(max_length=50, default="T")
    peak_lumi_unit = models.CharField(max_length=50, default="10^{34}cm^{-2}s^{-1}")
    beta_star_unit = models.CharField(max_length=50, default="cm")
    init_lumi_unit = models.CharField(max_length=50, default="10^{34}cm^{-2}s^{-1}")
    peak_specific_lumi_unit = models.CharField(max_length=50, default="10^{30}cm^{-2}s^{-1}(10^{11}p)^{-2}")
    intensity_beam2_unit = models.CharField(max_length=50, default="10^{11}")
    intensity_beam1_unit = models.CharField(max_length=50, default="10^{11}")
    delivered_lumi_unit = models.CharField(max_length=50, default="pb^{-1}")
    recorded_lumi_unit = models.CharField(max_length=50, default="pb^{-1}")
    crossing_angle_unit = models.CharField(max_length=50, default="{\\mu}rad")
    energy_unit = models.CharField(max_length=50, default="GeV")

    first_run_number = models.PositiveIntegerField(
        help_text="Run number for the first run in the fill",
        verbose_name="First run number",
    )

    last_run_number = models.PositiveIntegerField(
        help_text="Run number for the last run in the fill",
        verbose_name="Last run number",
    )


class OmsRun(models.Model):
    """
    CMS Online Monitoring System Fill
    """

    RUN_TYPE_CHOICES = (("collisions", "Collisions"), ("cosmics", "Cosmics"))

    run_number = models.PositiveIntegerField(
        help_text="Run number", verbose_name="Run", unique=True, primary_key=True
    )

    run_type = models.CharField(max_length=10, choices=RUN_TYPE_CHOICES)

    fill = models.ForeignKey(OmsFill, on_delete=models.CASCADE)

    lumisections = models.PositiveIntegerField()

    b_field = models.FloatField(
        help_text="Magnetic field", verbose_name="B Field", null=True
    )
    clock_type = models.CharField(
        max_length=4000, help_text="Clock type", verbose_name="Clock type", null=True
    )
    cmssw_version = models.CharField(
        max_length=4000,
        help_text="CMSSW version",
        verbose_name="Online Version",
        null=True,
    )
    components = models.CharField(
        max_length=1000,
        help_text="List of subsystems included into the Run",
        verbose_name="Components",
        null=True,
    )
    delivered_lumi = models.FloatField(
        help_text="Integrated stable luminosity delivered by LHC",
        verbose_name="Delivered Lumi",
        null=True,
    )
    duration = models.PositiveIntegerField(
        help_text="Duration of the run", verbose_name="Duration", null=True
    )
    end_lumi = models.FloatField(
        help_text="Luminosity at the end of the run",
        verbose_name="Ending Lumi",
        null=True,
    )

    # end_time = models.DateTimeField(
    #     help_text="Time when the run was stopped", verbose_name="StopTime"
    # )

    energy = models.PositiveIntegerField(
        help_text="LHC energy", verbose_name="LHC Energy", null=True
    )
    fill_type_party1 = models.CharField(
        max_length=25,
        help_text="Fill Type Party 1",
        verbose_name="Fill Type Party 1",
        null=True,
    )
    fill_type_party2 = models.CharField(
        max_length=25,
        help_text="Fill Type Party 2",
        verbose_name="Fill Type Party 2",
        null=True,
    )
    fill_type_runtime = models.CharField(
        max_length=25, help_text="Fill type", verbose_name="Fill Type", null=True
    )
    hlt_key = models.CharField(
        max_length=256, help_text="HLT configuration key", verbose_name="HLT Key"
    )
    hlt_physics_counter = models.BigIntegerField(
        help_text="HLT triggers  for Physics streams",
        verbose_name="HLT Triggers Physics Streams",
        null=True,
    )
    hlt_physics_rate = models.FloatField(
        help_text="HLT rate for Physics streams",
        verbose_name="HLT Rate Physics Streams",
        null=True,
    )
    hlt_physics_size = models.FloatField(
        help_text="HLT size for Physics streams",
        verbose_name="HLT size Physics Streams",
        null=True,
    )
    hlt_physics_throughput = models.FloatField(
        help_text="HLT data rate for Physics streams",
        verbose_name="HLT Data Rate Physics Streams",
        null=True,
    )
    init_lumi = models.FloatField(
        help_text="Luminosity at the beginning of the run",
        verbose_name="Initial Lumi",
        null=True,
    )
    initial_prescale_index = models.PositiveIntegerField(
        help_text="Initial prescale index",
        verbose_name="Initial Prescale Index",
        null=True,
    )
    l1_hlt_mode = models.CharField(
        max_length=256,
        help_text="L1/HLT trigger mode",
        verbose_name="L1 HLT Mode",
        null=True,
    )
    l1_hlt_mode_stripped = models.CharField(
        max_length=256,
        help_text="L1/HLT trigger mode",
        verbose_name="L1 HLT Mode",
        null=True,
    )
    l1_key = models.CharField(
        max_length=256,
        help_text="L1 trigger configuration key",
        verbose_name="L1 Key",
        null=True,
    )
    l1_key_stripped = models.CharField(
        max_length=256,
        help_text="L1 trigger configuration key",
        verbose_name="L1 Key (Stripped)",
        null=True,
    )
    l1_menu = models.CharField(
        max_length=256, help_text="L1 menu name", verbose_name="L1 Menu", null=True
    )
    l1_rate = models.FloatField(help_text="L1 rate", verbose_name="L1 Rate", null=True)
    l1_triggers_counter = models.BigIntegerField(
        help_text="Number of L1 triggers", verbose_name="L1 Triggers", null=True
    )

    # last_update = models.DateTimeField(
    #     help_text="Time of last update of run table", verbose_name="last update"
    # )

    recorded_lumi = models.FloatField(
        help_text="Integrated stable luminosity recorded by CMS",
        verbose_name="Recorded Lumi",
        null=True,
    )

    sequence = models.CharField(
        max_length=4000, help_text="Run type", verbose_name="Sequence", null=True
    )
    stable_beam = models.BooleanField(
        help_text="Stable beam declared", verbose_name="StableBeamDeclared", null=True
    )

    # start_time = models.DateTimeField(
    #     help_text="Time when the run was started", verbose_name="StartTime"
    # )

    tier0_transfer = models.BooleanField(
        help_text="Transfer data to tier0", verbose_name="Tier0 Transfer", null=True
    )
    trigger_mode = models.CharField(
        max_length=256,
        help_text="Running mode of CMS",
        verbose_name="TriggerMode",
        null=True,
    )

    b_field_unit = models.CharField(max_length=50, default="T")
    init_lumi_unit = models.CharField(max_length=50, default="10^{34}cm^{-2}s^{-1}")
    delivered_lumi_unit = models.CharField(max_length=50, default="pb^{-1}")
    recorded_lumi_unit = models.CharField(max_length=50, default="pb^{-1}")
    end_lumi_unit = models.CharField(max_length=50, default="10^{34}cm^{-2}s^{-1}")
    energy_unit = models.CharField(max_length=50, default="GeV")

    def save(self, *args, **kwargs):
        physics_or_special = (
            "/cdaq/physics" in self.hlt_key or "/cdaq/special" in self.hlt_key
        )
        is_collisions = physics_or_special and self.stable_beam
        self.run_type = "collisions" if is_collisions else "cosmics"
        super(OmsRun, self).save(*args, **kwargs)
