from django.contrib import admin
from .model.models import Department, Group, Subject

admin.site.register(Department)

admin.site.register(Group)
admin.site.register(Subject)
