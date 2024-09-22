from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError
from django.core.management.base import CommandParser
from django.db.models import Count

from recovery.utils import bulk_create_recovery_codes


User = get_user_model()


class Command(BaseCommand):
    help = "Generates Recovery Codes for provided usernames"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--username",
            "-u",
            nargs="*",
            type=str,
            help="List of Usernames to generate recovery code for separated by space",
        )

    def handle(self, *args, **options) -> None:
        users = User.objects.annotate(num_of_codes=Count("recovery_codes")).filter(num_of_codes=0)

        if usernames := options["username"]:
            if usernames == "__all__":
                self.stdout.write(
                    self.style.WARNING("Generating Recovery Codes for all the users...")
                )
            else:
                users.filter(username__in=usernames)
                self.stdout.write(
                    self.style.WARNING(
                        f"Generating Recovery Codes for users {', '.join(usernames)}..."
                    )
                )

        for user in users:
            try:
                bulk_create_recovery_codes(user=user)
            except CommandError as err:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error generating Recovery Codes for --> {getattr(user, user.USERNAME_FIELD)}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully generated Recovery Codes for --> {getattr(user, user.USERNAME_FIELD)}"
                    )
                )
