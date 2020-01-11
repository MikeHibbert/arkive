import os
import arrow
import htmlark
import bs4
from newspaper import Article, ArticleException
from opengraph_tags import add_og_tags_to_page_at
from django.conf import settings


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


def create_readable_page(url):
    newspaper = get_newspaper(url)

    html_template = os.path.join(settings.BASE_DIR, 'arkiver', "templates", 'readable-template.html')

    html = ''
    with open(html_template, 'r') as htmlt:
        html = htmlt.read()

    parser = htmlark.get_available_parsers()[0]
    soup = bs4.BeautifulSoup(html, parser=parser)

    # TODO: add in all title, description, images and og tags and all copy

    save_file = os.path.join(settings.BASE_DIR, 'pages', "{}.html".format(arrow.now().timestamp))

    add_og_tags_to_page_at(url, save_file)

    html = str(soup)

    with open(save_file, 'w') as sf:
        sf.write(html)

    return save_file
