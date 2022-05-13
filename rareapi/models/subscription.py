from django.db import models


class Subscription(models.Model):
    follower = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name="+")
    author = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name="+")
    created_on = models.DateField(auto_now=True)
    ended_on = models.DateField(auto_now=True)
