from django.shortcuts import render
from notifications.models import Notification
from rest_framework import generics
from notifications.serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer
