from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from database.models import LogBook, LogBookEntry
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EntryForm, NewLogBookForm, AddOwnerForm

# Create your views here.

class LibraryView(LoginRequiredMixin, TemplateView):
    template_name = 'library/library.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryView, self).get_context_data(*args, **kwargs)
        context['logbook_list'] = LogBook.objects.filter(owners__in=[self.request.user])
        context['form'] = NewLogBookForm()
        return context

class LogBookView(LoginRequiredMixin, TemplateView):
    template_name = 'library/logbook.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LogBookView, self).get_context_data(*args, **kwargs)
        context['logbook'] = get_object_or_404(LogBook,
                                               pk=self.kwargs['logbook_id'],
                                               owners__in=[self.request.user])
        context['form'] = EntryForm()
        return context

class OwnersView(LoginRequiredMixin, TemplateView):
    template_name = 'library/owners.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OwnersView, self).get_context_data(*args, **kwargs)
        logbook = get_object_or_404(LogBook,
                                 pk=self.kwargs['logbook_id'],
                                 owners__in=[self.request.user])
        owners = logbook.owners.all()
        context['logbook'] = logbook        
        context['owners'] = owners
        context['not_owners'] = User.objects.all().difference(owners)
        context['form'] = AddOwnerForm()
        return context

class NewLogbookEntryView(LoginRequiredMixin ,View):

    def post(self, request, *args, **kwargs):
        logbook = get_object_or_404(LogBook,
                                 pk=self.kwargs['logbook_id'],
                                 owners__in=[request.user])
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = LogBookEntry(loogbook=logbook,
                                 author=request.user,
                                 text=form.cleaned_data['entry_text'])
            entry.save()
            return HttpResponseRedirect('/library/'+str(logbook.id))
        else:
            return HttpResponseBadRequest()

class NewLogbookView(LoginRequiredMixin ,View):

    def post(self, request, *args, **kwargs):
        form = NewLogBookForm(self.request.POST)
        if form.is_valid():
            logbook = LogBook(name=form.cleaned_data['name'])
            logbook.save()
            logbook.owners.add(request.user)
            logbook.save()
            return HttpResponseRedirect('/library/'+str(logbook.id))
        else:
            return HttpResponseBadRequest()

class RemoveOwnerView(LoginRequiredMixin ,View):

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(LogBook,
                                 pk=self.kwargs["logbook_id"],
                                 owners__in=[request.user])
        user = get_object_or_404(User, username=self.kwargs["username"])
        book.owners.remove(user)
        book.save()
        return HttpResponseRedirect('/library/'+str(book.id)+'/owners')

class AddOwnerView(LoginRequiredMixin ,View):

    def add_owner(self, request, logbook_id, username):
        book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
        user = get_object_or_404(User, username=username)
        book.owners.add(user)
        book.save()

    def get(self, request, *args, **kwargs):
        self.add_owner(request, self.kwargs["logbook_id"], self.kwargs["username"])
        return HttpResponseRedirect('/library/'+str(self.kwargs["logbook_id"])+'/owners')

    def post(self, request, *args, **kwargs):
        form = AddOwnerForm(request.POST)
        if form.is_valid():
            self.add_owner(request, self.kwargs["logbook_id"], form.cleaned_data['username'])
            return HttpResponseRedirect('/library/'+str(self.kwargs["logbook_id"])+'/owners')
        else:
            return HttpResponseBadRequest()