from django.urls import path
from . import views
from library.views import LibraryView, LogBookView, OwnersView

app_name = 'library'

urlpatterns = [
    path('', LibraryView.as_view(), name='index'),
    path('<int:logbook_id>/', LogBookView.as_view(), name='logbook'),
    path('<int:logbook_id>/new_entry', views.new_entry, name='new_entry'),
    path('<int:logbook_id>/owners/', OwnersView.as_view(), name='owners'),
    path('new_logbook', views.new_logbook, name='new_logbook'),
    path('<int:logbook_id>/owners/remove/<str:username>', views.remove_owner, name='remove_owner'),
    path('<int:logbook_id>/owners/add_owner', views.add_owner, name='add_owner'),
    path('<int:logbook_id>/owners/add/<str:username>', views.add_owner_direct, name='add_owner_direct'),
]