from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Teacher
from config.settings import DepartmentEnum
import hashlib
# User / Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = Teacher
        fields = ('first_name', 'second_name', 'position', 'username', 'email', 'password', 'password2')
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
                one_rate=560,
                load=1.0,
                kpi='Teacher',
                department_id=DepartmentEnum.computer_engineering.id,
            )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        teacher.set_password(password)
        teacher.save()
        return teacher
