from django.contrib import admin
from .model.models import Department, Subject, Teacher

admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Subject)
