from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("access_keys", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="accesskey",
            name="quota_exhausted_on",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="accesskey",
            name="quota_limit",
            field=models.PositiveIntegerField(default=10000),
        ),
    ]