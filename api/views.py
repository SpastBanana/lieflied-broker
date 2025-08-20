from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Tickets


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class TicketsView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tickets.objects.all()