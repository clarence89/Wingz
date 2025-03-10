
from django.core.management.base import BaseCommand
from users.models import User, Role


class Command(BaseCommand):
    help = "Create a superuser with preset data"

    def handle(self, *args, **options):
        username = "admin"
        email = "clarence89.github.io"
        password = "adminpassword"
        if not User.objects.filter(username=username).exists():
            users = User.objects.create_superuser(username, email, password)
            users.first_name = "Admin"
            users.last_name = "Account"
            users.role = Role.objects.get(name="admin")
            users.save()
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists.")) 
 