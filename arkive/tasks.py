import os
import logging
from django.conf import settings
from celery import task
from arkiver.helpers import get_newspaper, create_archive_page, create_readable_page, upload_file_to_arweave

logger = logging.getLogger(__name__)

@task()
def test_celery():
    return "it works!"


@task(bind=True)
def create_archive_page_task(self, url, tags):
    save_file = create_archive_page(url)

    self.update_state(state='PROGRESS', meta={'current': 1, 'total': 3, 'tx_id': 'none'})
    transaction = upload_file_to_arweave(save_file, url, tags)

    logger.debug(transaction.id)

    self.update_state(state='PROGRESS', meta={'current': 2, 'total': 3, 'tx_id': transaction.id.decode("utf-8")})

    while transaction.status != "PENDING":
        transaction.get_status()

    self.update_state(state='PROGRESS', meta={'current': 3, 'total': 3, 'tx_id': transaction.id.decode("utf-8")})

    return "tx_id: {}".format(transaction.id)


@task(bind=True)
def create_readable_page_task(self, url, tags, include_images):
    save_file = create_readable_page(url, include_images)
    self.update_state(state='PROGRESS', meta={'current': 1, 'total': 3, 'tx_id': 'none'})

    transaction = upload_file_to_arweave(save_file, url, tags)
    self.update_state(state='PROGRESS', meta={'current': 2, 'total': 3, 'tx_id': transaction.id.decode("utf-8")})

    while transaction.status != "PENDING":
        transaction.get_status()

    self.update_state(state='PROGRESS', meta={'current': 3, 'total': 3, 'tx_id': transaction.id.decode("utf-8")})

    return "tx_id: {}".format(transaction.id)


