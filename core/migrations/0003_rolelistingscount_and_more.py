# Generated by Django 5.0.6 on 2024-06-16 12:20

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_remove_roles_categories"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoleListingsCount",
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
            ],
        ),
        migrations.AddIndex(
            model_name="categories",
            index=models.Index(fields=["name"], name="core_catego_name_26485d_idx"),
        ),
        migrations.AddIndex(
            model_name="roles",
            index=models.Index(fields=["name"], name="core_roles_name_089fd0_idx"),
        ),
        migrations.AddIndex(
            model_name="technologies",
            index=models.Index(fields=["name"], name="core_techno_name_0ba523_idx"),
        ),
        migrations.AddField(
            model_name="rolelistingscount",
            name="role_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="core.roles"
            ),
        ),
    ]
