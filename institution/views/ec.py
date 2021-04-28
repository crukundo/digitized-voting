from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import ec_official_required
from ..forms import BaseCandidateInlineFormSet, PositionForm, ECOfficerSignUpForm
from ..models import Candidate, Position, Election, User


class ECOfficerSignUpView(CreateView):
    model = User
    form_class = ECOfficerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'ec_officer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('ec:election_change_list')


@method_decorator([login_required, ec_official_required], name='dispatch')
class ElectionsListView(ListView):
    model = Election
    ordering = ('name', )
    context_object_name = 'elections'
    template_name = 'institution/ec/election_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.elections \
            .select_related('faculty') \
            .annotate(positions_count=Count('positions', distinct=True)) \
            .annotate(taken_count=Count('voted_elections', distinct=True))
        return queryset


@method_decorator([login_required, ec_official_required], name='dispatch')
class ElectionsCreateView(CreateView):
    model = Election
    fields = ('name', 'faculty', )
    template_name = 'institution/ec/election_add_form.html'

    def form_valid(self, form):
        election = form.save(commit=False)
        election.owner = self.request.user
        election.save()
        messages.success(self.request, 'The election was created successfully! Go ahead and add some positions now.')
        return redirect('ec:elections_change', election.pk)


@method_decorator([login_required, ec_official_required], name='dispatch')
class ElectionUpdateView(UpdateView):
    model = Election
    fields = ('name', 'faculty', )
    context_object_name = 'election'
    template_name = 'institution/ec/election_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['positions'] = self.get_object().positions.annotate(candidates_count=Count('candidates'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.elections.all()

    def get_success_url(self):
        return reverse('ec:elections_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, ec_official_required], name='dispatch')
class ElectionDeleteView(DeleteView):
    model = Election
    context_object_name = 'election'
    template_name = 'institution/ec/election_delete_confirm.html'
    success_url = reverse_lazy('ec:election_change_list')

    def delete(self, request, *args, **kwargs):
        election = self.get_object()
        messages.success(request, 'The election %s was deleted successfully!' % election.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.elections.all()


@method_decorator([login_required, ec_official_required], name='dispatch')
class ElectionResultsView(DetailView):
    model = Election
    context_object_name = 'election'
    template_name = 'institution/ec/election_results.html'

    def get_context_data(self, **kwargs):
        election = self.get_object()
        voted_elections = election.voted_elections.select_related('student__user').order_by('-date')
        total_voters = voted_elections.count()
        extra_context = {
            'voted_elections': voted_elections,
            'total_voters': total_voters,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.elections.all()


@login_required
@ec_official_required
def position_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    election = get_object_or_404(Election, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.election = election
            position.save()
            messages.success(request, 'You may now add candidates for this position.')
            return redirect('ec:position_change', election.pk, position.pk)
    else:
        form = PositionForm()

    return render(request, 'institution/ec/position_add_form.html', {'election': election, 'form': form})


@login_required
@ec_official_required
def position_change(request, election_pk, position_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    election = get_object_or_404(Election, pk=election_pk, owner=request.user)
    position = get_object_or_404(Position, pk=position_pk, election=election)

    CandidateFormSet = inlineformset_factory(
        Position,  # parent model
        Candidate,  # base model
        formset=BaseCandidateInlineFormSet,
        fields=('mugshot','full_name',),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        formset = CandidateFormSet(request.POST, instance=position)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Positions and their candidates saved successfully!')
            return redirect('ec:election_change', election.pk)
    else:
        form = PositionForm(instance=position)
        formset = CandidateFormSet(instance=position)

    return render(request, 'institution/ec/position_change_form.html', {
        'election': election,
        'position': position,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, ec_official_required], name='dispatch')
class PositionDeleteView(DeleteView):
    model = Position
    context_object_name = 'position'
    template_name = 'institution/ec/position_delete_confirm.html'
    pk_url_kwarg = 'position_pk'

    def get_context_data(self, **kwargs):
        position = self.get_object()
        kwargs['election'] = position.election
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        position = self.get_object()
        messages.success(request, 'The position %s was deleted successfully!' % position.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Position.objects.filter(election__owner=self.request.user)

    def get_success_url(self):
        position = self.get_object()
        return reverse('ec:election_change', kwargs={'pk': position.election_id})
