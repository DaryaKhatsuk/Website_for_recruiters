from django.db import models
from django.contrib.auth.models import User


class AccountVerif(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, label='Code')
    state_acc = models.CharField(max_length=4, choices=(('A', 'Active'), ('U', 'Unverified'), ('B', 'Blocked')))


class SaveLocation(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    selecting = models.CharField(max_length=12, label='Selecting', choices=(('D', 'On device'), ('S', 'On server')))
    location = models.CharField(max_length=255, label='Location', null=True, blank=True)


class Language(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=3, label='Language', choices=(('EN', 'English'), ('RU', 'Русский')))
