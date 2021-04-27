from django.urls import include, path

from .views import institution, students, teachers

urlpatterns = [
    path('', institution.home, name='home'),

    path('students/', include(([
        path('', students.ElectionListView.as_view(), name='election_list'),
        path('faculty/', students.StudentFacultyView.as_view(), name='student_faculty'),
        path('taken/', students.VotedElectionListView.as_view(), name='voted_elections_list'),
        path('election/<int:pk>/', students.vote, name='vote'),
    ], 'institution'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.ElectionsListView.as_view(), name='election_change_list'),
        path('election/add/', teachers.ElectionsCreateView.as_view(), name='election_add'),
        path('election/<int:pk>/', teachers.ElectionUpdateView.as_view(), name='election_change'),
        path('election/<int:pk>/delete/', teachers.ElectionDeleteView.as_view(), name='election_delete'),
        path('election/<int:pk>/results/', teachers.ElectionResultsView.as_view(), name='election_results'),
        path('election/<int:pk>/position/add/', teachers.position_add, name='position_add'),
        path('election/<int:election_pk>/position/<int:position_pk>/', teachers.position_change, name='position_change'),
        path('election/<int:election_pk>/position/<int:position_pk>/delete/', teachers.PositionDeleteView.as_view(), name='position_delete'),
    ], 'institution'), namespace='teachers')),
]
