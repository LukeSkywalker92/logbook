from django.urls import path
from . import views
from library.views import LibraryView, LogBookView, OwnersView, NewLogbookEntryView, NewLogbookView, RemoveOwnerView, AddOwnerView

app_name = 'library'

urlpatterns = [
    path('', LibraryView.as_view(), name='index'),
    path('<int:logbook_id>/', LogBookView.as_view(), name='logbook'),
    path('<int:logbook_id>/new_entry', NewLogbookEntryView.as_view(), name='new_entry'),
    path('<int:logbook_id>/owners/', OwnersView.as_view(), name='owners'),
    path('new_logbook', NewLogbookView.as_view(), name='new_logbook'),
    path('<int:logbook_id>/owners/remove/<str:username>', RemoveOwnerView.as_view(), name='remove_owner'),
    path('<int:logbook_id>/owners/add_owner', AddOwnerView.as_view(), name='add_owner'),
    path('<int:logbook_id>/owners/add/<str:username>', AddOwnerView.as_view(), name='add_owner_direct'),
]