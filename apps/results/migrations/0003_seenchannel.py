from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("results", "0002_creator"),
    ]

    operations = [
        migrations.CreateModel(
            name="SeenChannel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("channel_id", models.CharField(max_length=100, unique=True)),
                ("first_seen_at", models.DateTimeField(auto_now_add=True)),
                ("last_seen_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]