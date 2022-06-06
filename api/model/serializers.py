from rest_framework import serializers
from accounts.models import Teacher
from accounts.serializers import TeacherGETSerializer
from api.model.models import Group, GroupSubject, Schedule, Subject, Workload
from django.db.models import F


def group_taken(teacher: Teacher, group_subject: GroupSubject):
    if len(Workload.objects.filter(teacher__exact=teacher, group_subject__exact=group_subject)) == 1:
        return True


def get_refresh_data(teacher: Teacher, subject: Subject):
    office_mod = 0
    lec_mod = 0
    no_of_prac_groups = Workload.objects.filter(
        is_practice=True, teacher__exact=teacher, group_subject__subject__exact=subject).count()
    no_of_lab_groups = Workload.objects.filter(
        is_lab=True, teacher__exact=teacher, group_subject__subject__exact=subject).count()
    if Workload.objects.filter(is_lecture=True, teacher__exact=teacher, group_subject__subject__exact=subject).count() > 0:
        lec_mod = 1
    if teacher in subject.teachers.all():
        office_mod = 1
    total_hour_by_subject = subject.practice_hour * no_of_prac_groups + subject.lecture_hour * \
        lec_mod + subject.lab_hour * no_of_lab_groups + subject.office_hour * office_mod
    return {
        'total_hour': total_hour_by_subject,
        'prac_groups': no_of_prac_groups,
        'lab_groups': no_of_lab_groups,
        'is_lec': lec_mod,
        'is_office': office_mod
    }


