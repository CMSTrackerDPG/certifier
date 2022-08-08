import datetime

from mixer.backend.django import mixer


def create_runs(amount, first_run_number, runtype, reco, good=True, date=None):
    if runtype not in ["collisions", "cosmics"]:
        raise ValueError("Unknown run type: {}".format(runtype))
    if reco not in ["express", "prompt", "rereco"]:
        raise ValueError("Unknown reco type: {}".format(runtype))

    for i in range(first_run_number, first_run_number + amount):
        if runtype == "collisions":
            if good:
                if not date:
                    mixer.blend(
                        "certifier.TrackerCertification",
                        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=i, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
                        pixel="good",
                        strip="good",
                        tracking="good",
                    )
                else:
                    mixer.blend(
                        "certifier.TrackerCertification",
                        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=i, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
                        pixel="good",
                        strip="good",
                        tracking="good",
                        date=date
                    )

            else:
                if not date:
                    mixer.blend(
                        "certifier.TrackerCertification",
                        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=i, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
                        pixel="good",
                        strip="good",
                        tracking="bad",
                    )
                else:
                    mixer.blend(
                        "certifier.TrackerCertification",
                        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=i, run_type="collisions", hlt_key="/cdaq/physics", stable_beam=True)),
                        pixel="good",
                        strip="good",
                        tracking="bad",
                        date=date
                    )
        else:
            if good:
                if not date:
                    mixer.blend(
                        "certifier.TrackerCertification",
                        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=i, run_type="cosmics")),
                        pixel="good",
                        strip="good",
                        tracking="good",
                    )
                else:
                    mixer.blend(
                        "certifier.TrackerCertification",
                        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=i, run_type="cosmics")),
                        pixel="good",
                        strip="good",
                        tracking="good",
                        date=date
                    )
            else:
                if not date:
                    mixer.blend(
                        "certifier.TrackerCertification",
                        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=i, run_type="cosmics")),
                        pixel="good",
                        strip="good",
                        tracking="bad",
                    )
                else:
                    mixer.blend(
                        "certifier.TrackerCertification",
                        runreconstruction=mixer.blend("certifier.RunReconstruction", reconstruction=reco, run=mixer.blend("oms.OmsRun", run_number=i, run_type="cosmics")),
                        pixel="good",
                        strip="good",
                        tracking="bad",
                        date=date
                    )


def create_recent_run(run_number=None):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if not run_number:
        mixer.blend("certifier.TrackerCertification", date=today)
    else:
        mixer.blend("certifier.TrackerCertification", date=today, runreconstruction=mixer.blend("certifier.RunReconstruction", run=mixer.blend("oms.OmsRun", run_number=run_number)))
