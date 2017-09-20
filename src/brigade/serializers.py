from rest_framework import serializers

from worker.serializers import WorkerProfileSerializer

from .models import Brigade


class BrigadeSerializer(serializers.ModelSerializer):
    workers = serializers.SerializerMethodField()

    class Meta:
        model = Brigade
        fields = (
            'id',
            'name',
            'workers',
        )

    def get_workers(self, obj):
        return WorkerProfileSerializer(obj.worker_set, many=True).data
