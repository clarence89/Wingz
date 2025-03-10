from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ride, RideEvent
from .serializer import RideSerializer, RideEventSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import F, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Radians, Sin, Cos, ACos
from .permissions import IsAdminUser
from .pagination import ViewsetPagination
from django.db import connection

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
    def get_queryset(self):
        queryset = super().get_queryset()

        # A very chatGPT generated solution. I don't know the formula, then search to chatGPT
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

            try:
                queryset = queryset.annotate(distance=ExpressionWrapper(distance_expr, output_field=FloatField())).order_by('distance')
            except Exception as e:
                logger.error(
                    "An error occurred while ordering queryset by distance. "
                    "Error message : %s" % e
                )
                raise e
        for query in connection.queries:
            print(query['sql'])
        print(queryset.query) 
        return queryset

@swagger_auto_schema(tags=["RideEvents"])
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ViewsetPagination
