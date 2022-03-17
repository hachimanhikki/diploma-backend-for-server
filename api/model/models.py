from django.db import models


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

# class Subject(models.Model):
#     name = models.CharField(max_length=200)
#     credits = models.IntegerField()

#     def __str__(self) -> str:
#         return f"{self.name}, {self.credits}"
