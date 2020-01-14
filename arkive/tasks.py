import os
from django.conf import settings
from celery import task
from arkiver.helpers import get_newspaper, create_archive_page, create_readable_page, upload_file_to_arweave


@task
def create_archive_page_task(url, tags):
    save_file = create_archive_page(url)

    upload_file_to_arweave(save_file)


@task
def create_readable_page_task(url, tags):
    save_file = create_readable_page(url)

    upload_file_to_arweave(save_file)


