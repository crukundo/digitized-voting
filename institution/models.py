from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_ec_officer = models.BooleanField(default=False)


class Faculty(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Election(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='elections')
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='elections')

    def __str__(self):
        return self.name


class Position(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')
    text = models.CharField('Position', max_length=255)

    def __str__(self):
        return self.text


class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    mugshot = models.ImageField(upload_to='candidates/', blank=True, null=True)
    full_name = models.CharField('Candidate full name', max_length=255)

    def __str__(self):
        return self.full_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    elections = models.ManyToManyField(Election, through='VotedElection')
    faculty = models.ManyToManyField(Faculty, related_name='student_faculty')
    email = models.EmailField(default=False, blank=True, null=True)
    mobile = models.CharField(blank=True, max_length=20, null=True)

    def get_unvoted_positions(self, election):
        voted_positions = self.election_candidate \
            .filter(candidate__position__election=election) \
            .values_list('candidate__position__pk', flat=True)
        positions = election.positions.exclude(pk__in=voted_positions).order_by('text')
        return positions

    def __str__(self):
        return self.user.username


class VotedElection(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='voted_elections')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='voted_elections')
    date = models.DateTimeField(auto_now_add=True)


class StudentVote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='election_candidate')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='+')
