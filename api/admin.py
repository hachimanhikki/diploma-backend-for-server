from django.contrib import admin
from .model.models import Department, Group, Subject, Teacher

admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Subject)
