from django.shortcuts import render
from notifications.models import Notification
from rest_framework import generics, filters
from notifications.serializers import NotificationSerializer
from profiles.models import Profile
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


class NotificationListByProfileView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']

    def get_queryset(self):
        # Get the profile_id from the URL
        profile_id = self.kwargs.get('id')

        # Ensure the profile exists
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

        # Filter the notifications for the given profile (as recipient)
        return Notification.objects.filter(
            recipient=profile
        ).order_by('-created_at')


class NotificationCreateView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        The notification is triggered programmatically, so handles the creation
        with the required fields passed in.
        """
        # No sender field added directly here because it's triggered elsewhere
        serializer.save()
