from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apps.recorder.models import VoiceRecordingModel
from apps.users.models import User


class Command(BaseCommand):
    help = 'Create role-based groups: Super Admin, Authenticator, Normal User.'

    def handle(self, *args, **options):
        review_perm, _ = Permission.objects.get_or_create(
            codename='can_review_recording',
            defaults={
                'name': 'Can review and verify voice recording status (approve/reject)',
                'content_type': ContentType.objects.get_for_model(VoiceRecordingModel),
            },
        )

        groups = {
            'Super Admin': [],
            'Authenticator': [review_perm],
            'Normal User': [],
        }

        for name, perms in groups.items():
            group, created = Group.objects.get_or_create(name=name)
            group.permissions.set(perms)
            status = 'created' if created else 'updated'
            self.stdout.write(self.style.SUCCESS(f'Group "{name}" {status}'))

        self.stdout.write(self.style.SUCCESS('Done. Assign users a role via the "role" field or add them to a group.'))