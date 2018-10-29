from rest_framework import serializers

from .models import TimeReport

class TimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeReport
        fields = '__all__'
