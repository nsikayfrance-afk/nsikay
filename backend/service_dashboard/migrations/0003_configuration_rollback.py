from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service_dashboard", "0002_operationalcountryconfigurationlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="operationalcountryconfigurationlog",
            name="rolled_back",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="operationalcountryconfigurationlog",
            name="rolled_back_at",
            field=models.DateTimeField(
                blank=True,
                null=True
            ),
        ),
        migrations.AddField(
            model_name="operationalcountryconfigurationlog",
            name="rolled_back_by",
            field=models.CharField(
                blank=True,
                max_length=150,
                null=True
            ),
        ),
        migrations.AddField(
            model_name="operationalcountryconfigurationlog",
            name="rollback_reason",
            field=models.TextField(
                blank=True,
                null=True
            ),
        ),
        migrations.AddIndex(
            model_name="operationalcountryconfigurationlog",
            index=models.Index(
                fields=["rolled_back"],
                name="service_das_rolled__550544_idx",
            ),
        ),
        migrations.CreateModel(
            name="OperationalCountryConfigurationSnapshot",
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
                    "previous_operational_codes",
                    models.TextField(
                        blank=True,
                        default="",
                    ),
                ),
                (
                    "previous_operational_count",
                    models.PositiveIntegerField(
                        default=0,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                    ),
                ),
                (
                    "configuration_log",
                    models.OneToOneField(
                        on_delete=models.deletion.CASCADE,
                        related_name="snapshot",
                        to="service_dashboard.operationalcountryconfigurationlog",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]

