import os
import openpyxl
from django.conf import settings
from api.model.models import Group, Subject, Teacher
from config.settings import DepartmentEnum
import api.service.functions as functions


wb = openpyxl.load_workbook(os.path.join(
    settings.MEDIA_ROOT, 'all_data.xlsx'), data_only=True)
teachers_sheet = wb['Преподаватели']
course_sheet = [0, wb['1 курс'], wb['2 курс'], wb['3 курс']]
group_sheet = wb['Группы']


def parse_teachers() -> list:
    teachers = []
    for i in range(2, teachers_sheet.max_column + 1):
        teacher_name = teachers_sheet.cell(row=1, column=i).value
        if teacher_name is not None:
            teacher = Teacher(full_name=teacher_name, excel_column_index=i)
            teachers.append(teacher)
    return teachers


def parse_subjects(course: int) -> list:
    subjects = []
    for i in range(10, course_sheet[course].max_row + 1):
        department = course_sheet[course].cell(
            row=i, column=course_sheet[course].max_column).value
        if isinstance(department, str) and functions.compare_strings(department, DepartmentEnum.computer_engineering.value):
            subject = Subject()
            subject.configure_subject(i, course_sheet[course])
            subject.department_id = DepartmentEnum.computer_engineering.id
            subjects.append(subject)
    return subjects


def parse_subjects_for_teacher(teacher: Teacher) -> list:
    subject_names = []
    for i in range(2, teachers_sheet.max_row + 1):
        if teachers_sheet.cell(row=i, column=teacher.excel_column_index).value is not None:
            subject_name = teachers_sheet.cell(row=i, column=1).value
            subject_names.append(functions.formated(subject_name))
    return subject_names


def parse_groups() -> list:
    groups = []
    for i in range(2, group_sheet.max_row + 1):
        group = Group()
        group.name = group_sheet.cell(row=i, column=1).value
        group.course = functions.clear_int(
            group_sheet.cell(row=i, column=2).value)
        group.number_of_students = functions.clear_int(
            group_sheet.cell(row=i, column=3).value)
        group.code = group.name.split('-')[0]
        if group.course != 1:
            groups.append(group)
    return groups
