from django.shortcuts import redirect, render
from .models import PostingCriteria


def edit_criteria(request):
    obj = PostingCriteria.objects.order_by("-updated_at").first()

    if obj is None:
        obj = PostingCriteria.objects.create()

    if request.method == "POST":
        obj.min_subscribers = int(request.POST.get("min_subscribers") or obj.min_subscribers or 0)
        obj.max_subscribers = int(request.POST.get("max_subscribers") or obj.max_subscribers or 0)
        obj.min_views = int(request.POST.get("min_views") or obj.min_views or 0)
        obj.max_days_since_posting = int(request.POST.get("max_days_since_posting") or obj.max_days_since_posting or 0)
        obj.additional_criteria = request.POST.get("additional_criteria", "")
        obj.result_per_keyword = int(request.POST.get("result_per_keyword") or obj.result_per_keyword or 1)
        obj.per_page_keyword = int(request.POST.get("per_page_keyword") or obj.per_page_keyword or 1)
        obj.video_to_check = int(request.POST.get("video_to_check") or obj.video_to_check or 1)
        obj.recent_days = int(request.POST.get("recent_days") or obj.recent_days or 1)
        obj.shorts_max_second = int(request.POST.get("shorts_max_second") or obj.shorts_max_second or 1)

        obj.is_active = request.POST.get("is_active") == "on"
        obj.save()
        return redirect("posting_criteria:edit")

    return render(request, "posting_criteria/form.html", {
        "object": obj,
        "active_page": "posting_criteria",
    })
