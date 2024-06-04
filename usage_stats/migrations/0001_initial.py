# Generated by Django 5.0.6 on 2024-06-04 15:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AggregatedTechCounts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "counter",
                    models.IntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "role_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.roles"
                    ),
                ),
                (
                    "technology_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.technologies",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalTechCounts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "counter",
                    models.IntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "role_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.roles"
                    ),
                ),
                (
                    "technology_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.technologies",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MonthlyTechnologiesCounts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "counter",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "role_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.roles"
                    ),
                ),
                (
                    "technology_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.technologies",
                    ),
                ),
            ],
        ),
    ]
