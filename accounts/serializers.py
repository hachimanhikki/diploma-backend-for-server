from rest_framework import serializers
from api.model.models import Department
from accounts.models import Teacher
from rest_framework.authtoken.models import Token


class TeacherSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(max_length=200)

    class Meta:
        model = Teacher
        fields = ('first_name', 'second_name', 'username',
                  'email', 'password', "department_name", 'kpi', 'position', 'one_rate')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        teacher = Teacher(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            second_name=self.validated_data['second_name'],
            position=self.validated_data['position'],
            one_rate=self.validated_data['one_rate'],
            load=1.0,
            kpi=self.validated_data['kpi'],
        )
        department = Department.objects.get(
            name=self.validated_data['department_name'])
        teacher.department = department
        password = self.validated_data['password']
        teacher.set_password(password)
        teacher.save()
        return teacher


class TeacherGETSerializer:
    def __init__(self, teacher: Teacher = None, teachers: list = None, many: bool = False):
        self.data = {}
        if many:
            self.data = self._serialize_teachers(teachers)
        else:
            self.data = self._serialize_teacher(teacher)

    def _serialize_teacher(self, teacher: Teacher) -> dict:
        return {
            'username': teacher.username,
            'first_name': teacher.first_name,
            'second_name': teacher.second_name,
            'kpi': teacher.kpi,
            'position': teacher.position,
            'one_rate': teacher.one_rate,
            'email': teacher.email,
            'department_name': teacher.department.name,
            'load': teacher.load,
            'total_hour': teacher.total_hour,
            'is_head': teacher.is_admin,
            'token': Token.objects.get(user=teacher).key
        }

    def _serialize_teachers(self, teachers) -> list:
        res = []
        for teacher in teachers:
            res.append(self._serialize_teacher(teacher))
        return res
