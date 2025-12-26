from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Mood(models.Model) : 
    MOOD_CHOICES = [
        ('happy' , 'happy') , 
        ('sad' , 'sad') , 
        ('angry' , 'angry')
    ]

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    mood = models.CharField(choices=MOOD_CHOICES)
    note = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
