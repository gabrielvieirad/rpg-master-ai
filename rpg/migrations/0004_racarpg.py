# Generated by Django 5.1.5 on 2025-04-01 00:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_cachelog"),
        ("rpg", "0003_classerpg"),
    ]

    operations = [
        migrations.CreateModel(
            name="RacaRPG",
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
                ("nome", models.CharField(max_length=255)),
                ("descricao", models.TextField()),
                ("modificadores_atributos", models.JSONField(blank=True, default=dict)),
                ("habilidades", models.TextField(blank=True, null=True)),
                ("idiomas", models.TextField(blank=True, null=True)),
                ("tamanho", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "deslocamento",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                (
                    "sistema",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="racas",
                        to="api.sistemarpg",
                    ),
                ),
            ],
        ),
    ]
