from django.contrib.auth.models import User
from django.db import models


class Comments(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.comment}'

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ('comment',)


class Company(models.Model):
    name = models.CharField(max_length=100)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    website = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company's"
        ordering = ('name',)

class Currency(models.Model):
    choices_lang = models.CharField(max_length=4, choices=('USD', 'EUR', 'BYR', 'UAH', 'RUB', 'PLN'))
    def __str__(self):
        return f'{self.choices_lang}'

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currency's"
        ordering = ('choices_lang',)

class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100)
    comments = models.CharField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancy's"
        ordering = ('title',)
class Emails(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    content = models.CharField(max_length=1024)
    sent_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ('subject',)

class Candidate(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    desired_salary = models.IntegerField(null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    resume_file = models.FileField(upload_to='resumes/')
    referred_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    applied_vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50)
    interview_date = models.DateTimeField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    cover_letter = models.CharField(max_length=1000, null=True, blank=True)
    source = models.URLField(null=True, blank=True)
    message = models.CharField(Emails, max_length=1000, null=True, blank=True)
    comments = models.CharField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"
        ordering = ('full_name','status', 'experience')

class Meetings(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField(User, related_name='meetings_attending')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings_organizing')
    participant = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='meetings_organizing')

    def __str__(self):
        return f'{self.title}, {self.date}, {self.participant}'

    class Meta:
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"
        ordering = ('title','date', 'location', 'participant')

class Notes(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    note = models.CharField(max_length=1024, null=True, blank=True)
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ('title',)

class SelectionStage(models.Model):
    name = models.CharField(max_length=100)


class Selection(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    stages = models.ManyToManyField(SelectionStage, through=SelectionStage(status))
    def __str__(self):
        return f'{self.vacancy}'

    class Meta:
        verbose_name = "Selection"
        verbose_name_plural = "Selection"
        ordering = ('candidate', 'vacancy', 'status', 'stages',)

class AppendLine(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    name_line = models.CharField(max_length=50)
    line = models.CharField(max_length=100)
