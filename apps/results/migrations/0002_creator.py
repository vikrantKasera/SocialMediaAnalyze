from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("results", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Creator",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("channel_id", models.CharField(max_length=100, unique=True)),
                ("channel_name", models.CharField(max_length=255)),
                ("channel_url", models.URLField(max_length=500)),
                ("custom_url", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("country", models.CharField(blank=True, max_length=100)),
                ("subscribers", models.PositiveBigIntegerField(blank=True, null=True)),
                ("average_recent_views", models.PositiveBigIntegerField(default=0)),
                ("days_since_oldest_video", models.PositiveIntegerField(default=0)),
                ("engagement_flags", models.JSONField(blank=True, default=list)),
                ("recent_videos", models.JSONField(blank=True, default=list)),
                ("search_keywords", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]