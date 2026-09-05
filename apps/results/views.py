from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from .models import ResultFile

def list_results(request):
    paginator = Paginator(ResultFile.objects.order_by("-created_at"), 15)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "results/list.html", {
        "results": page_obj,
        "active_page": "results",
    })

def download_result(request, pk):
    result = get_object_or_404(ResultFile, pk=pk)

    if not result.file:
        raise Http404("Result file is not available.")

    try:
        response = FileResponse(
            result.file.open("rb"),
            as_attachment=True,
            filename=result.filename or result.file.name.rsplit("/", 1)[-1],
        )
        return response
    except FileNotFoundError:
        raise Http404("Result file is not available.")
