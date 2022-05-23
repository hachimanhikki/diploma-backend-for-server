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
            group = Group.objects.get(name=group_name['name'])
            group_subject = GroupSubject.objects.get(
                subject=subject, group=group)
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
            workload.save()
        subject.teachers.add(teacher)
        subject.save()
        return workload
