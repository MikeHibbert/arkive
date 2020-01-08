from newspaper import Article, ArticleException


def get_newspaper(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        article.nlp()

    except ArticleException as ae:
        article = None

    return article


def create_single_page(url):
    pass