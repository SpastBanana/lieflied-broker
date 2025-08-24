from django.contrib import admin
from django.urls import path, include
from api.views import TicketsView, TicketStatsView, TicketEdit
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/user/register/', CreateUserView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/tickets/', TicketsView.as_view(), name="tickets-API"),
    path('api/tickets/stats/', TicketStatsView.as_view(), name="ticket-stats-API"),
    path('api/tickets/edit/<int:id>/', TicketEdit.as_view(), name="ticket-stats-API"),
]
