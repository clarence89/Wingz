import random
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from users.models import Role 

class Command(BaseCommand):
    help = "Seed the database with Ride and RideEvent data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        self.seed_roles()
        self.stdout.write("Seeding complete!")

    def seed_roles(self):
        if Role.objects.count() >= 10:
            self.stdout.write("Users already seeded.")
            return

        for i in range(10): 
            if i == 0:
                Role.objects.create(
                    name="admin",
                    description="Administrator",
                )
            else:
                Role.objects.create(
                    name=f"role_{i}",
                    description=f"user_{i}@example.com",
                )
        self.stdout.write("Roles seeded.")
