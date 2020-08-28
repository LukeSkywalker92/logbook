from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from database.models import LogBook, LogBookEntry
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime

from .forms import EntryForm, NewLogBookForm, AddCollaboratorForm

# Create your views here.

class LibraryView(LoginRequiredMixin, TemplateView):
    template_name = 'library/library.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryView, self).get_context_data(*args, **kwargs)
        context['logbook_list'] = LogBook.objects.filter(collaborators__in=[self.request.user]).order_by('updated_date')
        context['form'] = NewLogBookForm()
        return context

class LogBookView(LoginRequiredMixin, TemplateView):
    template_name = 'library/logbook.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LogBookView, self).get_context_data(*args, **kwargs)
        context['logbook'] = get_object_or_404(LogBook,
                                               pk=self.kwargs['logbook_id'],
                                               collaborators__in=[self.request.user])
        context['form'] = EntryForm()
        return context

class CollaboratorsView(LoginRequiredMixin, TemplateView):
    template_name = 'library/owners.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CollaboratorsView, self).get_context_data(*args, **kwargs)
        logbook = get_object_or_404(LogBook,
                                 pk=self.kwargs['logbook_id'],
                                 owner=self.request.user)
        collaborators = logbook.collaborators.all()
        owner = logbook.owner
        context['owner'] = owner
        context['logbook'] = logbook        
        context['collaborators'] = collaborators
        context['not_collaborators'] = User.objects.all().difference(collaborators)
        context['form'] = AddCollaboratorForm()
        return context

class NewLogbookEntryView(LoginRequiredMixin ,View):

    def post(self, request, *args, **kwargs):
        logbook = get_object_or_404(LogBook,
                                 pk=self.kwargs['logbook_id'],
                                 collaborators__in=[request.user])
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = LogBookEntry(loogbook=logbook,
                                 author=request.user,
                                 text=form.cleaned_data['entry_text'])
            logbook.updated_date = datetime.datetime.now()
            logbook.save()
            entry.save()
            return HttpResponseRedirect('/library/'+str(logbook.id))
        else:
            return HttpResponseBadRequest()

class NewLogbookView(LoginRequiredMixin ,View):

    def post(self, request, *args, **kwargs):
        form = NewLogBookForm(self.request.POST)
        if form.is_valid():
            logbook = LogBook(name=form.cleaned_data['name'], owner=request.user)
            logbook.save()
            logbook.collaborators.add(request.user)
            logbook.save()
            return HttpResponseRedirect('/library/'+str(logbook.id))
        else:
            return HttpResponseBadRequest()

class RemoveCollaboratorView(LoginRequiredMixin ,View):

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(LogBook,
                                 pk=self.kwargs["logbook_id"],
                                 owner=request.user)
        user = get_object_or_404(User, username=self.kwargs["username"])
        book.collaborators.remove(user)
        book.save()
        return HttpResponseRedirect('/library/'+str(book.id)+'/collaborators')

class AddCollaboratorView(LoginRequiredMixin ,View):

    def add_collaborator(self, request, logbook_id, username):
        book = get_object_or_404(LogBook, pk=logbook_id, owner=request.user)
        user = get_object_or_404(User, username=username)
        book.collaborators.add(user)
        book.save()

    def get(self, request, *args, **kwargs):
        self.add_collaborator(request, self.kwargs["logbook_id"], self.kwargs["username"])
        return HttpResponseRedirect('/library/'+str(self.kwargs["logbook_id"])+'/collaborators')

    def post(self, request, *args, **kwargs):
        form = AddCollaboratorForm(request.POST)
        if form.is_valid():
            self.add_collaborator(request, self.kwargs["logbook_id"], form.cleaned_data['username'])
            return HttpResponseRedirect('/library/'+str(self.kwargs["logbook_id"])+'/collaborators')
        else:
            return HttpResponseBadRequest()