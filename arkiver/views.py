from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def process_page(request):
    return render(request, 'processed-page.html')