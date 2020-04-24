from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import UserViewSet, ClientViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('user', ClientViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
