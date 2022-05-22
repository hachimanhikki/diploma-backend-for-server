from rest_framework import serializers
from django.contrib.auth.models import User
from api.model.models import Department
from accounts.models import Teacher
import hashlib
# User / Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(max_length=200)
    class Meta:
        model = Teacher
        fields = ('first_name', 'second_name', 'username', 'email', 'password', "department_name", 'kpi')
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
        department = Department.objects.get(name=self.validated_data['department_name'])
        teacher.department = department
        password = self.validated_data['password']
        teacher.set_password(password)
        teacher.save()
        return teacher
