import os
import openpyxl
from django.conf import settings
from api.model.models import Subject, Teacher
from config.settings import DepartmentEnum
import api.service.functions as functions


wb = openpyxl.load_workbook(os.path.join(
    settings.MEDIA_ROOT, 'all_data.xlsx'), data_only=True)
teachers_sheet = wb['Преподаватели']
course_sheet = [0, wb['1 курс'], wb['2 курс'], wb['3 курс']]


def parse_teachers() -> list:
    teachers = []
    for i in range(2, teachers_sheet.max_column + 1):
        teacher_name = teachers_sheet.cell(row=1, column=i).value
        if teacher_name is not None:
            teacher = Teacher(full_name=teacher_name)
            teachers.append(teacher)
    return teachers


def parse_subjects(course_number: int) -> list:
    subjects = []
    for i in range(10, course_sheet[course_number].max_row + 1):
        department = course_sheet[course_number].cell(
            row=i, column=course_sheet[course_number].max_column).value
        if isinstance(department, str) and functions.compare_strings(department, DepartmentEnum.computer_engineering.value):
            subject = Subject()
            subject.configure_subject(i, course_sheet[course_number])
            subject.department_id = DepartmentEnum.computer_engineering.get_id()
            subjects.append(subject)
    return subjects


def parse_subjects_for_teacher(teacher: Teacher) -> list:
    teacher_index = 2
    while teachers_sheet.cell(row=1, column=teacher_index).value != teacher.full_name:
        teacher_index += 1
    subject_names = []
    for i in range(2, teachers_sheet.max_row + 1):
        if teachers_sheet.cell(row=i, column=teacher_index).value is not None:
            subject_name = teachers_sheet.cell(row=i, column=1).value
            subject_names.append(functions.formated(subject_name))
    return subject_names
