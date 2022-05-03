from django.db import models
import api.service.functions as functions


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.id} {self.name}"

    class Meta:
        db_table = 'department'


class Teacher(models.Model):
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, null=True)
    kpi = models.CharField(max_length=200, null=True)
    one_rate = models.IntegerField(null=True)
    load = models.FloatField(null=True)
    excel_column_index = models.IntegerField(null=True)
    total_hour = models.IntegerField(default=0)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.id} {self.full_name} {self.total_hour}"

    class Meta:
        db_table = 'teacher'


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
    practice_count = models.IntegerField(default=0)
    office_count = models.IntegerField(default=0)
    lab_count = models.IntegerField(default=0)
    lecture_hour = models.IntegerField(default=0)
    practice_hour = models.IntegerField(default=0)
    office_hour = models.IntegerField(default=0)
    lab_hour = models.IntegerField(default=0)
    total_hour = models.IntegerField(default=0)
    excel_row_index = models.IntegerField(null=True)

    department = models.ForeignKey(
        Department, null=True, on_delete=models.SET_NULL)
    teachers = models.ManyToManyField(Teacher, related_name='subjects')
    groups = models.ManyToManyField(
        Group, related_name='subjects', through='GroupSubject')

    def __str__(self) -> str:
        return f"{self.name}, {self.credits}"

    def configure_subject(self, row_index, sheet) -> None:
        self.name = functions.formated(
            sheet.cell(row=row_index, column=1).value)
        self.credits = functions.clear_int(
            sheet.cell(row=row_index, column=12).value)
        self.lecture_count = functions.clear_int(
            sheet.cell(row=row_index, column=13).value)
        self.practice_count = functions.clear_int(
            sheet.cell(row=row_index, column=14).value)
        self.office_count = functions.clear_int(
            sheet.cell(row=row_index, column=15).value)
        self.lab_count = functions.clear_int(
            sheet.cell(row=row_index, column=16).value)
        self.lecture_hour = functions.clear_int(
            sheet.cell(row=row_index, column=17).value)
        self.practice_hour = functions.clear_int(
            sheet.cell(row=row_index, column=18).value)
        self.office_hour = functions.clear_int(
            sheet.cell(row=row_index, column=19).value)
        self.lab_hour = functions.clear_int(
            sheet.cell(row=row_index, column=20).value)
        self.total_hour = functions.clear_int(
            sheet.cell(row=row_index, column=21).value)
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group_subject = models.ForeignKey(
        GroupSubject, null=True, on_delete=models.CASCADE)
    is_lecture = models.BooleanField()
    is_lab = models.BooleanField()
    is_practice = models.BooleanField(default=True)

    class Meta:
        db_table = 'workload'
