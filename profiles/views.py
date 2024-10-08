from django.shortcuts import render
from profiles.models import Profile, Follower
from notifications.models import Notification
from django.contrib.auth.models import User
from rest_framework import generics, status, filters
from profiles.serializers import ProfileSerializer, FollowerSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.http import Http404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend


class ProfileListView(generics.ListAPIView):
    """
    API view to list profiles with annotations for followers, followed profiles
    and pieces counts. Supports ordering by any field using Django REST
    Framework's OrderingFilter, with a default ordering by ID.
    """
    queryset = Profile.objects.annotate(
        followed_count=Count("followed", distinct=True),
        follower_count=Count("follower", distinct=True),
        pieces_count=Count("creator", distinct=True),
    )
    serializer_class = ProfileSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
    ordering = ["id"]


class ProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific profile.
    Ensures only the owner of the profile can update or delete it.
    Annotates the profile with follower, followed, and pieces counts.
    """
    queryset = Profile.objects.annotate(
        followed_count=Count("followed", distinct=True),
        follower_count=Count("follower", distinct=True),
        pieces_count=Count("creator", distinct=True),
    )
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        # Get the user ID from the URL kwargs
        id = self.kwargs.get("id")

        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Restrict access to the user's own profile
            if str(id) != str(self.request.user.id):
                raise PermissionDenied(
                    "You are not allowed to access this profile."
                )

        # Retrieve the profile of the user with the given ID
        try:
            return Profile.objects.annotate(
                followed_count=Count("followed", distinct=True),
                follower_count=Count("follower", distinct=True),
                pieces_count=Count("creator", distinct=True),
            ).get(owner__id=id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")


class FollowerListByProfileView(generics.ListAPIView):
    """
    API view to list all followers of a specific profile.
    Supports filtering and ordering. Raises a 404 if the profile does not exist
    Passes the context to indicate this is a follower-only view.
    """
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["follower__owner_id"]
    ordering_fields = "__all__"
    ordering = ["id"]

    def get_queryset(self):
        # Get the profile_id from the URL
        id = self.kwargs.get("id")

        # Check if the profile exists, raise 404 if not found
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

        # Return the queryset of followers for the given profile
        return Follower.objects.filter(followed_profile=profile)

    def get_serializer_context(self):
        # Pass context to serializer to indicate this is a follower-only view
        context = super().get_serializer_context()
        context["view_type"] = "followers_only"
        return context


class FollowingListByProfileView(generics.ListAPIView):
    """
    API view to list all profiles that a specific profile is following.
    Supports ordering and raises a 404 if the profile does not exist.
    Passes the context to indicate this is a following-only view.
    """
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
    ordering = ["id"]

    def get_queryset(self):
        # Get the profile_id from the URL
        profile_id = self.kwargs.get("id")

        # Check if the profile exists, raise 404 if not found
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

        # Return the queryset of profiles that the given profile is following
        return Follower.objects.filter(follower=profile)

    def get_serializer_context(self):
        # Pass context to serializer to indicate this is a following-only view
        context = super().get_serializer_context()
        context["view_type"] = "following_only"
        return context


class FollowerCreateView(generics.CreateAPIView):
    """
    API view to list all profiles that a specific profile is following.
    Supports ordering and raises a 404 if the profile does not exist.
    Passes the context to indicate this is a following-only view.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer

    def post(self, request, *args, **kwargs):
        # Get the profile_id from the URL
        profile_id = self.kwargs.get("id")

        # Get the profile to be followed
        try:
            followed_profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

        # Prevent users following themselves
        if request.user.profile == followed_profile:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the current user is already following this profile
        if Follower.objects.filter(
            follower=request.user.profile, followed_profile=followed_profile
        ).exists():
            return Response(
                {"detail": "You are already following this profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new Follower instance
        Follower.objects.create(
            follower=request.user.profile, followed_profile=followed_profile
        )

        # Create notification if the actor is not the recipient
        if request.user.profile != followed_profile:
            Notification.objects.create(
                actor=request.user.profile,
                recipient=followed_profile,
                interaction_type="follow",
            )

        return Response(
            {"detail": "You are now following this profile."},
            status=status.HTTP_201_CREATED,
        )


class FollowerDeleteView(generics.DestroyAPIView):
    """
    API view to unfollow a specific profile.
    Ensures the user is following the profile before deleting the follow
    relationship. Returns a 404 if the user is not following the profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer

    def delete(self, request, *args, **kwargs):
        # Get the profile_id and follower_id from the URL
        profile_id = self.kwargs.get("id")

        # Get the profile that the current user is following
        try:
            followed_profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

        # Try to find the following relationship
        try:
            follow_relationship = Follower.objects.get(
                follower=request.user.profile,
                followed_profile=followed_profile
            )
        except Follower.DoesNotExist:
            return Response(
                {"detail": "You are not following this profile."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the follow relationship
        follow_relationship.delete()

        return Response(
            {"detail": "You have unfollowed this profile."},
            status=status.HTTP_204_NO_CONTENT,
        )
