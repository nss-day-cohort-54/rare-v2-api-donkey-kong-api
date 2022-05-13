from django.db import models

class Subscription(models.Model):
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    created_on = models.DateField(auto_now=True)
    ended_on = models.DateField(auto_now=True)