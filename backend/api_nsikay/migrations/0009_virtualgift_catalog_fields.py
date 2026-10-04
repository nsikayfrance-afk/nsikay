# Generated manually by NSIKAY on 2026-10-01.
# Adds the permanent VirtualGift catalogue structure.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_nsikay", "0008_alter_pagepromotionslot_page_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="virtualgift",
            name="slug",
            field=models.SlugField(
                max_length=180,
                unique=True,
                default="__temporary_virtualgift_migration__",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="virtualgift",
            name="value_eur",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=20,
                default=0.10,
            ),
        ),
        migrations.AddField(
            model_name="virtualgift",
            name="currency_reference",
            field=models.CharField(
                max_length=3,
                default="EUR",
            ),
        ),
        migrations.AddField(
            model_name="virtualgift",
            name="avatar",
            field=models.FileField(
                upload_to="gift_avatars/",
                blank=True,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="virtualgift",
            name="category",
            field=models.CharField(
                max_length=80,
                default="MINERAL",
            ),
        ),
        migrations.AddField(
            model_name="virtualgift",
            name="active",
            field=models.BooleanField(
                default=True,
            ),
        ),
        migrations.AddField(
            model_name="virtualgift",
            name="display_order",
            field=models.PositiveIntegerField(
                default=0,
            ),
        ),
        migrations.AddField(
            model_name="virtualgift",
            name="metadata",
            field=models.JSONField(
                default=dict,
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="virtualgift",
            name="currency",
            field=models.CharField(
                max_length=3,
                default="EUR",
            ),
        ),
        migrations.AlterField(
            model_name="virtualgift",
            name="name",
            field=models.CharField(
                max_length=150,
            ),
        ),
    ]