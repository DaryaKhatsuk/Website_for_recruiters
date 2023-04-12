from django.db import models
from django.contrib.auth.models import User


class AccountVerif(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, label='Code')
