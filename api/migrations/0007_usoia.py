# Generated by Django 5.1.5 on 2025-03-03 22:36

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_historiagerada"),
    ]

    operations = [
        migrations.CreateModel(
            name="UsoIA",
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
                ("quantidade_requisicoes", models.IntegerField(default=0)),
                (
                    "ultimo_reset",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
