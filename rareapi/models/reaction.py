from django.db import models

class Reaction(models.Model):
    label = models.CharField(max_length=35)
    image_url = models.TextField()
    