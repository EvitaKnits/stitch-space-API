from django.shortcuts import render
from profiles.models import Profile, Follower
from rest_framework import generics
from profiles.serializers import ProfileSerializer, FollowerSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class FollowerListView(generics.ListAPIView): 
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer