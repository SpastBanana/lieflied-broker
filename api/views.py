from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TicketSerializer, TicketStatsSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Tickets


class TicketsView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tickets.objects.all()
    
class TicketDelete(generics.DestroyAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tickets.objects.all()
    

class TicketStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats_data = calculate_ticket_stats()

        serializer = TicketStatsSerializer(data=stats_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_ticket_stats():
    list_payed = Tickets.objects.filter(has_payed='1').values()
    list_unpayed = Tickets.objects.filter(has_payed='0').values()
    total_payed_amount, total_payed_count, total_unpayed_amount, total_unpayed_count = 0,0,0,0

    if len(list_payed) != 0:
        for order in list_payed:
            order_payed_amount = float(order['total_amount'].replace(',', '.'))
            total_payed_amount += order_payed_amount
            order_payed_count = int(order['ticket_count'])
            total_payed_count += order_payed_count

    if len(list_unpayed) != 0:
        for order in list_unpayed:
            order_unpayed_amount = float(order['total_amount'].replace(',', '.'))
            total_unpayed_amount += order_unpayed_amount
            order_unpayed_count = int(order['ticket_count'])
            total_unpayed_count += order_unpayed_count

    data = {
        'tickets_ordered': str(total_unpayed_count),
        'tickets_payed': str(total_payed_count),
        'tickets_sum': str(total_unpayed_count + total_payed_count),
        'amount_ordered': "{:.2f}".format(total_unpayed_amount).replace('.', ','),
        'amount_payed': "{:.2f}".format(total_payed_amount).replace('.', ','),
        'amount_sum': "{:.2f}".format(total_unpayed_amount + total_payed_amount).replace('.', ','),
    }

    return data