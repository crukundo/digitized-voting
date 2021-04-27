from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import StudentFacultyForm, StudentSignUpForm, VoteForm
from ..models import Election, Student, VotedElection, User


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:election_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentFacultyView(UpdateView):
    model = Student
    form_class = StudentFacultyForm
    template_name = 'institution/students/faculty_form.html'
    success_url = reverse_lazy('students:election_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Faculties updated successfully!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class ElectionListView(ListView):
    model = Election
    ordering = ('name', )
    context_object_name = 'elections'
    template_name = 'institution/students/election_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_faculty = student.faculty.values_list('pk', flat=True)
        voted_elections = student.elections.values_list('pk', flat=True)
        queryset = Election.objects.filter(faculty__in=student_faculty) \
            .exclude(pk__in=voted_elections) \
            .annotate(positions_count=Count('positions')) \
            .filter(positions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class VotedElectionListView(ListView):
    model = VotedElection
    context_object_name = 'voted_elections'
    template_name = 'institution/students/voted_elections_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.voted_elections \
            .select_related('election', 'election__faculty') \
            .order_by('election__name')
        return queryset


@login_required
@student_required
def vote(request, pk):
    election = get_object_or_404(Election, pk=pk)
    student = request.user.student

    if student.elections.filter(pk=pk).exists():
        return render(request, 'students/voted_elections_list.html')

    total_positions = election.positions.count()
    unvoted_positions = student.get_unvoted_positions(election)
    total_unvoted_positions = unvoted_positions.count()
    progress = 100 - round(((total_unvoted_positions - 1) / total_positions) * 100)
    position = unvoted_positions.first()

    if request.method == 'POST':
        form = VoteForm(position=position, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_vote = form.save(commit=False)
                student_vote.student = student
                student_vote.save()
                if student.get_unvoted_positions(election).exists():
                    return redirect('students:vote', pk)
                else:
                    correct_answers = student.voted_elections.filter(candidate__position__election=election).count()
                    VotedElection.objects.create(student=student, election=election)
                    messages.success(request, 'Congratulations! You voted in the %s election successfully!' % (quiz.name))
                    return redirect('students:elections_list')
    else:
        form = VoteForm(position=position)

    return render(request, 'institution/students/vote_form.html', {
        'election': election,
        'position': position,
        'form': form,
        'progress': progress
    })
