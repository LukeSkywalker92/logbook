from django.contrib import admin
from .models import LogBook, LogBookEntry


# Register your models here.

@admin.register(LogBook)
class LogBookAdmin(admin.ModelAdmin):
    pass

@admin.register(LogBookEntry)
class LogBookEntryAdmin(admin.ModelAdmin):
    pass
