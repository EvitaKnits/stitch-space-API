from django.shortcuts import render
from pieces.models import Piece, Comment, Rating
from profiles.models import Profile
from rest_framework import generics
from pieces.serializers import PieceSerializer, CommentSerializer, RatingSerializer

class PieceListView(generics.ListAPIView): 
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer

class CommentListView(generics.ListAPIView): 
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class RatingListView(generics.ListAPIView): 
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer