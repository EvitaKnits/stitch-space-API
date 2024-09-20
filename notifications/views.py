from django.shortcuts import render
from notifications.models import Notification
from rest_framework import generics
from notifications.serializers import NotificationSerializer
from profiles.models import Profile
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

class NotificationListView(generics.ListAPIView):
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer

class NotificationListByProfileView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_queryset(self):
        # Get the profile_id from the URL
        profile_id = self.kwargs.get('id')

        # Ensure the profile exists
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

        # Filter the notifications for the given profile (as recipient)
        return Notification.objects.filter(recipient=profile).order_by('-created_at')