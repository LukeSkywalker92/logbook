from django import forms

class EntryForm(forms.Form):
    entry_text = forms.CharField(widget=forms.Textarea(attrs={'width':'100%'}))