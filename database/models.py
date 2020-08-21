from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.

class LogBook(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class LogBookEntry(models.Model):
    loogbook = models.ForeignKey(LogBook, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = MarkdownxField()
    pub_date = models.DateTimeField('date published', auto_now=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def __str__(self):
        return self.author.get_username() + ' (' + str(self.pub_date) + ')' 