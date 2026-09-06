import threading
import traceback

from django.db import close_old_connections
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.dashboard.models import OutreachRun
from apps.results.models import ResultFile

def outreach(request):
    return render(request, "dashboard/outreach.html", {
        "active_page": "outreach",
        "run": OutreachRun.objects.filter(status=OutreachRun.STATUS_RUNNING).first(),
    })

def start_outreach(request):
    if request.method != "POST":
        return redirect("youtube:outreach")

    running = OutreachRun.objects.filter(status=OutreachRun.STATUS_RUNNING).first()
    if running:
        return redirect("youtube:outreach")

    run = OutreachRun.objects.create(logs=[])
    thread = threading.Thread(target=_execute_outreach, args=(run.pk,), daemon=True)
    thread.start()
    return redirect("youtube:outreach")


def stop_outreach(request):
    if request.method == "POST":
        run = OutreachRun.objects.filter(status=OutreachRun.STATUS_RUNNING).first()
        if run:
            run.cancel_requested = True
            run.save(update_fields=["cancel_requested"])
    return redirect("youtube:outreach")


def outreach_status(request, run_id):
    run = OutreachRun.objects.get(pk=run_id)
    result_url = None
    if run.result_file_id:
        result_url = reverse("results:download", args=[run.result_file_id])
    return JsonResponse({
        "status": run.status,
        "logs": run.logs,
        "error": run.error,
        "result_url": result_url,
        "result_filename": run.result_file.filename if run.result_file_id else None,
    })


def _execute_outreach(run_id):
    from apps.youtube.tasks.async_scripts.extract_youtube_data import run_extraction

    close_old_connections()
    run = OutreachRun.objects.get(pk=run_id)
    print(f"[outreach:{run_id}] Background extraction started.", flush=True)

    def log(message):
        current_run = OutreachRun.objects.get(pk=run_id)
        if current_run.cancel_requested:
            raise RuntimeError("Outreach stopped by user.")
        timestamp = timezone.localtime().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(f"[outreach:{run_id}] {log_message}", flush=True)
        current_run.logs = [*current_run.logs, log_message]
        current_run.save(update_fields=["logs"])

    try:
        summary = run_extraction(progress_callback=log)
        if summary["filename"]:
            run.result_file = ResultFile.objects.get(filename=summary["filename"])
        run.status = OutreachRun.STATUS_COMPLETED
        run.completed_at = timezone.now()
        run.save(update_fields=["result_file", "status", "completed_at"])
    except Exception as error:
        print(f"[outreach:{run_id}] Background extraction failed: {type(error).__name__}: {error}", flush=True)
        traceback.print_exc()
        stopped = OutreachRun.objects.get(pk=run_id).cancel_requested
        run.status = OutreachRun.STATUS_STOPPED if stopped else OutreachRun.STATUS_FAILED
        run.error = "Outreach stopped by user." if stopped else str(error)
        run.completed_at = timezone.now()
        run.save(update_fields=["status", "error", "completed_at"])
        if stopped:
            current_logs = run.logs
            timestamp = timezone.localtime().strftime("%H:%M:%S")
            run.logs = [*current_logs, f"[{timestamp}] Outreach stopped by user."]
            run.save(update_fields=["logs"])
        else:
            log(f"Process failed: {error}")
    finally:
        close_old_connections()
