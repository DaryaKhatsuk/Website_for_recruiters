from django.db import models
from django.contrib.auth.models import User


class AccountVerif(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, label='Code')
    state_acc = models.CharField(max_length=12, choices=('Active', 'Unverified', 'Blocked'))

    class Meta:
        verbose_name = "AccountVerif"
        verbose_name_plural = "AccountVerif"
        ordering = ('state_acc',)


class SaveLocation(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    selecting = models.CharField(max_length=12, label='Selecting', choices=(('D', 'On device'), ('S', 'On server')))
    location = models.CharField(max_length=255, label='Location', null=True, blank=True)

    class Meta:
        verbose_name = "SaveLocation"
        verbose_name_plural = "SaveLocations"
        ordering = ('selecting',)


class Language(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=3, label='Language', choices=(('EN', 'English'), ('RU', 'Русский')))

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ('language',)
