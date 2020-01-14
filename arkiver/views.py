from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import URLForm, PublishOptionsForm
from .helpers import get_newspaper
from arkive.tasks import create_archive_page_task, create_readable_page_task


def home(request):
    return render(request, 'home.html')


def get_content(request):
    if request.method == "POST":
        form = URLForm(request.POST)

        if form.is_valid():
            newspaper = get_newspaper(form.cleaned_data.get('url'))
        else:
            messages.error(request, "URL not valid")

    return render(request, 'processed-page.html', locals())


def set_options(request):
    if request.method == "POST":
        form = URLForm(request.POST)

        if form.is_valid():
            newspaper = get_newspaper(form.cleaned_data.get('url'))
        else:
            messages.error(request, "URL not valid")

    return render(request, 'processed-page.html', locals())


def publish_page(request):
    if request.method == "POST":
        form = PublishOptionsForm(request.POST)
        if form.is_valid():
            publish_as = form.cleaned_data['publish_as']
            url = form.cleaned_data['url']

            if publish_as == 'readable':
                save_file = create_readable_page_task(url)
            if publish_as == 'archive':
                save_file = create_archive_page_task(url)

    return render(request, 'published-page.html', locals())
