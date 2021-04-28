from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from institution.models import (Candidate, Position, Student, VotedElection, StudentVote, Faculty, User)


class ECOfficerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_ec_officer = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email address", required=False)
    mobile = forms.CharField(label="Mobile number", required=False)
    faculty = forms.ModelMultipleChoiceField(
        queryset=Faculty.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.faculty.add(*self.cleaned_data.get('faculty'))
        return user


class StudentFacultyForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('faculty', )
        widgets = {
            'faculty': forms.CheckboxSelectMultiple
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('text', )


class BaseCandidateInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()


class VoteForm(forms.ModelForm):
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None,
        label="Candidates", 
        help_text="Select your desired candidate and hit next")

    class Meta:
        model = StudentVote
        fields = ('candidate', )

    def __init__(self, *args, **kwargs):
        position = kwargs.pop('position')
        super().__init__(*args, **kwargs)
        self.fields['candidate'].queryset = position.candidates.order_by('full_name')
