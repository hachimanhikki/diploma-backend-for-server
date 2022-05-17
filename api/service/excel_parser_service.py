import os
import openpyxl
from django.conf import settings
from api.model.models import Group, Subject
from accounts.models import Teacher
from config.settings import DepartmentEnum
import api.service.functions as functions


wb = openpyxl.load_workbook(os.path.join(
    settings.MEDIA_ROOT, 'all_data.xlsx'), data_only=True)
teachers_sheet = wb['Преподаватели']
course_sheet = [0, wb['1 курс'], wb['2 курс'], wb['3 курс']]
course_educational_programs_count = [0, 11, 9, 8]
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
            row=i, column=course_educational_programs_count[course] + 14).value
        if isinstance(department, str) and functions.compare_strings(department, DepartmentEnum.computer_engineering.value):
            subject = Subject()
            subject.configure_subject(
                i, DepartmentEnum.computer_engineering.id, course_sheet[course], course_educational_programs_count[course])
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
        groups.append(group)
    return groups


def parse_groups_for_subject(course: int, subject: Subject, allowed_group_codes) -> list:
    groups = []
    for i in range(2, len(allowed_group_codes) + 2):
        trimester = functions.clear_int(course_sheet[course].cell(
            row=subject.excel_row_index, column=i).value)
        group_code = course_sheet[course].cell(row=8, column=i).value
        if group_code in allowed_group_codes and trimester > 0:
            groups.append((group_code, trimester))
    return groups
