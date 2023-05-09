from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    website = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(max_length=300, null=True, blank=True)
    datatime_create = models.DateTimeField()
    datatime_update = models.DateTimeField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company's"
        ordering = ('name',)


class Currency(models.Model):
    choices_currency = models.CharField(max_length=4, choices=(('U', 'USD'), ('E', 'EUR'), ('B', 'BYR'), ('UA', 'UAH'),
                                                               ('R', 'RUB'), ('P', 'PLN')))

    def __str__(self):
        return f'{self.choices_currency}'

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currency's"
        ordering = ('choices_currency',)


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=1024)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=4, choices=(('U', 'USD'), ('E', 'EUR'), ('B', 'BYR'), ('UA', 'UAH'),
                                                       ('R', 'RUB'), ('P', 'PLN')))
    location = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(max_length=300, null=True, blank=True)
    open = models.BooleanField(default=True)
    datatime_create = models.DateTimeField()
    datatime_update = models.DateTimeField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"
        ordering = ('title', 'company', 'location')


class Emails(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.EmailField()
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1024)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ('title',)


class Candidate(models.Model):
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    desired_salary = models.IntegerField(null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    resume_file = models.FileField(upload_to='resumes/')
    referred_by = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50)
    interview_date = models.DateTimeField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    cover_letter = models.CharField(max_length=1000, null=True, blank=True)
    source = models.URLField(null=True, blank=True)
    message = models.ForeignKey(Emails, max_length=1000, null=True, blank=True, on_delete=models.CASCADE)
    sun_emails = models.IntegerField(null=True, blank=True)
    comments = models.CharField(max_length=300, null=True, blank=True)
    datatime_create = models.DateTimeField()
    datatime_update = models.DateTimeField()

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"
        ordering = ('full_name', 'status', 'experience', 'position', 'location')


class Meetings(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField(User, related_name='meetings_attending')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings_organizing')
    participant = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='meetings_organizing')
    datatime_create = models.DateTimeField()
    datatime_update = models.DateTimeField()

    def __str__(self):
        return f'{self.title}, {self.date}, {self.participant}'

    class Meta:
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"
        ordering = ('title', 'date', 'location', 'participant')


class Notes(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    note = models.CharField(max_length=1024, null=True, blank=True)
    datatime_create = models.DateTimeField()
    datatime_update = models.DateTimeField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ('title',)


class SelectionStage(models.Model):
    status = models.CharField(max_length=30, choices=(('R', 'Refusal'), ('NS', 'No stage'),
                                                      ('CS', 'Candidate Selection'), ('SI', 'Screening interview'),
                                                      ('I', 'Interview'), ('TI', 'Technical interview'), ('O', 'Offer'),
                                                      ('AO', 'Accepted offer'), ('EtW', 'Exit to work')))


class Selection(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    stages = models.ManyToManyField(SelectionStage)

    def __str__(self):
        return f'{self.vacancy}'

    class Meta:
        verbose_name = "Selection"
        verbose_name_plural = "Selection"
        ordering = ('candidate', 'vacancy', 'status')


class VacancyStage(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    stages = models.ManyToManyField(SelectionStage)

    def __str__(self):
        return f'{self.vacancy} - Stages'

    class Meta:
        verbose_name = "Vacancy Stage"
        verbose_name_plural = "Vacancy Stages"
        ordering = ('vacancy',)
