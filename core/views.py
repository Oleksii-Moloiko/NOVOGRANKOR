from django.shortcuts import render

from .models import Category


def home(request):
    categories = Category.objects.prefetch_related(
        "monuments"
    )

    return render(
        request,
        "home.html",
        {
            "categories": categories,
        }
    )