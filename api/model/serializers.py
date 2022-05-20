from rest_framework import serializers
from api.model.models import Group, GroupSubject, Subject


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
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
    def __init__(self, by_subject: bool = False, by_group: bool = False):
        self.data = []
        self.by_subject = by_subject
        self.by_group = by_group
        if by_subject:
            self._serialize_by_subject()
        elif by_group:
            self._serialize_by_group()

    def _serialize_by_subject(self):
        self.data = []
        subjects = Subject.objects.exclude(groups=None)
        for subject in subjects:
            groups_subjects = GroupSubject.objects.filter(
                subject_id__exact=subject.id).order_by('group__name')
            self.data.append(self._groups_subjects_to_dict(groups_subjects))

    def _serialize_by_group(self):
        self.data = []
        groups = Group.objects.exclude(subjects=None)
        for group in groups:
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