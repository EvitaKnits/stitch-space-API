"""
URL configuration for stitch_space_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from profiles.views import (
    ProfileListView, ProfileRUDView, FollowerListView, 
    FollowerListByProfileView, FollowingListByProfileView, 
    FollowerCreateView, FollowerDeleteView
)
from notifications.views import NotificationListView, NotificationListByProfileView
from pieces.views import PieceListView, CommentListView, RatingListView, PieceCreateView, PieceRUDView
from .views import root_route, logout_route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profile/<int:id>/', ProfileRUDView.as_view(), name='profile-rud'),

    # Follower routes
    path('followers/', FollowerListView.as_view(), name='follower-list'),
    path('profile/<int:id>/followers/', FollowerListByProfileView.as_view(), name='profile-followers-list'),
    path('profile/<int:id>/followers/add/', FollowerCreateView.as_view(), name='profile-follow-add'),  # New POST route for adding followers
    path('profile/<int:id>/followers/remove/', FollowerDeleteView.as_view(), name='profile-follow-remove'),  # New DELETE route for removing followers
    path('profile/<int:id>/following/', FollowingListByProfileView.as_view(), name='profile-following-list'),
    
    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('profile/<int:id>/notifications/', NotificationListByProfileView.as_view(), name='profile-notifications-list'),

    # Pieces
    path('pieces/', PieceListView.as_view(), name='piece-list'),
    path('pieces/create/', PieceCreateView.as_view(), name='piece-create'),
    path('pieces/<int:id>/', PieceRUDView.as_view(), name='piece-rud'),

# Comments 
    path('comments/', CommentListView.as_view(), name='comment-list'),

# Ratings
    path('ratings/', RatingListView.as_view(), name='rating-list'),

    # Accounts
    path("accounts/", include("allauth.urls")),
]