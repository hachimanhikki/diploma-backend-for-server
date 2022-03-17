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
    one_rate = models.IntegerField(null=True)
    load = models.FloatField(null=True)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.id} {self.full_name}"

    class Meta:
        db_table = 'teacher'


class Subject(models.Model):
    name = models.CharField(max_length=200)
    credits = models.IntegerField()
    lecture_count = models.IntegerField(null=True)
    practice_count = models.IntegerField(null=True)
    office_count = models.IntegerField(null=True)
    lab_count = models.IntegerField(null=True)
    lecture_hour = models.IntegerField(null=True)
    practice_hour = models.IntegerField(null=True)
    office_hour = models.IntegerField(null=True)
    lab_cout = models.IntegerField(null=True)
    total_hour = models.IntegerField(null=True)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.SET_NULL)
    teacher = models.ManyToManyField(Teacher, related_name='subjects')

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

    class Meta:
        db_table = 'subject'
