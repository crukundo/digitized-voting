from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_ec_officer:
            return redirect('ec:election_change_list')
        else:
            return redirect('students:election_list')
    return render(request, 'institution/home.html')
