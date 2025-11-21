from django.db import models
from django.contrib.auth.models import User   # ✅ import User for linking

class Property(models.Model):
    PROPERTY_TYPES = [
        ('AP', 'Apartment'),
        ('VI', 'Villa'),
        ('FL', 'Flat'),
        ('PL', 'Plot'),
        ('CO', 'Commercial'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=2, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=200)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    area = models.IntegerField(help_text="Area in sq ft")
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    # ✅ NEW FIELD — user who created this property
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # If user is deleted, keep the property
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
