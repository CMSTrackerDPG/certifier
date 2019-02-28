# Generated by Django 2.1.7 on 2019-02-27 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OmsFill",
            fields=[
                (
                    "fill_number",
                    models.PositiveIntegerField(
                        help_text="Fill number",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="Fill",
                    ),
                ),
                (
                    "b_field",
                    models.FloatField(
                        help_text="Magnetic field", null=True, verbose_name="B Field"
                    ),
                ),
                (
                    "beta_star",
                    models.FloatField(help_text="β*", null=True, verbose_name="β*"),
                ),
                (
                    "bunches_beam1",
                    models.PositiveIntegerField(
                        help_text="Number of bunches beam 1",
                        null=True,
                        verbose_name="Bunches Beam1",
                    ),
                ),
                (
                    "bunches_beam2",
                    models.PositiveIntegerField(
                        help_text="Number of bunches beam 2",
                        null=True,
                        verbose_name="Bunches Beam2",
                    ),
                ),
                (
                    "bunches_colliding",
                    models.PositiveIntegerField(
                        help_text="Number of colliding bunches measured by CMS",
                        null=True,
                        verbose_name="nCollidingBunches",
                    ),
                ),
                (
                    "bunches_target",
                    models.PositiveIntegerField(
                        help_text="Target number of colliding bunches by LHC configuration",
                        null=True,
                        verbose_name="nTargetBunches",
                    ),
                ),
                (
                    "crossing_angle",
                    models.FloatField(
                        help_text="Crossing angle by LHC configuration",
                        null=True,
                        verbose_name="Crossing Angle",
                    ),
                ),
                (
                    "delivered_lumi",
                    models.FloatField(
                        help_text="Integrated stable luminosity delivered by LHC",
                        null=True,
                        verbose_name="Delivered Lumi",
                    ),
                ),
                (
                    "downtime",
                    models.PositiveIntegerField(
                        help_text="Total downtime during the Fill",
                        null=True,
                        verbose_name="Downtime",
                    ),
                ),
                (
                    "duration",
                    models.PositiveIntegerField(
                        help_text="Duration of the Fill",
                        null=True,
                        verbose_name="Duration",
                    ),
                ),
                (
                    "efficiency_lumi",
                    models.FloatField(
                        help_text="The efficiency calculated by luminosity",
                        null=True,
                        verbose_name="Efficiency by Luminosity",
                    ),
                ),
                (
                    "efficiency_time",
                    models.FloatField(
                        help_text="The efficiency calculated by time",
                        null=True,
                        verbose_name="Efficiency by Time",
                    ),
                ),
                (
                    "energy",
                    models.FloatField(
                        help_text="LHC target energy", null=True, verbose_name="Energy"
                    ),
                ),
                (
                    "era",
                    models.CharField(
                        help_text="Era Name",
                        max_length=40,
                        null=True,
                        verbose_name="Era",
                    ),
                ),
                (
                    "fill_type_party1",
                    models.CharField(
                        help_text="Fill Type Party 1",
                        max_length=25,
                        null=True,
                        verbose_name="Fill Type Party 1",
                    ),
                ),
                (
                    "fill_type_party2",
                    models.CharField(
                        help_text="Fill Type Party 2",
                        max_length=25,
                        null=True,
                        verbose_name="Fill Type Party 2",
                    ),
                ),
                (
                    "fill_type_runtime",
                    models.CharField(
                        help_text="Fill type",
                        max_length=25,
                        null=True,
                        verbose_name="Fill Type",
                    ),
                ),
                (
                    "init_lumi",
                    models.FloatField(
                        help_text="Luminosity at the beginning of the fill",
                        null=True,
                        verbose_name="InitialLumi",
                    ),
                ),
                (
                    "injection_scheme",
                    models.CharField(
                        help_text="Injection scheme",
                        max_length=100,
                        null=True,
                        verbose_name="Injection scheme",
                    ),
                ),
                (
                    "intensity_beam1",
                    models.FloatField(
                        help_text="Beam 1 peak intensity",
                        null=True,
                        verbose_name="IntensityBeam1",
                    ),
                ),
                (
                    "intensity_beam2",
                    models.FloatField(
                        help_text="Beam 2 peak intensity",
                        null=True,
                        verbose_name="IntensityBeam2",
                    ),
                ),
                (
                    "peak_lumi",
                    models.FloatField(
                        help_text="Peak of instantaneous luminosity during the fill",
                        null=True,
                        verbose_name="PeakLumi",
                    ),
                ),
                (
                    "peak_pileup",
                    models.FloatField(
                        help_text="Peak pileup",
                        null=True,
                        verbose_name="PeakPileup (interactions/BX)",
                    ),
                ),
                (
                    "peak_specific_lumi",
                    models.FloatField(
                        help_text="Peak value of average specific luminosity ",
                        null=True,
                        verbose_name="PeakSpecificLumi",
                    ),
                ),
                (
                    "recorded_lumi",
                    models.FloatField(
                        help_text="Integrated stable luminosity recorded by CMS",
                        null=True,
                        verbose_name="Recorded Lumi",
                    ),
                ),
                ("b_field_unit", models.CharField(max_length=50)),
                ("peak_lumi_unit", models.CharField(max_length=50)),
                ("beta_star_unit", models.CharField(max_length=50)),
                ("init_lumi_unit", models.CharField(max_length=50)),
                ("peak_specific_lumi_unit", models.CharField(max_length=50)),
                ("intensity_beam2_unit", models.CharField(max_length=50)),
                ("intensity_beam1_unit", models.CharField(max_length=50)),
                ("delivered_lumi_unit", models.CharField(max_length=50)),
                ("recorded_lumi_unit", models.CharField(max_length=50)),
                ("crossing_angle_unit", models.CharField(max_length=50)),
                ("energy_unit", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="OmsRun",
            fields=[
                (
                    "run_number",
                    models.PositiveIntegerField(
                        help_text="Run number",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="Run",
                    ),
                ),
                (
                    "run_type",
                    models.CharField(
                        choices=[("collisions", "Collisions"), ("cosmics", "Cosmics")],
                        max_length=3,
                    ),
                ),
                ("lumisections", models.PositiveIntegerField()),
                (
                    "b_field",
                    models.FloatField(
                        help_text="Magnetic field", null=True, verbose_name="B Field"
                    ),
                ),
                (
                    "clock_type",
                    models.CharField(
                        help_text="Clock type",
                        max_length=4000,
                        null=True,
                        verbose_name="Clock type",
                    ),
                ),
                (
                    "cmssw_version",
                    models.CharField(
                        help_text="CMSSW version",
                        max_length=4000,
                        null=True,
                        verbose_name="Online Version",
                    ),
                ),
                (
                    "components",
                    models.CharField(
                        help_text="List of subsystems included into the Run",
                        max_length=1000,
                        null=True,
                        verbose_name="Components",
                    ),
                ),
                (
                    "delivered_lumi",
                    models.FloatField(
                        help_text="Integrated stable luminosity delivered by LHC",
                        null=True,
                        verbose_name="Delivered Lumi",
                    ),
                ),
                (
                    "duration",
                    models.PositiveIntegerField(
                        help_text="Duration of the run",
                        null=True,
                        verbose_name="Duration",
                    ),
                ),
                (
                    "end_lumi",
                    models.FloatField(
                        help_text="Luminosity at the end of the run",
                        null=True,
                        verbose_name="Ending Lumi",
                    ),
                ),
                (
                    "energy",
                    models.PositiveIntegerField(
                        help_text="LHC energy", null=True, verbose_name="LHC Energy"
                    ),
                ),
                (
                    "fill_type_party1",
                    models.CharField(
                        help_text="Fill Type Party 1",
                        max_length=25,
                        null=True,
                        verbose_name="Fill Type Party 1",
                    ),
                ),
                (
                    "fill_type_party2",
                    models.CharField(
                        help_text="Fill Type Party 2",
                        max_length=25,
                        null=True,
                        verbose_name="Fill Type Party 2",
                    ),
                ),
                (
                    "fill_type_runtime",
                    models.CharField(
                        help_text="Fill type",
                        max_length=25,
                        null=True,
                        verbose_name="Fill Type",
                    ),
                ),
                (
                    "hlt_key",
                    models.CharField(
                        help_text="HLT configuration key",
                        max_length=256,
                        verbose_name="HLT Key",
                    ),
                ),
                (
                    "hlt_physics_counter",
                    models.PositiveIntegerField(
                        help_text="HLT triggers  for Physics streams",
                        null=True,
                        verbose_name="HLT Triggers Physics Streams",
                    ),
                ),
                (
                    "hlt_physics_rate",
                    models.FloatField(
                        help_text="HLT rate for Physics streams",
                        null=True,
                        verbose_name="HLT Rate Physics Streams",
                    ),
                ),
                (
                    "hlt_physics_size",
                    models.FloatField(
                        help_text="HLT size for Physics streams",
                        null=True,
                        verbose_name="HLT size Physics Streams",
                    ),
                ),
                (
                    "hlt_physics_throughput",
                    models.FloatField(
                        help_text="HLT data rate for Physics streams",
                        null=True,
                        verbose_name="HLT Data Rate Physics Streams",
                    ),
                ),
                (
                    "init_lumi",
                    models.FloatField(
                        help_text="Luminosity at the beginning of the run",
                        null=True,
                        verbose_name="Initial Lumi",
                    ),
                ),
                (
                    "initial_prescale_index",
                    models.PositiveIntegerField(
                        help_text="Initial prescale index",
                        null=True,
                        verbose_name="Initial Prescale Index",
                    ),
                ),
                (
                    "l1_hlt_mode",
                    models.CharField(
                        help_text="L1/HLT trigger mode",
                        max_length=256,
                        null=True,
                        verbose_name="L1 HLT Mode",
                    ),
                ),
                (
                    "l1_hlt_mode_stripped",
                    models.CharField(
                        help_text="L1/HLT trigger mode",
                        max_length=256,
                        null=True,
                        verbose_name="L1 HLT Mode",
                    ),
                ),
                (
                    "l1_key",
                    models.CharField(
                        help_text="L1 trigger configuration key",
                        max_length=256,
                        null=True,
                        verbose_name="L1 Key",
                    ),
                ),
                (
                    "l1_key_stripped",
                    models.CharField(
                        help_text="L1 trigger configuration key",
                        max_length=256,
                        null=True,
                        verbose_name="L1 Key (Stripped)",
                    ),
                ),
                (
                    "l1_menu",
                    models.CharField(
                        help_text="L1 menu name",
                        max_length=256,
                        null=True,
                        verbose_name="L1 Menu",
                    ),
                ),
                (
                    "l1_rate",
                    models.FloatField(
                        help_text="L1 rate", null=True, verbose_name="L1 Rate"
                    ),
                ),
                (
                    "l1_triggers_counter",
                    models.PositiveIntegerField(
                        help_text="Number of L1 triggers",
                        null=True,
                        verbose_name="L1 Triggers",
                    ),
                ),
                (
                    "recorded_lumi",
                    models.FloatField(
                        help_text="Integrated stable luminosity recorded by CMS",
                        null=True,
                        verbose_name="Recorded Lumi",
                    ),
                ),
                (
                    "sequence",
                    models.CharField(
                        help_text="Run type",
                        max_length=4000,
                        null=True,
                        verbose_name="Sequence",
                    ),
                ),
                (
                    "stable_beam",
                    models.BooleanField(
                        help_text="Stable beam declared",
                        null=True,
                        verbose_name="StableBeamDeclared",
                    ),
                ),
                (
                    "tier0_transfer",
                    models.BooleanField(
                        help_text="Transfer data to tier0",
                        null=True,
                        verbose_name="Tier0 Transfer",
                    ),
                ),
                (
                    "trigger_mode",
                    models.CharField(
                        help_text="Running mode of CMS",
                        max_length=256,
                        null=True,
                        verbose_name="TriggerMode",
                    ),
                ),
                ("b_field_unit", models.CharField(max_length=50)),
                ("init_lumi_unit", models.CharField(max_length=50)),
                ("delivered_lumi_unit", models.CharField(max_length=50)),
                ("recorded_lumi_unit", models.CharField(max_length=50)),
                ("end_lumi_unit", models.CharField(max_length=50)),
                ("energy_unit", models.CharField(max_length=50)),
                (
                    "fill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="oms.OmsFill"
                    ),
                ),
            ],
        ),
    ]
