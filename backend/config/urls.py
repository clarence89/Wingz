"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from drf_yasg import openapi
from users.views import getAccountDetails
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from rides.views import RideViewSet, RideEventViewSet


...

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"rides", RideViewSet, basename="ride")
router.register(r"ride_events", RideEventViewSet, basename="ride_event")
urlpatterns = [
    path(r"auth/", include("trench.urls")),  
    path(r"auth/", include("trench.urls.jwt")),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "account/details",
        getAccountDetails.as_view(),
        name="ipaddresses-scan",
    ),
    path("api/", include(router.urls)),
    path("", admin.site.urls),

    # path("redoc/", schema_view.with_ui("redoc",
    # ^^ cache_timeout=0), name="schema-redoc"),
]
