from django.shortcuts import render
from users.models import User, Follower
from rest_framework import generics
from users.serializers import UserSerializer, FollowerSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# class UserListView(LoginRequiredMixin, generics.ListAPIView):
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FollowerListView(generics.ListAPIView): 
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer