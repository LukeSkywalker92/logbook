from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from database.models import LogBook, LogBookEntry

from .forms import EntryForm

# Create your views here.

def library(request):
    logbook_list = LogBook.objects.all()
    context = {
        'logbook_list': logbook_list
        }
    return render(request, 'library/library.html', context)

def logbook(request, logbook_id):
    book = get_object_or_404(LogBook, pk=logbook_id)
    form = EntryForm()
    return render(request, 'library/logbook.html', {'logbook': book, 'form':form})

def new_entry(request, logbook_id):
    book = get_object_or_404(LogBook, pk=logbook_id)
    form = EntryForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data['entry_text'])
        print(request.user)
        entry = LogBookEntry(loogbook=book, author=request.user, text=form.cleaned_data['entry_text'])
        entry.save()
    return HttpResponseRedirect('/library/logbook/'+str(logbook_id))