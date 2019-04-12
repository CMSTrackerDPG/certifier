# Create fake entries

```python

import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

mixer.blend("oms.OmsFill")
mixer.blend("oms.OmsRun")
mixer.blend("oms.OmsRun")

mixer.blend("certifier.RunReconstruction")
my_run_certification = mixer.blend("certifier.TrackerCertification")
```