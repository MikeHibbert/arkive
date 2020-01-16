import os
from os import listdir
from os.path import isfile, join
import arrow
import htmlark
import bs4
import logging
from arweave import Transaction, Wallet
from newspaper import Article, ArticleException
from opengraph_tags import add_og_tags_to_page_at, add_og_tage_to_page
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

    tx = {id: None}

    logger.error("Loading {}",format(filepath))

    with open(filepath, 'r') as file_to_upload:
        logger.error("Loaded {}", format(filepath))
        data = file_to_upload.read()

        tx = Transaction(wallet, data=data.encode())

        tx.add_tag("app", "Arkive")
        tx.add_tag('created', str(arrow.now().timestamp))
        tx.add_tag('url', url)

        for tag in tags:
            tx.add_tag("keyword", tag['keyword'])

        tx.sign(wallet)

        tx.post()

    return tx





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

        html = html.replace('{{newspaper.title}}', newspaper.title)
        html = html.replace('{{newspaper.top_image}}', newspaper.top_image)
        html = html.replace('{{newspaper.text}}', newspaper.text)
        html = html.replace('{{newspaper.authors}}', ",".join(newspaper.authors))
        html = html.replace('{{newspaper.keywords}}', ",".join(newspaper.keywords))
        html = html.replace('{{newspaper.summary}}', newspaper.summary)

        save_file = os.path.join(settings.BASE_DIR, 'pages', "{}.html".format(arrow.now().timestamp))

        add_og_tage_to_page(html, save_file)

    return save_file
