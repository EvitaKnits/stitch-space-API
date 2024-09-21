from django.shortcuts import render
from pieces.models import Piece, Comment, Rating
from profiles.models import Profile
from rest_framework import generics, filters
from pieces.serializers import PieceSerializer, CommentSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

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

class CommentListView(generics.ListAPIView): 
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class RatingListView(generics.ListAPIView): 
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer