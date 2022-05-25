from rest_framework import serializers
from api.model.models import Department
from accounts.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(max_length=200)

    class Meta:
        model = Teacher
        fields = ('first_name', 'second_name', 'username',
                  'email', 'password', "department_name", 'kpi')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        teacher = Teacher(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            second_name=self.validated_data['second_name'],
            position="Преподователь",
            one_rate=560,
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
    def __init__(self, teachers: list):
        self.data = []
        self.teachers = teachers
        self._serialize_teachers()

    def _serialize_teachers(self):
        for teacher in self.teachers:
            res = {
                'username': teacher.username,
                'first_name': teacher.first_name,
                'second_name': teacher.second_name,
                'kpi': teacher.kpi,
                'email': teacher.email,
                'department': teacher.department.name,
                'total_hour': teacher.total_hour
            }
            self.data.append(res)
