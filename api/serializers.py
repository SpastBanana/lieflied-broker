from django.contrib.auth.models import User
from .models import Tickets
from rest_framework import serializers
    

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = '__all__'


class TicketStatsSerializer(serializers.Serializer):
    tickets_ordered = serializers.CharField()
    tickets_payed = serializers.CharField()
    tickets_sum = serializers.CharField()
    amount_ordered = serializers.CharField()
    amount_payed = serializers.CharField()
    amount_sum = serializers.CharField()