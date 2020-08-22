from django import forms
from markdownx.fields import MarkdownxFormField

class EntryForm(forms.Form):
    entry_text = MarkdownxFormField()

class NewLogBookForm(forms.Form):
    name = forms.CharField(max_length=200)