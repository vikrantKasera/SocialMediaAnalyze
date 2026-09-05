from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .models import SearchKeyword


def list_keywords(request):
    paginator = Paginator(SearchKeyword.objects.order_by("id"), 15)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "search_keywords/list.html", {
        "active_page": "search_keyword",
        "search_keywords": page_obj,
    })


def create_keyword(request):
    if request.method == "POST":
        keyword = (request.POST.get("keyword") or "").strip()
        is_active = request.POST.get("is_active") == "on"
        if keyword:
            SearchKeyword.objects.create(keyword=keyword, is_active=is_active)
            return redirect("search_keywords:list")

    return render(request, "search_keywords/form.html", {
        "active_page": "search_keyword",
        "object": None,
        "keyword": request.POST.get("keyword", "") if request.method == "POST" else "",
        "is_active": request.POST.get("is_active") == "on" if request.method == "POST" else True,
        "error": "Please provide a valid keyword." if request.method == "POST" else "",
    })


def edit_keyword(request, pk):
    obj = get_object_or_404(SearchKeyword, pk=pk)

    if request.method == "POST":
        keyword = (request.POST.get("keyword") or "").strip()
        is_active = request.POST.get("is_active") == "on"
        if keyword:
            obj.keyword = keyword
            obj.is_active = is_active
            obj.save()
            return redirect("search_keywords:list")

    return render(request, "search_keywords/form.html", {
        "object": obj,
        "keyword": obj.keyword,
        "is_active": obj.is_active,
        "active_page": "search_keyword",
        "error": "Please provide a valid keyword." if request.method == "POST" else "",
    })


def delete_keyword(request, pk):
    obj = get_object_or_404(SearchKeyword, pk=pk)
    if request.method == "POST":
        obj.delete()
    return redirect("search_keywords:list")