def refresh_teacher_and_subject(teacher: Teacher, subject: Subject, refresh: bool):
    modifier = -1 if refresh else 1
    refresh_data = get_refresh_data(teacher=teacher, subject=subject)
    teacher.total_hour += modifier * refresh_data['total_hour']
    subject.taken_hour += modifier * refresh_data['total_hour']
    subject.taken_lectures += modifier * 1 if refresh_data['is_lec'] else 0
    subject.taken_practice += modifier * refresh_data['prac_groups']
    subject.taken_lab += modifier * refresh_data['lab_groups']
    subject.office_count += modifier * 1 if refresh_data['is_office'] else 0
    return teacher, subject


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
            lec_groups = []
            prac_groups = []
            lec_taken_groups = Workload.objects.filter(
                group_subject__subject__exact=subject, is_lecture__exact=True).values_list('group_subject__group')
            prac_taken_groups = Workload.objects.filter(
                group_subject__subject__exact=subject, is_practice__exact=True).values_list('group_subject__group')
            lec_taken_groups_ins = [Group.objects.get(
                name__exact=taken_group[0]) for taken_group in lec_taken_groups]
            prac_taken_groups_ins = [Group.objects.get(
                name__exact=taken_group[0]) for taken_group in prac_taken_groups]
            for group_subject in groups_subjects:
                if group_subject.group not in lec_taken_groups_ins:
                    lec_groups.append(GroupSerializer(
                        group_subject.group).data)
                if group_subject.group not in prac_taken_groups_ins:
                    prac_groups.append(GroupSerializer(
                        group_subject.group).data)

            lectures = []
            if subject.lecture_count:
                dsitributed_lec_count = self._distribute_lecture_teachers(
                    len(lec_groups), subject.lecture_count)
                prev_count = 0
                for count in dsitributed_lec_count:
                    lectures.append(
                        lec_groups[prev_count:(prev_count + count)])
                    prev_count += count

            res = {
                'subject': SubjectSerializer(subject, exclude=('groups')).data,
                'groups': {'prac': prac_groups, 'lec': lectures},
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

    def _distribute_lecture_teachers(self, groups_count: int, lecture_count: int) -> list:
        return self._distribute_groups_teachers(groups_count, lecture_count)

    def _distribute_groups_teachers(self, count_1: int, count_2: int) -> list:
        base, extra = divmod(count_1, count_2)
        result = [base + (i < extra) for i in range(count_2)]
        return result


class WorkloadGETSerializer:
    def __init__(self, teacher_name: str = '', all: bool = False, by_teacher: bool = False):
        self.data = []
        self.all = all
        self.by_teacher = by_teacher

        if all:
            self.data = self._serialize_all()
        elif by_teacher:
            self.data = self._serialize_by_teacher(teacher_name)

    def _groups_subjects_get_by(self, lec: bool, teacher: Teacher):
        if lec:
            teacher_workloads = Workload.objects.filter(
                teacher_id__exact=teacher.id, is_lecture=True).order_by('group_subject__subject__name', 'group_subject__group__name')
        else:
            teacher_workloads = Workload.objects.filter(
                teacher_id__exact=teacher.id, is_practice=True).order_by('group_subject__subject__name', 'group_subject__group__name')
        res = []
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
            res.append(self._groups_subjects_to_dict(
                subject=subject_ins, groups=groups_ins, trimester=trimester[0][0]))
        return res

    def _serialize_by_teacher(self, teacher_username: str) -> dict:
        res = {}
        teacher = Teacher.objects.get(username__exact=teacher_username)
        serializer = TeacherGETSerializer(teacher=teacher)
        res['teacher'] = serializer.data
        res['lec'] = self._groups_subjects_get_by(lec=True, teacher=teacher)
        res['prac'] = self._groups_subjects_get_by(lec=False, teacher=teacher)
        return res

    def _serialize_all(self) -> list:
        res = []
        workloads = Workload.objects.all()
        teachers = workloads.values_list('teacher', flat=True).distinct()
        for teacher_id in teachers:
            teacher = Teacher.objects.get(id__exact=teacher_id)
            res.append(self._serialize_by_teacher(teacher.username))
        return res

    def _groups_subjects_to_dict(self, subject: Subject, groups: list, trimester: int) -> dict:
        res = {
            'subject': SubjectSerializer(subject, exclude=('groups', 'teachers')).data,
            'groups': [GroupSerializer(group).data for group in groups],
            'trimester': trimester,
        }
        return res


class WorkloadSerializer(serializers.ModelSerializer):
    teacher_username = serializers.CharField()
    subject = SubjectSerializer(exclude=('groups', 'teachers'))
    groups = GroupSerializer(many=True)
    trimester = serializers.IntegerField()
    is_lecture = serializers.BooleanField()
    is_practice = serializers.BooleanField()
    is_lab = serializers.BooleanField()

    class Meta:
        model = Workload
        fields = ('teacher_username', 'subject', 'groups',
                  'trimester', 'is_lecture', 'is_practice', 'is_lab')

    def _save_workload(self, teacher: Teacher, subject: Subject):
        teacher, subject = refresh_teacher_and_subject(
            teacher=teacher, subject=subject, refresh=True)
        for group_name in self.validated_data['groups']:
            group = Group.objects.get(name__exact=group_name['name'])
            group_subject = GroupSubject.objects.get(
                subject__exact=subject, group__exact=group)
            if group_taken(teacher, group_subject):
                workload = Workload.objects.filter(
                    teacher__exact=teacher, group_subject__exact=group_subject)[0]
                workload.is_lecture = self.validated_data['is_lecture'] or workload.is_lecture
                workload.is_practice = self.validated_data['is_practice'] or workload.is_practice
                workload.is_lab = self.validated_data['is_lab'] or workload.is_lab
            else:
                workload = Workload()
                workload.teacher = teacher
                workload.group_subject = group_subject
                workload.is_lecture = self.validated_data['is_lecture']
                workload.is_practice = self.validated_data['is_practice']
                workload.is_lab = self.validated_data['is_lab']
            workload.save()
        if teacher not in subject.teachers.all():
            subject.teachers.add(teacher)
        teacher, subject = refresh_teacher_and_subject(
            teacher=teacher, subject=subject, refresh=False)
        teacher.save()
        subject.save()

    def edit_data(self):
        teacher = Teacher.objects.get(
            username__exact=self.validated_data['teacher_username'])
        subject = Subject.objects.get(
            id__exact=self.validated_data['subject']['id'])

        # refresh all hour and subject
        teacher, subject = refresh_teacher_and_subject(
            teacher=teacher, subject=subject, refresh=True)
        subject.teachers.remove(teacher)
        # delete all workload records and replace them with new groups
        Workload.objects.filter(
            group_subject__subject__name__exact=subject.name, teacher__exact=teacher).delete()
        self._save_workload(subject=subject, teacher=teacher)
        return None

    def save_data(self):
        teacher = Teacher.objects.get(
            username__exact=self.validated_data['teacher_username'])
        subject = Subject.objects.get(
            id__exact=self.validated_data['subject']['id'])
        self._save_workload(subject=subject, teacher=teacher)
        return None


class ScheduleSerializer:
    def __init__(self, group_name: str = '', teacher_name: str = '', by_group: bool = False, by_teacher: bool = False) -> None:
        self.data = {}
        self.group_name = group_name
        self.teacher_name = teacher_name
        if by_group:
            self._serialize_by_group()
        elif by_teacher:
            self._serialize_by_teacher()

    def get_groups(self) -> list:
        groups = Schedule.objects.order_by('group_name').values_list(
            'group_name', flat=True).distinct()
        return groups

    def get_teachers(self) -> list:
        teachers = Schedule.objects.order_by('teacher_name').values_list(
            'teacher_name', flat=True).distinct()
        return teachers

    def _set_initial_data(self) -> None:
        self.data = {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': [],
            'Saturday': [],
            'time_ranges': []
        }

    def _make_info(self, schedule, start_time, end_time) -> dict:
        return {
            'start_time': start_time,
            'end_time': end_time,
            'group_name': schedule.group_name,
            'teacher_name': schedule.teacher_name,
            'subject_name': schedule.subject_name,
            'classroom': schedule.classroom,
            'is_lecture': schedule.is_lecture,
            'is_practice': schedule.is_practice,
            'is_lab': schedule.is_lab
        }

    def _serialize_by_group(self) -> None:
        self._set_initial_data()
        schedules = Schedule.objects.filter(
            group_name__exact=self.group_name).order_by('time')
        self._populate_data(schedules)

    def _serialize_by_teacher(self) -> None:
        self._set_initial_data()
        schedules = Schedule.objects.filter(
            teacher_name__exact=self.teacher_name).order_by('time')
        self._populate_data(schedules)

    def _populate_data(self, schedules):
        for schedule in schedules:
            if schedule.week_day in self.data:
                start_time, end_time = schedule.time.split("-")
                info = self._make_info(schedule, start_time, end_time)
                self.data[schedule.week_day].append(info)
                times = {'start_time': start_time, 'end_time': end_time}
                if times not in self.data['time_ranges']:
                    self.data['time_ranges'].append(times)
