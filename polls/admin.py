from django.contrib import admin

# Custom model registration
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
