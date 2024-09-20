from django.db import models
from profiles.models import Profile
from pieces.models import Piece

class Notification(models.Model): 
    """
    Model to represent profile interactions with pieces and profiles. 
    Each instance records a specific interaction with a specific
    piece or profile.
    """
    INTERACTION_TYPES = (
        ('comment', 'Comment'),
        ('rating', 'Rating'),
        ('follow', 'Follow')
    )

    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, null=True, blank=True)
    actor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notification_sender')
    recipient = models.ForeignKey (Profile, on_delete=models.CASCADE, related_name='notification_receiver')
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
        
        # Access the actor's first name through the `owner` relationship (which is the User model)
        actor_first_name = self.actor.owner.first_name

        if self.interaction_type == 'follow':
            return f"{actor_first_name} {interaction_display} you"
        else:
            piece_title = self.piece.title
            return f"{actor_first_name} {interaction_display} '{piece_title}'"
