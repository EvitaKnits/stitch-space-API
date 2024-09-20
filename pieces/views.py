from django.shortcuts import render
from pieces.models import Piece, Comment, Rating
from profiles.models import Profile
from rest_framework import generics
from pieces.serializers import PieceSerializer, CommentSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated

class PieceListView(generics.ListAPIView): 
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer

class PieceCreateView(generics.CreateAPIView):
    serializer_class = PieceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the profile to the currently authenticated user
        serializer.save(profile=self.request.user.profile)

class CommentListView(generics.ListAPIView): 
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class RatingListView(generics.ListAPIView): 
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer