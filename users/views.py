from django.shortcuts import render
from users.models import User
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class UserListView(LoginRequiredMixin, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer