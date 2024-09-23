from rest_framework import serializers
from .models import MusicLog


class MusicLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicLog
        fields = '__all__'
