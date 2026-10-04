from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nsikay_profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="nsikayprofile",
            name="specialized_data",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
    ]

