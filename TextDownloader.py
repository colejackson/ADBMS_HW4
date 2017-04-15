from json import loads
import urllib2

with open('books.json', 'r') as f:
    books = loads(f.read())

for book in books:

    book_id = book['book_id']

    url = 'http://www.gutenberg.org/cache/epub/{}/pg{}.txt'.format(book_id, book_id)
    file_path = 'books/{}.txt'.format(book_id)

    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print 'Failed #{}'.format(book_id)

    txt_file = response.read()

    with open(file_path, 'w+') as f:
        f.write(txt_file)

    print 'Downloaded Book #{}'.format(book_id)
