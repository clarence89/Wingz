import random
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from users.models import User
from rides.models import Ride, RideEvent
from datetime import  timedelta
from django.utils import timezone
from users.models import Role


class Command(BaseCommand):
    help = "Seed the database with Ride and RideEvent data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        self.seed_users()
        self.seed_rides()
        self.stdout.write("Seeding complete!")

    def seed_users(self):
        if User.objects.count() >= 10:
            self.stdout.write("Users already seeded.")
            return

        for i in range(10): 
            role = random.choice(Role.objects.all())
            first_name = random.choice(["John", "Jane", "Jim", "Jill", "Jack"])
            last_name = random.choice(["Doe", "Smith", "Johnson", "Williams", "Jones"])
            User.objects.create_user(
                username=f"user_{i}",
                email=f"user_{i}@example.com",
                password="password123",
                first_name=first_name,
                last_name=last_name,
                role=role
            )
        self.stdout.write("Users seeded.")

    def seed_rides(self):
        users = User.objects.all()
        if users.count() < 2:
            self.stdout.write("Not enough users to seed rides.")
            return

        riders = users[:5] 
        drivers = users[5:] 

        for i in range(10): 
            ride = Ride.objects.create(
                rider=random.choice(riders),
                driver=random.choice(drivers),
                status=random.choice(["en-route", "pickup", "dropoff"]),
                pickup_latitude=random.uniform(-90, 90),
                pickup_longitude=random.uniform(-180, 180),
                dropoff_latitude=random.uniform(-90, 90),
                dropoff_longitude=random.uniform(-180, 180),
                pickup_time=now(),
            )
            self.seed_ride_events(ride)

        self.stdout.write("Rides seeded.")



    def seed_ride_events(self, ride):
        possible_statuses = ["en-route", "pickup", "dropoff"]

        time_adjusted = timezone.now()
        for status in possible_statuses:
            time_adjusted += timedelta(
                minutes=random.choice([-1, 1]) * random.randint(0, 59),
                hours=random.choice([-1, 1]) * random.randint(0, 1),
            )
            print(f"Creating event for {status} at {time_adjusted}")

            ride_event = RideEvent.objects.create(
                ride=ride,
                description=f"Status Changed to {status}",
            )
            
            ride_event.created_at = time_adjusted
            ride_event.save()
            if status == ride.status:
                time_adjusted = timezone.now()
                break



        self.stdout.write(f"Events seeded for Ride {ride.id_ride}.")
