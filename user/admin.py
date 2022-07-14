from django.contrib import admin

# Register your models here.
from user.models import User, DreamAssociation

admin.site.register(User)
admin.site.register(DreamAssociation)
