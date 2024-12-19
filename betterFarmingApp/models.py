from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils.timezone import now

class Plant(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    rainfall = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name


class PlantImage(models.Model):
    plant = models.ForeignKey(Plant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='plant_images/')

    def __str__(self):
        return f"Image for {self.plant.name}"
    


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=50)
    rainfall = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # New field

    def __str__(self):
        return self.username



class Testimonial(models.Model):
    reviewer = models.CharField(max_length=100, default='Anonymous')
    reviewerid = models.IntegerField(null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    date_sent = models.DateTimeField(default=now)  # Timestamp of the testimonial
    profile_image = models.ImageField(upload_to='profile_image/',blank=True, null=True,default='./static/img/noProfile.png')
    # Removed image field because it will be dynamically fetched from the user's profile

    def __str__(self):
        return self.reviewer
