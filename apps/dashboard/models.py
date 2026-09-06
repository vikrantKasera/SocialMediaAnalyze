from django.db import models


class OutreachRun(models.Model):
	STATUS_RUNNING = "running"
	STATUS_COMPLETED = "completed"
	STATUS_FAILED = "failed"
	STATUS_STOPPED = "stopped"
	STATUS_CHOICES = (
		(STATUS_RUNNING, "Running"),
		(STATUS_COMPLETED, "Completed"),
		(STATUS_FAILED, "Failed"),
		(STATUS_STOPPED, "Stopped"),
	)

	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_RUNNING)
	logs = models.JSONField(default=list, blank=True)
	result_file = models.ForeignKey(
		"results.ResultFile",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="outreach_runs",
	)
	error = models.TextField(blank=True)
	cancel_requested = models.BooleanField(default=False)
	started_at = models.DateTimeField(auto_now_add=True)
	completed_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ("-started_at",)
