from django import forms
from markdownx.fields import MarkdownxFormField

class EntryForm(forms.Form):
    entry_text = MarkdownxFormField()