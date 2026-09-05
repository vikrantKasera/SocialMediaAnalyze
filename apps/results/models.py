from pathlib import Path
from django.db import models

class ResultFile(models.Model):
    file = models.FileField(upload_to="results/")
    filename = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and not self.filename:
            self.filename = Path(self.file.name).name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filename
