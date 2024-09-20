from django.shortcuts import render
from profiles.models import Profile, Follower
from rest_framework import generics
from profiles.serializers import ProfileSerializer, FollowerSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.http import Http404

class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

def get_object(self):
        # Get the user ID from the URL kwargs
        id = self.kwargs.get('id')

        # Restrict access to the user's own profile
        if str(id) != str(self.request.user.id):
            raise PermissionDenied("You are not allowed to access this profile.")

        # Retrieve the profile of the user with the given ID
        try:
            return Profile.objects.get(owner__id=id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

class FollowerListView(generics.ListAPIView): 
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

class FollowerListByProfileView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Get the profile_id from the URL
        id = self.kwargs.get('id')

        # Check if the profile exists, raise 404 if not found
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

        # Return the queryset of followers for the given profile
        return Follower.objects.filter(followed_profile=profile)

    def get_serializer_context(self):
        # Pass context to the serializer to indicate this is a follower-only view
        context = super().get_serializer_context()
        context['view_type'] = 'followers_only'
        return context