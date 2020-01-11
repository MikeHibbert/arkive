import htmlark
import bs4


def create_tag(og_type, content, soup):
    tag = soup.new_tag('meta', property=og_type, content=content)

    return tag


def create_tag_from(tag, soup):
    og_tag = None
    if tag.name.lower() == 'img':
        return create_tag('og:image', tag['src'], soup)

    if tag.name.lower() == 'meta':
        name = tag.get('name', '').lower()
        if name == 'description':
            return create_tag('og:description', tag['content'], soup)

    if tag.name.lower() == 'title':
        return create_tag('og:title', tag.contents[0], soup)

    return og_tag


def add_all_og_tags(html):
    parser = htmlark.get_available_parsers()[0]
    soup = bs4.BeautifulSoup(html, parser=parser)

    for meta in soup('meta'):
        name = meta.get('name', '')
        if name == 'description':
            og_description = create_tag_from(meta, soup)
            soup.head.append(og_description)

    for tag in soup('title'):
        og_title = create_tag_from(tag, soup)
        soup.head.append(og_title)

    images = soup('img')

    for image in images:
        tag = create_tag_from(image, soup)
        soup.head.append(tag)

    return str(soup)


def add_og_tags_to_page_at(url, save_file="og_webpage.html"):
    _, html = htmlark._get_resource(url)

    add_og_tage_to_page(html, save_file)


def add_og_tage_to_page(html, save_file):
    html = add_all_og_tags(html)

    with open(save_file, 'w') as sf:
        sf.write(html)

        sf.close()


if __name__ == "__main__":
    import arrow

    save_file = "og_webpage-{}.html".format(arrow.now().timestamp)
    add_og_tags_to_page_at('https://www.bbc.co.uk/news/world-africa-51063149', save_file)

    packed_html = htmlark.convert_page(save_file, ignore_errors=True)

    with open(save_file, 'w') as sf:
        sf.write(packed_html)