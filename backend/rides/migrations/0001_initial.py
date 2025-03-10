# Generated by Django 4.2.8 on 2024-12-10 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ride",
            fields=[
                ("id_ride", models.AutoField(primary_key=True, serialize=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("en-route", "En-Route"),
                            ("pickup", "Pickup"),
                            ("dropoff", "Dropoff"),
                        ],
                        default="en-route",
                        max_length=8,
                    ),
                ),
                ("pickup_latitude", models.FloatField(blank=True, null=True)),
                ("pickup_longitude", models.FloatField(blank=True, null=True)),
                ("dropoff_latitude", models.FloatField(blank=True, null=True)),
                ("dropoff_longitude", models.FloatField(blank=True, null=True)),
                ("pickup_time", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="RideEvent",
            fields=[
                ("id_ride_event", models.AutoField(primary_key=True, serialize=False)),
                ("description", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "id_ride",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rides.ride"
                    ),
                ),
            ],
        ),
    ]
