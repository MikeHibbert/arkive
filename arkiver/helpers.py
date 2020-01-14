import os
from os import listdir
from os.path import isfile, join
import arrow
import htmlark
import bs4
import logging
from arweave import Transaction, Wallet
from newspaper import Article, ArticleException
from opengraph_tags import add_og_tags_to_page_at
from django.conf import settings

logger = logging.getLogger(__name__)


def upload_file_to_arweave(filepath, url, tags):
    wallet_path = os.path.join(settings.BASE_DIR, 'wallet')

    files = [f for f in listdir(wallet_path) if isfile(join(wallet_path, f))]

    if len(files) > 0:
        filename = files[0]
    else:
        raise FileNotFoundError("Unable to load a wallet JSON file from wallet/ ")

    wallet_path = join(wallet_path, filename)

    wallet = Wallet(wallet_path)

    tx_id = None

    try:
        with open(filepath, 'r') as file_to_upload:
            data = file_to_upload.read()

            tx = Transaction(wallet, data=data.encode())

            tx.add_tag("app", "Arkive")
            tx.add_tag('created', str(arrow.now().timestamp))
            tx.add_tag('url', url)

            for tag in tags:
                tx.add_tag("keyword", tag['keyword'])

            tx.sign(wallet)

            tx.post()

            tx_id = tx.id.decode()

    except Exception as e:
        logger.debug(e)

    return tx_id





def get_newspaper(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        article.nlp()

    except ArticleException as ae:
        article = None

    return article


def create_archive_page(url):
    save_file = os.path.join(settings.BASE_DIR, 'pages', "{}.html".format(arrow.now().timestamp))
    add_og_tags_to_page_at(url, save_file)

    packed_html = htmlark.convert_page(save_file, ignore_errors=True)

    with open(save_file, 'w') as sf:
        sf.write(packed_html)

    return save_file


def create_readable_page(url, include_images):
    newspaper = get_newspaper(url)

    html_template = os.path.join(settings.BASE_DIR, 'arkiver', "templates", 'readable-template.html')

    html = ''
    with open(html_template, 'r') as htmlt:
        html = htmlt.read()

    parser = htmlark.get_available_parsers()[0]
    soup = bs4.BeautifulSoup(html, parser=parser)

    # TODO: add in all title, description, images and og_tags and all copy

    save_file = os.path.join(settings.BASE_DIR, 'pages', "{}.html".format(arrow.now().timestamp))

    add_og_tags_to_page_at(url, save_file)

    html = str(soup)

    with open(save_file, 'w') as sf:
        sf.write(html)

    return save_file
