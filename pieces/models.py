from django.db import models
from profiles.models import Profile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Piece(models.Model):
    """
    This model represents a Piece with various attributes, which
    belongs to a User Profile.
    """

    ART_TYPES = (
        ('knitting', 'Knitting'),
        ('crochet', 'Crochet'),
        ('embroidery', 'Embroidery'),
        ('weaving', 'Weaving'),
        ('dyeing', 'Dyeing'),
        ('other', 'Other')
    )

    title = models.CharField(max_length=75, null=False)
    image = models.URLField(max_length=1024, 
                            default='https://picsum.photos/id/1/800/600')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='creator')
    art_type = models.CharField(max_length=20, choices=ART_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)


class Comment(models.Model):
    """
    This model represents a Comment made on a Piece by a User Profile.
    """

    content = models.TextField()
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    """
    This model represents a Rating given to a Piece by a User Profile.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Adds a constraint so that a profile only rates a piece once.
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'piece'],
                name='unique_rating'
            )
        ]

    def clean(self):
        """
        Custom validation to prevent a user from rating their own piece.
        """
        if self.piece.profile == self.profile:
            raise ValidationError("You cannot rate your own piece.")

    def save(self, *args, **kwargs):
        # Calls the clean method to ensure validation
        self.clean()
        super().save(*args, **kwargs)
