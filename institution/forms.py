from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from institution.models import (Candidate, Position, Student, VotedElection,
                              Faculty, User)


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
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

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Please vote one of the candidates.', code='no_correct_answer')


class VoteForm(forms.ModelForm):
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = VotedElection
        fields = ('candidate', )

    def __init__(self, *args, **kwargs):
        position = kwargs.pop('position')
        super().__init__(*args, **kwargs)
        self.fields['candidate'].queryset = position.candidates.order_by('full_name')
