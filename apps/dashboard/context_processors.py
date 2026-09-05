def sidebar_context(request):
    recent_results = []
    try:
        from apps.results.models import ResultFile
        recent_results = ResultFile.objects.order_by("-created_at")[:3]
    except Exception:
        pass

    return {
        "limit": request.session.get("limit", 1000),
        "recent_results": recent_results,
    }
