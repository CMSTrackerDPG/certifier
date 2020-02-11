# Translation of old field to new fields:

This page gives an overview of how the fields from the TkDQMDoctor have looked like in the old certification helper website and how the are called in the new version.

```python
translations = {
	'RunInfo.userid' : 'TrackerCertification.user',
	'RunInfo.type.reco'  : 'TrackerCertification.runreconstruction.reconstruction',
	'RunInfo.type.runtype' : "TrackerCertification.runreconstruction.run.run_type",
	'RunInfo.type.bfield' : "TrackerCertification.runreconstruction.run.b_field",
	'RunInfo.type.beamtype' : "TrackerCertification.runreconstruction.run.fill_type_party1",
	'RunInfo.type.beamenergy' : "TrackerCertification.runreconstruction.run.energy",
	'RunInfo.type.dataset' : "TrackerCertification.runreconstruction.dataset",
	'RunInfo.reference_run.reference_run' : "TrackerCertification.reference_runreconstruction.run.run_number",
	'RunInfo.reference_run.reco' : "TrackerCertification.reference_runreconstruction.reconstruction",
	'RunInfo.reference_run.runtype' : "TrackerCertification.reference_runreconstruction.run.run_type",
	'RunInfo.reference_run.bfield' : "TrackerCertification.reference_runreconstruction.run.b_field",
	'RunInfo.reference_run.beamtype' : "TrackerCertification.reference_runreconstruction.run.fill_type_party1",
	'RunInfo.reference_run.beamenergy' : "TrackerCertification.reference_runreconstruction.run.energy",
	'RunInfo.reference_run.dataset' : "TrackerCertification.reference_runreconstruction.dataset",
	'RunInfo.run_number' : "TrackerCertification.runreconstruction.run.run_number",
	'RunInfo.number_of_ls' : "TrackerCertification.runreconstruction.run.lumisections",
	'RunInfo.int_luminosity' : "TrackerCertification.runreconstruction.run.recorded_lumi",
	'RunInfo.pixel' : "TrackerCertification.pixel",
	'RunInfo.pixel_lowstat' : "TrackerCertification.pixel_lowstat",
	'RunInfo.sistrip' : "TrackerCertification.strip",
	'RunInfo.sistrip_lowstat' : "TrackerCertification.strip_lowstat",
	'RunInfo.tracking' : "TrackerCertification.tracking",
	'RunInfo.tracking_lowstat' : "TrackerCertification.tracking_lowstat",
	'RunInfo.comment' : "TrackerCertification.comment",
	'RunInfo.date' : "TrackerCertification.date",
}
```

**Important Note**:

```RunInfo.type.beamtype``` now consists of two fields:
 - ```TrackerCertification.runreconstruction.run.fill_type_party1```
 - ```TrackerCertification.runreconstruction.run.fill_type_party2```


```RunInfo.reference_run.beamtype``` now consists of two fields:
 - ```TrackerCertification.reference_runreconstruction.run.fill_type_party1```
 - ```TrackerCertification.reference_runreconstruction.run.fill_type_party2```

* For cosmics data ```fill_type_party1``` and ```fill_type_party1``` have to manually overwritten/displayed as ```cosmics``` to make it consistent with the previous site.
* ```PB``` has to be manually displayed as ```HeavyIon``` to make it consistent.

```RunInfo.int_luminosity``` now consists of two fields:
 - ```TrackerCertification.runreconstruction.recorded_lumi```
 - ```TrackerCertification.runreconstruction.recorded_lumi_unit```

When summing up the integrated luminosity it hast to be grouped recorded_lumi_unit first. 

```RunInfo.type.beamenergy``` now consists of two fields:
 - ```TrackerCertification.runreconstruction.run.energy```
 - ```TrackerCertification.runreconstruction.run.energy_unit```

## Testing it

in new site:

```python
from certifier.models import TrackerCertification
run = TrackerCertification.objects.all().first()
for key, value in translations.items():
    print("{} \t{}".format(key,eval(value.replace("TrackerCertification", "run"))))
```

in old site:

```python
for key, value in translations.items():
    print("{} \t{}".format(key, eval(key.replace("RunInfo", "run"))))    
    
```
