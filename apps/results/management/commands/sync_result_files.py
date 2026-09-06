"""Register result workbooks that already exist in MEDIA_ROOT/results."""

from pathlib import Path
from datetime import timezone as datetime_timezone

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.results.models import ResultFile


class Command(BaseCommand):
    help = "Create ResultFile records for workbooks already present in media/results."

    def handle(self, *args, **options):
        results_dir = Path(settings.MEDIA_ROOT) / "results"
        created = 0
        for path in sorted(results_dir.glob("*.xlsx")):
            relative_name = f"results/{path.name}"
            result, was_created = ResultFile.objects.get_or_create(
                file=relative_name,
                defaults={"filename": path.name},
            )
            if was_created:
                timestamp = timezone.datetime.fromtimestamp(path.stat().st_mtime, tz=datetime_timezone.utc)
                ResultFile.objects.filter(pk=result.pk).update(created_at=timestamp)
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Registered {created} result file(s)."))