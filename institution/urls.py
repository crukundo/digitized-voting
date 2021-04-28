from django.urls import include, path

from .views import institution, students, ec

urlpatterns = [
    path('', institution.home, name='home'),

    path('students/', include(([
        path('', students.ElectionListView.as_view(), name='election_list'),
        path('faculty/', students.StudentFacultyView.as_view(), name='student_faculty'),
        path('taken/', students.VotedElectionListView.as_view(), name='voted_elections_list'),
        path('election/<int:pk>/', students.vote, name='vote'),
    ], 'institution'), namespace='students')),

    path('ec/', include(([
        path('', ec.ElectionsListView.as_view(), name='election_change_list'),
        path('election/add/', ec.ElectionsCreateView.as_view(), name='election_add'),
        path('election/<int:pk>/', ec.ElectionUpdateView.as_view(), name='election_change'),
        path('election/<int:pk>/delete/', ec.ElectionDeleteView.as_view(), name='election_delete'),
        path('election/<int:pk>/results/', ec.ElectionResultsView.as_view(), name='election_results'),
        path('election/<int:pk>/position/add/', ec.position_add, name='position_add'),
        path('election/<int:election_pk>/position/<int:position_pk>/', ec.position_change, name='position_change'),
        path('election/<int:election_pk>/position/<int:position_pk>/delete/', ec.PositionDeleteView.as_view(), name='position_delete'),
    ], 'institution'), namespace='ec')),
]
