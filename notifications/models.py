from django.db import models
from users.models import User
from pieces.models import Piece

class Notification(models.Model): 
    """
    Model to represent user interactions with pieces and users. 
    Each instance records a specific interaction with a specific
    piece or user.
    """
    INTERACTION_TYPES = (
        ('comment', 'Comment'),
        ('rating', 'Rating'),
        ('follow', 'Follow')
    )

    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, null=True, blank=True)
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_sender')
    recipient = models.ForeignKey (User, on_delete=models.CASCADE, related_name='notification_receiver')
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        Return a human-readable string representation of the notification.
        """
        # Map the interaction types to human-readable verbs
        interaction_verbs = {
            'comment': 'commented on',
            'rating': 'rated',
            'follow': 'followed'
        }

        # Get the verb corresponding to the interaction type 
        interaction_display = interaction_verbs[self.interaction_type]
        piece_title = self.piece.title

        if self.interaction_type == 'follow':
            return f"{self.actor.first_name} {interaction_display} you"
        else: 
            return f"{self.actor.first_name} {interaction_display} '{piece_title}'"
