from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name='library'),
    path('logbook/<int:logbook_id>/', views.logbook, name='logbook'),
    path('logbook/<int:logbook_id>/new_entry', views.new_entry, name='new_entry'),
    path('logbook/<int:logbook_id>/owners', views.owners, name='owners'),
    path('new_logbook', views.new_logbook, name='new_logbook'),
    path('logbook/<int:logbook_id>/owners/remove/<str:username>', views.remove_owner, name='remove_owner'),
    path('logbook/<int:logbook_id>/add_owner', views.add_owner, name='add_owner'),
]