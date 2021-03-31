from rest_framework import serializers
from certifier.models import TrackerCertification, RunReconstruction
from oms.models import OmsRun


class RunReferenceRunSerializer(serializers.ModelSerializer):
    run_number = serializers.SerializerMethodField()
    reference_run_number = serializers.SerializerMethodField()

    class Meta:
        model = TrackerCertification
        fields = ['run_number', 'reference_run_number']
    
    def get_run_number(self, obj):
        return obj.run_number
    
    def get_reference_run_number(self, obj):
        return obj.reference_run_number


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = OmsRun
        fields =  ['run_number', 'run_type']


class RunReconstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunReconstruction
        fields =  '__all__'