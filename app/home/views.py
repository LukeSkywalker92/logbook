from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name= 'home/home.html'

@login_required
def home(request):
    return render(request, 'home/home.html')