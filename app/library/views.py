from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from database.models import LogBook, LogBookEntry
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import EntryForm, NewLogBookForm, AddOwnerForm

# Create your views here.

@login_required
def library(request):
    logbook_list = LogBook.objects.filter(owners__in=[request.user])
    form = NewLogBookForm()
    context = {
        'logbook_list': logbook_list,
        'form': form
        }
    return render(request, 'library/library.html', context)

@login_required
def logbook(request, logbook_id):
    book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
    form = EntryForm()
    context = {
        'logbook': book,
        'form':form
        }
    return render(request, 'library/logbook.html', context)

@login_required
def owners(request, logbook_id):
    book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
    owners = book.owners.all()
    not_owners = User.objects.all().difference(owners)
    print(not_owners)
    form = AddOwnerForm()
    context = {
        'logbook': book,
        'owners':owners,
        'not_owners': not_owners,
        'form':form
        }
    return render(request, 'library/owners.html', context)

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