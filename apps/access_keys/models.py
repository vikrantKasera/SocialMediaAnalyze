from django.db import models

class AccessKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def masked_key(self):
        if not self.key:
            return ""
        if len(self.key) <= 12:
            return "*" * len(self.key)
        return f"{self.key[:7]}{'*' * max(6, len(self.key) - 11)}{self.key[-4:]}"

    def __str__(self):
        return self.masked_key
