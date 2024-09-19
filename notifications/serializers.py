from notifications.models import Notification
from pieces.models import Piece
from profiles.models import Profile
from rest_framework import serializers

class NotificationSerializer(serializers.ModelSerializer): 
    piece = serializers.PrimaryKeyRelatedField(queryset=Piece.objects.all())
    actor = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    recipient = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    interactionType = serializers.CharField(source='interaction_type')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta: 
        model = Notification
        fields = [
            'id', 'piece', 'actor', 'recipient', 'interactionType', 'createdAt'
        ]