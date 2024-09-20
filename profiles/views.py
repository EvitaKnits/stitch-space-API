from django.shortcuts import render
from profiles.models import Profile, Follower
from rest_framework import generics, status
from profiles.serializers import ProfileSerializer, FollowerSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
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

class FollowingListByProfileView(generics.ListAPIView): 
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Get the profile_id from the URL
        profile_id = self.kwargs.get('id')

        # Check if the profile exists, raise 404 if not found
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

        # Return the queryset of profiles that the given profile is following
        return Follower.objects.filter(follower=profile)

    def get_serializer_context(self):
        # Pass context to the serializer to indicate this is a following-only view
        context = super().get_serializer_context()
        context['view_type'] = 'following_only'
        return context

class FollowerCreateView(generics.CreateAPIView): 
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer

    def post(self, request, *args, **kwargs):
        # Get the profile_id from the URL
        profile_id = self.kwargs.get('id')
        
        # Get the profile to be followed
        try:
            followed_profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")
        
        # Check if the current user is already following this profile
        if Follower.objects.filter(follower=request.user.profile, followed_profile=followed_profile).exists():
            return Response({"detail": "You are already following this profile."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Follower instance
        Follower.objects.create(follower=request.user.profile, followed_profile=followed_profile)
        
        return Response({"detail": "You are now following this profile."}, status=status.HTTP_201_CREATED)

class FollowerDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer 

    def delete(self, request, *args, **kwargs):
        # Get the profile_id and follower_id from the URL
        profile_id = self.kwargs.get('id')
        
        # Get the profile that the current user is following
        try:
            followed_profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")
            
        # Try to find the following relationship
        try:
            follow_relationship = Follower.objects.get(follower=request.user.profile, followed_profile=followed_profile)
        except Follower.DoesNotExist:
            return Response({"detail": "You are not following this profile."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the follow relationship
        follow_relationship.delete()

        return Response({"detail": "You have unfollowed this profile."}, status=status.HTTP_204_NO_CONTENT)