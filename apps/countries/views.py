from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .models import Country


def list_countries(request):
    paginator = Paginator(Country.objects.order_by("name"), 15)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "countries/list.html", {
        "active_page": "countries",
        "countries": page_obj,
    })


def create_country(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        code = (request.POST.get("code") or "").strip()
        is_active = request.POST.get("is_active") == "on"
        if name and code:
            Country.objects.create(name=name, code=code, is_active=is_active)
            return redirect("countries:list")

    return render(request, "countries/form.html", {
        "active_page": "countries",
        "object": None,
        "name": request.POST.get("name", "") if request.method == "POST" else "",
        "code": request.POST.get("code", "") if request.method == "POST" else "",
        "is_active": request.POST.get("is_active") == "on" if request.method == "POST" else True,
        "error": "Please fill in the country name and code." if request.method == "POST" else "",
    })


def edit_country(request, pk):
    obj = get_object_or_404(Country, pk=pk)

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        code = (request.POST.get("code") or "").strip()
        is_active = request.POST.get("is_active") == "on"
        if name and code:
            obj.name = name
            obj.code = code
            obj.is_active = is_active
            obj.save()
            return redirect("countries:list")

    return render(request, "countries/form.html", {
        "object": obj,
        "name": obj.name,
        "code": obj.code,
        "is_active": obj.is_active,
        "active_page": "countries",
        "error": "Please fill in the country name and code." if request.method == "POST" else "",
    })


def delete_country(request, pk):
    obj = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        obj.delete()
    return redirect("countries:list")
