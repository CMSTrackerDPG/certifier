from rest_framework import serializers
from certifier.models import TrackerCertification, RunReconstruction
from oms.models import OmsRun


class RunReferenceRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackerCertification
        fields = ['runreconstruction', 'reference_runreconstruction']


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = OmsRun
        fields =  ['pk', 'run_number', 'run_type']