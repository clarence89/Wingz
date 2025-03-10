from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from django.db.models import Prefetch, F, Value, FloatField, ExpressionWrapper
from .models import Ride, RideEvent
from .serializer import RideSerializer, RideEventSerializer, RideQuerySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import F, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Radians, Sin, Cos, ACos
from .permissions import IsAdminUser
from .pagination import ViewsetPagination
from django.db import connection
from django.utils.timezone import now

from .filters import RideFilter
import logging
logger = logging.getLogger(__name__)


@swagger_auto_schema(tags=["Rides"])
class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ViewsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time', 'distance']  
    ordering = ['pickup_time']

    @swagger_auto_schema(
        query_serializer=RideQuerySerializer, 
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        today = now().date()
        queryset = super().get_queryset()

        queryset = queryset.select_related("rider", "driver")

        queryset = queryset.prefetch_related(
            Prefetch(
                "ride_events",
                queryset=RideEvent.objects.filter(created_at__date=today),
                to_attr="todays_events_cache",
            )
        )

        user_latitude = self.request.query_params.get('latitude')
        user_longitude = self.request.query_params.get('longitude')
        if user_latitude and user_longitude:
            try:
                user_latitude = float(user_latitude)
                user_longitude = float(user_longitude)
            except ValueError:
                logger.error("Invalid latitude or longitude format.")
                raise ValueError("Invalid latitude or longitude format.")

            lat_diff = Radians(F('pickup_latitude')) - Radians(Value(user_latitude))
            lon_diff = Radians(F('pickup_longitude')) - Radians(Value(user_longitude))

            distance_expr = ACos(Sin(lat_diff) * Sin(lat_diff) + Cos(lat_diff) * Cos(lat_diff) * Cos(lon_diff)) * 6371
            queryset = queryset.annotate(
                distance=ExpressionWrapper(distance_expr, output_field=FloatField())
            ).order_by('distance')
        # Checked and it is only Two
        print(f"Total Queries Executed: {len(connection.queries)}")
        return queryset


@swagger_auto_schema(tags=["RideEvents"])
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ViewsetPagination
