import htmlark

packed_html = htmlark.convert_page('https://www.bbc.co.uk/news/world-africa-51063149', ignore_errors=True)

f = open('htmlark_test.html', 'w')
f.write(packed_html)
f.close()