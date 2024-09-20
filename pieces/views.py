from django.shortcuts import render
from pieces.models import Piece, Comment, Rating
from profiles.models import Profile
from rest_framework import generics
from pieces.serializers import PieceSerializer, CommentSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

class PieceListView(generics.ListAPIView): 
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer

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