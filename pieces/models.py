from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Piece(models.Model): 
    """
    This model represents a Piece with various attributes, which
    belongs to a User.
    """

    ART_TYPES = (
        ('knitting', 'Knitting'),
        ('crochet', 'Crochet'), 
        ('embroidery', 'Embroidery'),
        ('weaving', 'Weaving'),
        ('dyeing', 'Dyeing'), 
        ('other', 'Other')
    )

    title = models.CharField(max_length=150, null=False)
    # image = models.ImageField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_type = models.CharField(max_length=20, choices=ART_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model): 
    """
    This model represents a Comment made on a Piece by a User.
    """

    content = models.TextField()
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    """
    This model represents a Rating given to a Piece by a User.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        # Adds a constraint so that a user only rates a piece once.
        constraints = [
            models.UniqueConstraint(fields=['user', 'piece'], name='unique_rating')
        ]
    
    def clean(self):
        """
        Custom validation to prevent a user from rating their own piece.
        """
        if self.piece.user == self.user:
            raise ValidationError("You cannot rate your own piece.")
    
    def save(self, *args, **kwargs):
        # Calls the clean method to ensure validation
        self.clean()
        super().save(*args, **kwargs)