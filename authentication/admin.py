from django.contrib import admin
from authentication.models import wordSentiment
from .models import p_testd, t_testd, wordSentiment
# Register your models here.

admin.site.register(wordSentiment)
admin.site.register(p_testd)
admin.site.register(t_testd)