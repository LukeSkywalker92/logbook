from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name='library'),
    path('logbook/<int:logbook_id>/', views.logbook, name='logbook'),
    path('logbook/<int:logbook_id>/new_entry', views.new_entry, name='new_entry'),
    path('new_logbook', views.new_logbook, name='new_logbook'),
]