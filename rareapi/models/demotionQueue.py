from django.db import models


class DemotionQueue(models.Model):
    action = models.CharField(max_length=20)
    admin = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name="+")
    approver_one = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name="+")
