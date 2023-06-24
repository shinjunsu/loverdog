from django.contrib import admin
from .models import board
# Register your models here.

class boardAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(board, boardAdmin)

