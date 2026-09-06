from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posting_criteria", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="postingcriteria",
            name="result_per_keyword",
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name="postingcriteria",
            name="per_page_keyword",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="postingcriteria",
            name="video_to_check",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="postingcriteria",
            name="recent_days",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="postingcriteria",
            name="shorts_max_second",
            field=models.PositiveIntegerField(default=1),
        ),
    ]