from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import URLForm
from .helpers import get_newspaper


def home(request):
    return render(request, 'home.html')


def get_content(request):
    if request.method == "POST":
        form = URLForm(request.POST)

        if form.is_valid():
            article = get_newspaper(form.cleaned_data.get('url'))
        else:
            messages.error(request, "URL not valid")

    return render(request, 'processed-page.html', locals())