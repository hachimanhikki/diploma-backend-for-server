from datetime import date
import openpyxl
from api.service.save_service import create_excel_doc
from config.settings import MEDIA_ROOT, TEMPLATE_NAME
from api.model.models import Teacher, Workload
from openpyxl.styles import Border, Side


wb = workload_sheet = None


def create_excel_workload() -> None:
    global wb, workload_sheet
    create_excel_doc(TEMPLATE_NAME, _excel_doc_name())
    wb = openpyxl.load_workbook(_excel_doc_name())
    workload_sheet = wb['Нагрузка']
    _populate_workload()


def _populate_workload() -> None:
    all_teacher = Teacher.objects.all()
    row_index = 7
    for teacher in all_teacher:
        teacher_workloads = Workload.objects.filter(
            teacher_id__exact=teacher.id).order_by('group_subject__subject__name', 'group_subject__group__name')
        if not teacher_workloads:
            continue
        _configure_teacher_cell(teacher, row_index)
        teacher_subjects = set(teacher_workloads.values_list(
            'group_subject__subject__name', 'group_subject__subject__office_hour'))
        start_row_index = row_index
        for subject_name, office_hour in teacher_subjects:
            workload_sheet.cell(row=row_index, column=16).value = office_hour
            teacher_lecture_workloads = teacher_workloads.filter(
                group_subject__subject__name__exact=subject_name, is_lecture__exact=True)
            teacher_practice_workloads = teacher_workloads.filter(
                group_subject__subject__name__exact=subject_name, is_practice__exact=True)
            teacher_lab_workloads = teacher_workloads.filter(
                group_subject__subject__name__exact=subject_name, is_lab__exact=True)
            if teacher_lecture_workloads:
                _configure_lecture_cells(teacher_lecture_workloads, row_index)
                row_index += 1
            if teacher_practice_workloads:
                _configure_cells(teacher_practice_workloads,
                                 row_index, is_practice=True)
                row_index += len(teacher_practice_workloads)
            if teacher_lab_workloads:
                _configure_cells(teacher_lab_workloads, row_index, is_lab=True)
                row_index += len(teacher_lab_workloads)
        _merge_column(start_row_index, row_index)
        workload_sheet.cell(
            row=row_index, column=19).value = teacher.total_hour
        _set_borders(row_index)
        row_index += 1
    wb.save(_excel_doc_name())


def _set_borders(row_index: int) -> None:
    other_side = Side(border_style='thin')
    bottom_side = Side(border_style='medium')
    for col in range(2, workload_sheet.max_column + 1):
        workload_sheet.cell(row=row_index, column=col).border = Border(
            bottom=bottom_side, top=other_side, left=other_side, right=other_side)


def _merge_column(start_row_index: int, end_row_index: int) -> None:
    for col in range(2, 7):
        workload_sheet.merge_cells(
            start_row=start_row_index, start_column=col, end_row=end_row_index, end_column=col)


def _configure_lecture_cells(workloads, row_index: int) -> None:
    _configure_workload_cell(workloads[0], row_index)
    lecture_groups = ', '.join(
        [workload.group_subject.group.name for workload in workloads])
    number_of_students = sum(
        [workload.group_subject.group.number_of_students for workload in workloads])
    workload_sheet.cell(row=row_index, column=9).value = lecture_groups
    workload_sheet.cell(row=row_index, column=11).value = number_of_students
    workload_sheet.cell(
        row=row_index, column=13).value = workloads[0].group_subject.subject.lecture_hour


def _configure_cells(workloads, row_index: int, is_practice: bool = False, is_lab: bool = False) -> None:
    for workload in workloads:
        _configure_workload_cell(workload, row_index, is_practice, is_lab)
        row_index += 1


def _configure_teacher_cell(teacher: Teacher, row_index: int) -> None:
    workload_sheet.cell(row=row_index, column=2).value = teacher.full_name
    workload_sheet.cell(row=row_index, column=5).value = teacher.one_rate
    workload_sheet.cell(row=row_index, column=6).value = teacher.load


def _configure_workload_cell(workload: Workload, row_index: int, is_practice: bool = False, is_lab: bool = False) -> None:
    subject = workload.group_subject.subject
    group = workload.group_subject.group
    workload_sheet.cell(
        row=row_index, column=7).value = subject.name.capitalize()
    workload_sheet.cell(
        row=row_index, column=8).value = group.course
    workload_sheet.cell(row=row_index, column=9).value = group.name
    workload_sheet.cell(
        row=row_index, column=10).value = workload.group_subject.trimester
    workload_sheet.cell(
        row=row_index, column=11).value = group.number_of_students
    workload_sheet.cell(
        row=row_index, column=12).value = subject.credits
    if is_practice:
        workload_sheet.cell(
            row=row_index, column=15).value = subject.practice_hour
    if is_lab:
        workload_sheet.cell(
            row=row_index, column=14).value = subject.lab_hour


def _formatted_current_date() -> None:
    today = date.today()
    return date.strftime(today, "%d.%m.%Y")


def _excel_doc_name() -> None:
    return f"{MEDIA_ROOT}/Нагрузка {_formatted_current_date()}.xlsx"
