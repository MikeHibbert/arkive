import os
from django.conf import settings
from celery import task
from arkiver.helpers import get_newspaper, create_archive_page, create_readable_page, upload_file_to_arweave


@task
def create_archive_page_task(self, list_of_work, progress_observer, url, tags):
    save_file = create_archive_page(url)

    upload_file_to_arweave(save_file, url, tags)


@task
def create_readable_page_task(self, list_of_work, progress_observer, url, tags, include_images):
    save_file = create_readable_page(url, include_images)

    upload_file_to_arweave(save_file, url, tags)


