from django.contrib import admin

# Register your models here.
from desarrollo.models import RegistroUserStory, Sprint

admin.site.register(RegistroUserStory)
admin.site.register(Sprint)