from django.contrib.auth.models import User
from django.db import models
from filebrowser.fields import FileBrowseField


class AccountVerif(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    state_acc = models.CharField(max_length=12, choices=(('A', 'Active'), ('U', 'Unverified'), ('B', 'Blocked')))

    class Meta:
        verbose_name = "AccountVerif"
        verbose_name_plural = "AccountVerif"
        ordering = ('state_acc',)


class AccountDirectory(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    directory = FileBrowseField('Directory', max_length=255)

    class Meta:
        verbose_name = "AccountDirectory"
        verbose_name_plural = "AccountDirectory"
        ordering = ('directory',)


class Language(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=3, choices=(('EN', 'English'), ('RU', 'Русский')))

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ('language',)
