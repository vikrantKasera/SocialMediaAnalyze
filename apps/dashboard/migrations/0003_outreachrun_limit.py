from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0002_outreachrun_stop"),
    ]

    operations = [
        migrations.AddField(
            model_name="outreachrun",
            name="limit",
            field=models.PositiveIntegerField(default=1000),
        ),
    ]