from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .models import AccessKey


def list_keys(request):
    paginator = Paginator(AccessKey.objects.order_by("-created_at"), 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "access_keys/list.html", {
        "active_page": "access_key",
        "page_obj": page_obj,
        "access_keys": page_obj,
    })


def create_key(request):
    if request.method == "POST":
        key = (request.POST.get("key") or "").strip()
        is_active = request.POST.get("is_active") == "on"
        if key:
            AccessKey.objects.create(key=key, is_active=is_active)
            return redirect("access_keys:list")

    return render(request, "access_keys/form.html", {
        "active_page": "access_key",
        "object": None,
        "key": request.POST.get("key", "") if request.method == "POST" else "",
        "is_active": request.POST.get("is_active") == "on" if request.method == "POST" else True,
        "error": "Please provide a valid API key." if request.method == "POST" else "",
    })


def edit_key(request, pk):
    obj = get_object_or_404(AccessKey, pk=pk)

    if request.method == "POST":
        key = (request.POST.get("key") or "").strip()
        is_active = request.POST.get("is_active") == "on"
        if key:
            obj.key = key
            obj.is_active = is_active
            obj.save()
            return redirect("access_keys:list")

    return render(request, "access_keys/form.html", {
        "object": obj,
        "key": obj.key,
        "is_active": obj.is_active,
        "active_page": "access_key",
        "error": "Please provide a valid API key." if request.method == "POST" else "",
    })


def delete_key(request, pk):
    obj = get_object_or_404(AccessKey, pk=pk)
    if request.method == "POST":
        obj.delete()
    return redirect("access_keys:list")
