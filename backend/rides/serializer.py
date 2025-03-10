# serializers.py
from rest_framework import serializers
from .models import Ride, RideEvent
from users.models import User
import datetime

class UserRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class GetRideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    rider = UserRideSerializer(read_only=True)
    driver = UserRideSerializer(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = '__all__'

    def get_todays_ride_events(self, obj):
        if hasattr(obj, "todays_events_cache"):
            return GetRideEventSerializer(obj.todays_events_cache, many=True).data
        return []

    
class GetRideSerializer(serializers.ModelSerializer):
    rider = UserRideSerializer(read_only=True)
    driver = UserRideSerializer(read_only=True)
    class Meta:
        model = Ride
        fields = '__all__'

class RideEventSerializer(serializers.ModelSerializer):
    ride = GetRideSerializer(read_only=True)
    class Meta:
        model = RideEvent
        fields = '__all__'

