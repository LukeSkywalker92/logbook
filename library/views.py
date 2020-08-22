from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from database.models import LogBook, LogBookEntry

from .forms import EntryForm, NewLogBookForm

# Create your views here.

def library(request):
    print(request.user)
    logbook_list = LogBook.objects.filter(owners__in=[request.user])
    print(logbook_list[0].owners)
    form = NewLogBookForm()
    context = {
        'logbook_list': logbook_list,
        'form': form
        }
    return render(request, 'library/library.html', context)

def logbook(request, logbook_id):
    book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
    form = EntryForm()
    context = {
        'logbook': book,
        'form':form
        }
    return render(request, 'library/logbook.html', context)

def new_entry(request, logbook_id):
    book = get_object_or_404(LogBook, pk=logbook_id, owners__in=[request.user])
    form = EntryForm(request.POST)
    if form.is_valid():
        entry = LogBookEntry(loogbook=book, author=request.user, text=form.cleaned_data['entry_text'])
        entry.save()
    return HttpResponseRedirect('/library/logbook/'+str(logbook_id))

def new_logbook(request):
    form = NewLogBookForm(request.POST)
    if form.is_valid():
        logbook = LogBook(name=form.cleaned_data['name'])
        logbook.save()
        return HttpResponseRedirect('/library/logbook/'+str(logbook.id))