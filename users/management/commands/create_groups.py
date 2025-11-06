from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = "Создает группы пользователей и назначает права"

    def handle(self, *args, **options):
        moderators_group, created = Group.objects.get_or_create(name="moderators")

        if created:
            self.stdout.write('Группа "moderators" создана')
        else:
            self.stdout.write('Группа "moderators" уже существует')

        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        view_course = Permission.objects.get(
            codename="view_course", content_type=course_content_type
        )
        change_course = Permission.objects.get(
            codename="change_course", content_type=course_content_type
        )
        view_lesson = Permission.objects.get(
            codename="view_lesson", content_type=lesson_content_type
        )
        change_lesson = Permission.objects.get(
            codename="change_lesson", content_type=lesson_content_type
        )

        moderators_group.permissions.add(
            view_course, change_course, view_lesson, change_lesson
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Группе "moderators" назначены разрешения: просмотр и редактирование курсов и уроков'
            )
        )
