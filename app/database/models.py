from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(
        max_length=12,
        blank=True,
    )
    darkmode = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

class LogBook(models.Model):
    name = models.CharField(max_length=200)
    owners = models.ManyToManyField(User)

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