from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posting_criteria", "0002_postingcriteria_search_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="postingcriteria",
            name="max_creators",
            field=models.PositiveIntegerField(default=1000),
        ),
    ]