from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0001_outreachrun"),
    ]

    operations = [
        migrations.AddField(
            model_name="outreachrun",
            name="cancel_requested",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="outreachrun",
            name="status",
            field=models.CharField(
                choices=[
                    ("running", "Running"),
                    ("completed", "Completed"),
                    ("failed", "Failed"),
                    ("stopped", "Stopped"),
                ],
                default="running",
                max_length=20,
            ),
        ),
    ]