from lxml import html
import requests
from json import dumps
from re import search

book_count = 0
author_count = 0

book_pointer = 1

book_list = list()
author_list = list()

while book_count < 50:

    page = requests.get('http://www.gutenberg.org/ebooks/{}'.format(book_pointer))
    tree = html.fromstring(page.content)

    author_s = tree.xpath("//a[@itemprop='creator']/text()")
    title_s = tree.xpath("//td[@itemprop='headline']/text()")
    publish_date_s = tree.xpath("//td[@itemprop='datePublished']/text()")

    author_name = author_s[0] if len(author_s) > 0 else 'NO AUTHOR'
    title = title_s[0] if len(title_s) > 0 else 'NO TITLE'
    publish_date = publish_date_s[0] if len(publish_date_s) > 0 else 'NO PUBLISH DATE'

    try:
        print '\n\nACCEPT THIS BOOK?\n\n{}\n{}\n{}\n\n'.format(author_name, title, publish_date)
    except UnicodeEncodeError:
        book_pointer += 1
        continue

    result = raw_input('YES OR NO: ')

    if len(result) > 0 and result[0] == 'y':

        author_id = author_count

        author_name_str = search('([A-Za-z]+),(\s([A-Za-z.]+))+', author_name).group(0)
        author_birth_year = search('([0-9]+(?=-))', author_name).group(1)

        if any(auth['author_name'] == author_name_str for auth in author_list):

            for auth in author_list:

                if auth['author_name'] == author_name_str:

                    author_id = auth['author_id']

        else:

            author = dict()

            author['author_name'] = author_name_str
            author['year_of_birth'] = int(author_birth_year)
            author['author_id'] = author_id

            author_list.append(author)

            author_count += 1

        book = dict()

        book['book_id'] = book_pointer
        book['book_title'] = title.strip('\n')
        book['publish_date'] = publish_date
        book['author_id'] = author_id

        book_list.append(book)
        book_count += 1

    book_pointer += 1

with open('books.json', 'w+') as f:
    f.write(dumps(book_list, indent=4))

with open('authors.json', 'w+') as f:
    f.write(dumps(author_list, indent=4))
