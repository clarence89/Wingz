from rest_framework import viewsets
from users.models import User
from users.serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rides.permissions import IsAdminUser
from rides.pagination import ViewsetPagination

@swagger_auto_schema(tags=["Users"])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ViewsetPagination

@swagger_auto_schema(tags=["Users"])
class getAccountDetails(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
