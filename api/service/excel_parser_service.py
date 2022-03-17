import os
import openpyxl
from django.conf import settings
from api.model.models import Teacher
from config.settings import DepartmentEnum


wb = openpyxl.load_workbook(os.path.join(
    settings.MEDIA_ROOT, 'all_data.xlsx'), data_only=True)
teachers_sheet = wb['Преподаватели']


def fetch_teachers():
    teachers = []
    for i in range(2, teachers_sheet.max_column + 1):
        teacher_name = teachers_sheet.cell(row=1, column=i).value
        if teacher_name is not None:
            teacher = Teacher(full_name=teacher_name)
            teachers.append(teacher)
    return teachers
