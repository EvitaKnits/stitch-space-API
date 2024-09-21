from django.shortcuts import render
from pieces.models import Piece, Comment, Rating
from profiles.models import Profile
from rest_framework import generics, filters
from pieces.serializers import PieceSerializer, CommentSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

class PieceListView(generics.ListAPIView): 
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['art_type', 'profile__owner__id']
    search_fields = ['title', 'profile__owner__first_name', 'profile__owner__last_name']

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
        piece = Piece.objects.get(id=self.kwargs['id'])
        # For unsafe methods (PUT, PATCH, DELETE), ensure only the owner can modify or delete
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and piece.profile != self.request.user.profile:
            raise PermissionDenied("You do not have permission to edit or delete this piece.")
        return piece

class CommentListCreateView(generics.ListCreateAPIView): 
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        piece_id = self.kwargs['id']
        return Comment.objects.filter(piece__id=piece_id)

    def perform_create(self, serializer):
        piece_id = self.kwargs['id']
        piece = Piece.objects.get(id=piece_id)
        serializer.save(piece=piece, profile=self.request.user.profile)

class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['piece', 'profile']

class PieceRatingListCreateView(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        piece_id = self.kwargs['id']
        return Rating.objects.filter(piece__id=piece_id)

    def perform_create(self, serializer):
        piece_id = self.kwargs['id']
        piece = get_object_or_404(Piece, id=piece_id)
        profile = self.request.user.profile

        try:
            serializer.save(piece=piece, profile=profile)
        except IntegrityError:
            raise ValidationError("You have already rated this piece.")
        except ValidationError as e:
            raise ValidationError(e.detail)

class RatingRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        rating = get_object_or_404(Rating, id=self.kwargs['id'])
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if rating.profile != self.request.user.profile:
                raise PermissionDenied("You do not have permission to modify this rating.")
        return rating