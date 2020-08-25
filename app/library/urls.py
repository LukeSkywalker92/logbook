from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name='library'),
    path('<int:logbook_id>/', views.logbook, name='logbook'),
    path('<int:logbook_id>/new_entry', views.new_entry, name='new_entry'),
    path('<int:logbook_id>/owners/', views.owners, name='owners'),
    path('new_logbook', views.new_logbook, name='new_logbook'),
    path('<int:logbook_id>/owners/remove/<str:username>', views.remove_owner, name='remove_owner'),
    path('<int:logbook_id>/owners/add_owner', views.add_owner, name='add_owner'),
    path('<int:logbook_id>/owners/add/<str:username>', views.add_owner_direct, name='add_owner_direct'),
]