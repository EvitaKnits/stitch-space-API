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
    ProfileListView, ProfileRUDView, FollowerListByProfileView,
    FollowingListByProfileView, FollowerCreateView, FollowerDeleteView
)
from notifications.views import NotificationListByProfileView
from pieces.views import (
    PieceFeedListView, PieceListView, CommentListCreateView, RatingListView,
    PieceCreateView, PieceRUDView, RatingRUDView, PieceRatingListCreateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),

    # Profiles
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profile/<int:id>/', ProfileRUDView.as_view(), name='profile-rud'),

    # Followers
    path(
        'profile/<int:id>/followers/',
        FollowerListByProfileView.as_view(),
        name='profile-followers-list'
    ),
    path(
        'profile/<int:id>/followers/add/',
        FollowerCreateView.as_view(),
        name='profile-follow-add'
    ),
    path(
        'profile/<int:id>/followers/remove/',
        FollowerDeleteView.as_view(),
        name='profile-follow-remove'
    ),
    path(
        'profile/<int:id>/following/',
        FollowingListByProfileView.as_view(),
        name='profile-following-list'
    ),

    # Notifications
    path(
        'profile/<int:id>/notifications/',
        NotificationListByProfileView.as_view(),
        name='profile-notifications-list'
    ),

    # Pieces
    path('pieces/', PieceListView.as_view(), name='piece-list'),
    path('pieces/create/', PieceCreateView.as_view(), name='piece-create'),
    path('pieces/feed/', PieceFeedListView.as_view(), name='piece-list'),
    path('pieces/<int:id>/', PieceRUDView.as_view(), name='piece-rud'),
    path(
        'pieces/<int:id>/comments/',
        CommentListCreateView.as_view(),
        name='comment-list'
    ),

    # Ratings
    path('ratings/', RatingListView.as_view(), name='rating-list'),
    path(
        'ratings/<int:id>/',
        RatingRUDView.as_view(),
        name='rating-detail'
    ),
    path(
        'pieces/<int:id>/ratings/',
        PieceRatingListCreateView.as_view(),
        name='piece-ratings'
    ),

    # Accounts
    path("accounts/", include("allauth.urls")),
]
