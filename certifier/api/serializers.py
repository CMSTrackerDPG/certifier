from rest_framework import serializers
from certifier.models import TrackerCertification


class RunReferenceRunSerializer(serializers.ModelSerializer):
    run_number = serializers.IntegerField(
        source='runreconstruction.run.run_number', read_only=True)
    run_reconstruction_type = serializers.CharField(
        source='runreconstruction.reconstruction', read_only=True)
    reference_run_number = serializers.IntegerField(
        source='reference_runreconstruction.run.run_number', read_only=True)
    reference_run_reconstruction_type = serializers.CharField(
        source='reference_runreconstruction.reconstruction', read_only=True)
    dataset = serializers.CharField(read_only=True)

    class Meta:
        model = TrackerCertification
        fields = [
            'run_number', 'run_reconstruction_type', 'reference_run_number',
            'reference_run_reconstruction_type', 'dataset'
        ]
