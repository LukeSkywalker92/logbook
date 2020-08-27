from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from database.models import LogBook, LogBookEntry
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
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

@login_required
def new_entry(request, logbook_id):
    book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
    form = EntryForm(request.POST)
    if form.is_valid():
        entry = LogBookEntry(loogbook=book, author=request.user, text=form.cleaned_data['entry_text'])
        entry.save()
    return HttpResponseRedirect('/library/'+str(logbook_id))

@login_required
def new_logbook(request):
    form = NewLogBookForm(request.POST)
    if form.is_valid():
        logbook = LogBook(name=form.cleaned_data['name'])
        logbook.save()
        logbook.owners.add(request.user)
        logbook.save()
        return HttpResponseRedirect('/library/'+str(logbook.id))

@login_required
def remove_owner(request, logbook_id, username):
    book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
    user = get_object_or_404(User, username=username)
    book.owners.remove(user)
    book.save()
    return HttpResponseRedirect('/library/'+str(book.id)+'/owners')
    #return HttpResponse(status=200)

@login_required
def add_owner(request, logbook_id):
    form = AddOwnerForm(request.POST)
    if form.is_valid():
        book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
        user = get_object_or_404(User, username=form.cleaned_data['username'])
        book.owners.add(user)
        book.save()
        return HttpResponseRedirect('/library/'+str(book.id)+'/owners')

@login_required
def add_owner_direct(request, logbook_id, username):
    book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
    user = get_object_or_404(User, username=username)
    book.owners.add(user)
    book.save()
    return HttpResponseRedirect('/library/'+str(book.id)+'/owners')