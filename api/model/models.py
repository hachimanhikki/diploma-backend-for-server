from django.db import models
import api.service.functions as functions
from config import settings


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.id} {self.name}"

    class Meta:
        db_table = 'department'


class Group(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    code = models.CharField(max_length=100)
    course = models.IntegerField()
    number_of_students = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = 'group'


class Subject(models.Model):
    name = models.CharField(max_length=200)
    credits = models.IntegerField()
    lecture_count = models.IntegerField(default=0)
    taken_lectures = models.IntegerField(default=0)
    practice_count = models.IntegerField(default=0)
    taken_practice = models.IntegerField(default=0)
    office_count = models.IntegerField(default=0)
    taken_office = models.IntegerField(default=0)
    lab_count = models.IntegerField(default=0)
    taken_lab = models.IntegerField(default=0)
    lecture_hour = models.IntegerField(default=0)
    practice_hour = models.IntegerField(default=0)
    office_hour = models.IntegerField(default=0)
    lab_hour = models.IntegerField(default=0)
    total_hour = models.IntegerField(default=0)
    taken_hour = models.IntegerField(default=0)
    excel_row_index = models.IntegerField(null=True)

    department = models.ForeignKey(
        Department, null=True, on_delete=models.SET_NULL)
    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='subjects')
    groups = models.ManyToManyField(
        Group, related_name='subjects', through='GroupSubject')

    def __str__(self) -> str:
        return f"{self.name}, {self.credits}"

    def configure_subject(self, row_index, department_id, sheet, educational_programs_count) -> None:
        self.department_id = department_id
        self.name = functions.formated(
            sheet.cell(row=row_index, column=1).value)
        self.credits = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 4).value)
        self.lecture_count = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 5).value)
        self.practice_count = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 6).value)
        self.office_count = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 7).value)
        self.lab_count = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 8).value)
        self.lecture_hour = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 9).value)
        self.practice_hour = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 10).value)
        self.office_hour = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 11).value)
        self.lab_hour = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 12).value)
        self.total_hour = functions.clear_int(
            sheet.cell(row=row_index, column=educational_programs_count + 13).value)
        self.excel_row_index = row_index

    class Meta:
        db_table = 'subject'


class GroupSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, db_column='group_name', on_delete=models.CASCADE)
    trimester = models.IntegerField()

    class Meta:
        db_table = 'group_subject'
        unique_together = [['subject', 'group']]


class Workload(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_subject = models.ForeignKey(
        GroupSubject, null=True, on_delete=models.CASCADE)
    is_lecture = models.BooleanField()
    is_lab = models.BooleanField()
    is_practice = models.BooleanField(default=True)

    class Meta:
        db_table = 'workload'
