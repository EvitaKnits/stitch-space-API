from django.shortcuts import render
from pieces.models import Piece, Comment, Rating
from profiles.models import Profile, Follower
from notifications.models import Notification
from rest_framework import generics, filters
from pieces.serializers import PieceSerializer, CommentSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Avg, Q, Count, Subquery, OuterRef, FloatField


class PieceFeedListView(generics.ListAPIView):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer

    def get_queryset(self):
        # Get the profile of the currently authenticated user
        user_profile = Profile.objects.get(owner=self.request.user)

        # Get the profiles that the current user is following
        followed_profiles = Follower.objects.filter(follower=user_profile).values_list(
            "followed_profile", flat=True
        )

        # Filter the Piece queryset to return pieces created by the followed profiles
        return Piece.objects.annotate(
            avg_rating=Avg("rating__score", default=0),
        ).filter(profile__in=followed_profiles)


class PieceListView(generics.ListAPIView):
    queryset = Piece.objects.annotate(
        avg_rating=Avg("rating__score", default=0), comments=Count("comment")
    )
    serializer_class = PieceSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["art_type", "profile__owner__id", "featured"]
    search_fields = ["title", "profile__owner__first_name", "profile__owner__last_name"]
    ordering_fields = "__all__"
    ordering = ["-created_at"]


class PieceCreateView(generics.CreateAPIView):
    serializer_class = PieceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the profile to the currently authenticated user
        serializer.save(profile=self.request.user.profile)


class PieceRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PieceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):

        user_profile = Profile.objects.get(owner=self.request.user)

        # Get the profiles that the current user is following
        followed_profiles = Follower.objects.filter(follower=user_profile).values_list(
            "followed_profile", flat=True
        )

        # Filter the Piece queryset to return pieces created by the followed profiles
        piece = Piece.objects.annotate(
            avg_rating=Avg("rating__score", default=0),
        ).get(id=self.kwargs["id"])

        # Retrieve the user's rating for this piece (if it exists)
        try:
            user_rating = Rating.objects.get(profile=user_profile, piece=piece)
        except Rating.DoesNotExist:
            user_rating = None  # If the user hasn't rated the piece yet

        # For unsafe methods (PUT, PATCH, DELETE), ensure only the owner can modify or delete
        if (
            self.request.method in ["PUT", "PATCH", "DELETE"]
            and piece.profile != self.request.user.profile
        ):
            raise PermissionDenied(
                "You do not have permission to edit or delete this piece."
            )
        piece.user_rating = user_rating
        return piece


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
    ordering = ["-created_at"]

    def get_queryset(self):
        piece_id = self.kwargs["id"]
        return Comment.objects.filter(piece__id=piece_id)

    def perform_create(self, serializer):
        piece_id = self.kwargs["id"]
        piece = Piece.objects.get(id=piece_id)
        serializer.save(piece=piece, profile=self.request.user.profile)

        # Create notification if the piece belongs to someone else
        if piece.profile != self.request.user.profile:
            Notification.objects.create(
                piece=piece,
                actor=self.request.user.profile,
                recipient=piece.profile,
                interaction_type="comment",
            )


class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["piece", "profile"]


class PieceRatingListCreateView(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["profile__owner__id"]

    def get_queryset(self):
        piece_id = self.kwargs["id"]
        return Rating.objects.filter(piece__id=piece_id)

    def perform_create(self, serializer):
        piece_id = self.kwargs["id"]
        piece = get_object_or_404(Piece, id=piece_id)
        profile = self.request.user.profile

        try:
            rating = serializer.save(piece=piece, profile=profile)

            # Create notification if the piece belongs to someone else
            if piece.profile != self.request.user.profile:
                Notification.objects.create(
                    piece=piece,
                    actor=self.request.user.profile,
                    recipient=piece.profile,
                    interaction_type="rating",
                )

        except IntegrityError:
            raise ValidationError("You have already rated this piece.")
        except ValidationError as e:
            raise ValidationError(e.detail)


class RatingRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        rating = get_object_or_404(Rating, id=self.kwargs["id"])
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            if rating.profile != self.request.user.profile:
                raise PermissionDenied(
                    "You do not have permission to modify this rating."
                )
        return rating
