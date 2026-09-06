from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("results", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OutreachRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("running", "Running"), ("completed", "Completed"), ("failed", "Failed")], default="running", max_length=20)),
                ("logs", models.JSONField(blank=True, default=list)),
                ("error", models.TextField(blank=True)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("result_file", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="outreach_runs", to="results.resultfile")),
            ],
            options={"ordering": ("-started_at",)},
        ),
    ]