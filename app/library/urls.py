from django.urls import path
from . import views
from library.views import LibraryView, LogBookView, CollaboratorsView, NewLogbookEntryView, NewLogbookView, RemoveCollaboratorView, AddCollaboratorView

app_name = 'library'

urlpatterns = [
    path('', LibraryView.as_view(), name='index'),
    path('<int:logbook_id>/', LogBookView.as_view(), name='logbook'),
    path('<int:logbook_id>/new_entry', NewLogbookEntryView.as_view(), name='new_entry'),
    path('<int:logbook_id>/collaborators/', CollaboratorsView.as_view(), name='collaborators'),
    path('new_logbook', NewLogbookView.as_view(), name='new_logbook'),
    path('<int:logbook_id>/collaborators/remove/<str:username>', RemoveCollaboratorView.as_view(), name='remove_collaborator'),
    path('<int:logbook_id>/collaborators/add_collaborator', AddCollaboratorView.as_view(), name='add_collaborator'),
    path('<int:logbook_id>/collaborators/add/<str:username>', AddCollaboratorView.as_view(), name='add_collaborator_direct'),
]