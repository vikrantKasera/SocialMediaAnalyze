def sidebar_context(request):
    recent_results = []
    limit = 1000
    try:
        from apps.results.models import ResultFile
        from apps.posting_criteria.models import PostingCriteria
        recent_results = ResultFile.objects.order_by("-created_at")[:3]
        criteria = PostingCriteria.objects.filter(is_active=True).order_by("-updated_at").first()
        if criteria:
            limit = criteria.max_creators
    except Exception:
        pass

    return {
        "limit": limit,
        "recent_results": recent_results,
    }
