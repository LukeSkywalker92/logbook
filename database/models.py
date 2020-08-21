from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LogBook(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class LogBookEntry(models.Model):
    loogbook = models.ForeignKey(LogBook, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return self.author.get_username() + ' (' + str(self.pub_date) + ')' 