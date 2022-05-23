from rest_framework import serializers
from accounts.models import Teacher
from api.model.models import Group, GroupSubject, Subject, Workload
from django.db.models import F


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
    id = serializers.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields) if not isinstance(fields, str) else {fields}
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            exclude = set(exclude) if not isinstance(
                exclude, str) else {exclude}
            for field_name in exclude:
                self.fields.pop(field_name)

    class Meta:
        model = Subject
        fields = '__all__'
        depth = 1


class GroupSubjectSerializer:
    def __init__(self, by_subject: bool = False, by_group: bool = False, available: bool = False):
        self.data = []
        self.by_subject = by_subject
        self.by_group = by_group
        self.available = available
        if by_subject:
            self._serialize_by_subject()
        elif by_group:
            self._serialize_by_group()

    def _serialize_by_subject(self):
        self.data = []
        if self.available:
            subjects = Subject.objects.exclude(
                groups=None).filter(taken_hour__lt=F('total_hour')).order_by("name")
        else:
            subjects = Subject.objects.exclude(groups=None).order_by("name")
        for subject in subjects:
            groups_subjects = GroupSubject.objects.filter(
                subject_id__exact=subject.id).order_by('group__name')
            self.data.append(self._groups_subjects_to_dict(groups_subjects))

    def _serialize_by_group(self):
        self.data = []
        groups = Group.objects.exclude(subjects=None)
        for group in groups:
            if self.available:
                groups_subjects = GroupSubject.objects.filter(
                    group__name__exact=group.name, subject__taken_hour__lt=F('subject__total_hour')).order_by('group__name')
            else:
                groups_subjects = GroupSubject.objects.filter(
                    group__name__exact=group.name).order_by('group__name')
            self.data.append(self._groups_subjects_to_dict(groups_subjects))

    def _groups_subjects_to_dict(self, groups_subjects: list) -> dict:
        res = {}
        trimester = groups_subjects[0].trimester

        if self.by_subject:
            subject = groups_subjects[0].subject
            res = {
                'subject': SubjectSerializer(subject, exclude=('groups')).data,
                'groups': [GroupSerializer(group_subject.group).data for group_subject in groups_subjects],
                'trimester': trimester,
            }
        elif self.by_group:
            group = groups_subjects[0].group
            res = {
                'group': GroupSerializer(group).data,
                'subjects': [SubjectSerializer(group_subject.subject, exclude=('groups')).data for group_subject in groups_subjects],
                'trimester': trimester,
            }

        return res


class WorkloadGETSerializer:
    def __init__(self, teacher_name: str, all: bool = False, by_teacher: bool = False):
        self.data = []
        self.all = all
        self.by_teacher = by_teacher

        if all:
            self.data = []
            self._serialize_all()
        elif by_teacher:
            self.data = {}
            self._serialize_by_teacher(teacher_name)

    def _groups_subjects_get_by(self, lec: bool, teacher: Teacher):
        if lec:
            teacher_workloads = Workload.objects.filter(
                teacher_id__exact=teacher.id, is_lecture=True).order_by('group_subject__subject__name', 'group_subject__group__name')
            str_key = 'lec'
        else:
            teacher_workloads = Workload.objects.filter(
                teacher_id__exact=teacher.id, is_practice=True).order_by('group_subject__subject__name', 'group_subject__group__name')
            str_key = 'prac'
        teacher_subjects = set(
            teacher_workloads.values_list('group_subject__subject'))
        for subject in teacher_subjects:
            subject_ins = Subject.objects.get(id__exact=subject[0])
            trimester = Workload.objects.filter(
                teacher_id__exact=teacher.id, group_subject__subject__exact=subject).values_list('group_subject__trimester')
            groups = Workload.objects.filter(
                teacher_id__exact=teacher.id, group_subject__subject__exact=subject).values_list('group_subject__group')
            groups_ins = [Group.objects.get(
                name__exact=group[0]) for group in groups]
            self.data[str_key].append(self._groups_subjects_to_dict(
                subject=subject_ins, groups=groups_ins, trimester=trimester[0][0]))

    def _serialize_by_teacher(self, teacher_name):
        self.data = {}
        self.data['prac'] = []
        self.data['lec'] = []
        groups = []
        teacher = Teacher.objects.get(username__exact=teacher_name)

        self.data['teacher'] = {
            'username': teacher.username,
            'first_name': teacher.first_name,
            'second_name': teacher.second_name,
            'kpi': teacher.kpi,
            'email': teacher.email,
            'department': teacher.department.name,
            'total_hour': teacher.total_hour
        }
        self._groups_subjects_get_by(lec=True, teacher=teacher)
        self._groups_subjects_get_by(lec=False, teacher=teacher)

    def _serialize_all(self):
        self.data = []
        workloads = Workload.objects.all()
        teachers = workloads.values_list('teacher')
        for teacher in teachers:
            self.data.append(self._serialize_by_teacher(teacher.name))

    def _groups_subjects_to_dict(self, subject: Subject, groups: list, trimester: int) -> dict:
        res = {
            'subject': SubjectSerializer(subject, exclude=('groups', 'teachers')).data,
            'groups': [GroupSerializer(group).data for group in groups],
            'trimester': trimester,
        }
        return res


class WorkloadSerializer(serializers.ModelSerializer):
    teacher_username = serializers.CharField()
    subject = SubjectSerializer(exclude=('groups'))
    groups = GroupSerializer(many=True)
    trimester = serializers.IntegerField()
    is_lecture = serializers.BooleanField()
    is_practice = serializers.BooleanField()
    is_lab = serializers.BooleanField()

    class Meta:
        model = Workload
        fields = ('teacher_username', 'subject', 'groups',
                  'trimester', 'is_lecture', 'is_practice', 'is_lab')

    def save(self):
        teacher = Teacher.objects.get(
            username__exact=self.validated_data['teacher_username'])
        subject = Subject.objects.get(
            id__exact=self.validated_data['subject']['id'])
        for group_name in self.validated_data['groups']:
            group = Group.objects.get(name__exact=group_name['name'])
            group_subject = GroupSubject.objects.get(
                subject__exact=subject, group__exact=group)
            if group_taken(teacher, group_subject):
                workload = Workload.objects.filter(
                    teacher__exact=teacher, group_subject__exact=group_subject)[0]
                workload.is_lecture = self.validated_data['is_lecture'] or workload.is_lecture
                workload.is_practice = self.validated_data['is_practice'] or workload.is_practice
                workload.is_practice = self.validated_data['is_lab'] or workload.is_lab
            else:
                workload = Workload()
                workload.teacher = teacher
                workload.group_subject = group_subject
                workload.is_lecture = self.validated_data['is_lecture']
                workload.is_practice = self.validated_data['is_practice']
                workload.is_lab = self.validated_data['is_lab']
            if self.validated_data['is_practice']:
                subject.taken_practice += 1
                subject.taken_hour += subject.practice_hour
            if self.validated_data['is_lab']:
                subject.taken_lab += 1
                subject.taken_hour += subject.lab_hour
            workload.save()
        if self.validated_data['is_lecture']:
            subject.taken_lectures += 1
            subject.taken_hour += subject.lecture_hour
        subject.teachers.add(teacher)
        subject.save()
        return workload
