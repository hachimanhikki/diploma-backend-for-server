from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Teacher
from api.model.models import Subject, Group, GroupSubject, Workload
from config.settings import DepartmentEnum
import hashlib
# User / Teacher Serializer


def group_taken(teacher: Teacher, group_subject: GroupSubject):
    if len(Workload.objects.filter(teacher__exact=teacher, group_subject__exact=group_subject)) == 1:
        return True


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
        }


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ("groups",)
        depth = 1


class WorkloadSerializer(serializers.ModelSerializer):
    teacher_username = serializers.CharField()
    print("subject")
    subject = SubjectSerializer()
    groups = GroupSerializer(many=True)
    trimester = serializers.IntegerField()
    is_lecture = serializers.BooleanField()
    is_practice = serializers.BooleanField()
    is_lab = serializers.BooleanField()
    class Meta:
        model = Workload
        fields = ('teacher_username', 'subject', 'groups', 'trimester', 'is_lecture', 'is_practice', 'is_lab')



    def save(self):
        teacher = Teacher.objects.get(username=self.validated_data['teacher_username'])
        subject = Subject.objects.get(name=self.validated_data['subject']['name'])
        for group_name in self.validated_data['groups']:
            group = Group.objects.get(name=group_name['name'])
            group_subject = GroupSubject.objects.get(subject=subject, group=group)
            if group_taken(teacher, group_subject):
                workload = Workload.objects.filter(teacher__exact=teacher, group_subject__exact=group_subject)[0]
                workload.is_lecture = self.validated_data['is_lecture'] or workload.is_lecture 
                workload.is_practice = self.validated_data['is_practice'] or workload.is_practice
            else:
                workload = Workload()
                workload.teacher = teacher
                workload.group_subject = group_subject
                workload.is_lecture = self.validated_data['is_lecture']
                workload.is_practice = self.validated_data['is_practice']
                workload.is_lab = False
            workload.save()

        return workload
