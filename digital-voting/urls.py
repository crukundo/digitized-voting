from django.urls import include, path

from institution.views import institution, students, ec

urlpatterns = [
    path('', include('institution.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', institution.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/ec/', ec.ECOfficerSignUpView.as_view(), name='ec_signup'),
]
