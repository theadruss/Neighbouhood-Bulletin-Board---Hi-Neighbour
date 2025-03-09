from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    # Add related_name to prevent conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )

    # ✅ Add a state field
    STATE_CHOICES = [
        ('KL', 'Kerala'),
        ('TN', 'Tamil Nadu'),
        ('KA', 'Karnataka'),
        ('AP', 'Andhra Pradesh'),
        ('MH', 'Maharashtra'),
        ('UP', 'Uttar Pradesh'),
        ('WB', 'West Bengal'),
        ('RJ', 'Rajasthan'),
        ('GJ', 'Gujarat'),
        # Add more states if needed
    ]

    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='KL')

    def __str__(self):
        return self.username


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Event', 'Event'),
        ('Alert', 'Alert'),
        ('Lost & Found', 'Lost & Found'),
        ('Important', 'Important'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # ✅ Image upload support

    def __str__(self):
        return self.title