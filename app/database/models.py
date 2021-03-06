from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    darkmode = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

class LogBook(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owner')
    collaborators = models.ManyToManyField(User, related_name='collaborators')
    creation_date = models.DateTimeField('date created', auto_now=True)
    updated_date = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.name

class LogBookEntry(models.Model):
    loogbook = models.ForeignKey(LogBook, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = MarkdownxField()
    pub_date = models.DateTimeField('date published', auto_now=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def __str__(self):
        return self.author.get_username() + ' (' + str(self.pub_date) + ')' 