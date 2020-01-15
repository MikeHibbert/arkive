import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import URLForm, PublishOptionsForm
from celery.result import AsyncResult
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
            return redirect(reverse('index'))

    return render(request, 'processed-page.html', locals())


def set_options(request):
    if request.method == "POST":
        form = PublishOptionsForm(request.POST)

        if form.is_valid():
            newspaper = get_newspaper(form.cleaned_data.get('url'))
        else:
            messages.error(request, "There was an error processing your page. Please try again.")
            return redirect(reverse('index'))

    return render(request, 'processed-page.html', locals())


def publish_page(request):
    if request.method == "POST":
        form = PublishOptionsForm(request.POST)
        if form.is_valid():
            publish_as = form.cleaned_data['publish_as']
            url = form.cleaned_data['url']
            tags = form.cleaned_data['tags']

            if len(tags) > 0:
                tags = json.loads(tags)
                tags = [{'keyword': keyword['value']} for keyword in tags]

            include_images = form.cleaned_data['include_images']

            if publish_as == 'readable':
                res = create_readable_page_task.delay(url, tags, include_images)
            if publish_as == 'archive':
                res = create_archive_page_task.delay(url, tags)

            task_id = res.id

    return render(request, 'published-page.html', locals())


def get_task_progress(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        'state': result.state,
        'details': result.info,
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
