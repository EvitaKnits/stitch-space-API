from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 
    """ 
    Custom user model extending Django's AbstractUser.
    Adds image and biography, art type, last visited 
    notifications, created at and updated at fields.
    """
    ART_TYPES = (
        ('knitting', 'Knitting'),
        ('crochet', 'Crochet'), 
        ('embroidery', 'Embroidery'),
        ('weaving', 'Weaving'),
        ('dyeing', 'Dyeing'), 
        ('other', 'Other')
    )

    email = models.EmailField(unique=True)
    biography = models.TextField(blank=True)
    art_type = models.CharField(
        max_length=20, choices=ART_TYPES, blank=True
    )
    last_visited_notifications = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        """
        Return the string representation of the user, which is the username.
        """
        return self.username


