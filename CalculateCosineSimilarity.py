from json import loads, dumps
from re import findall
from math import sqrt


def cosine_similarity(vec1, vec2):

    vec1_sum = sum(i*i for i in vec1)
    vec2_sum = sum(i*i for i in vec2)

    dot_product = sum(i[0] * i[1] for i in zip(vec1, vec2))

    return dot_product/(sqrt(vec1_sum)*sqrt(vec2_sum))


if __name__ == '__main__':

    word_count = 0

    master_dict = dict()

    book_vectors = dict()

    similarities = list()

    with open('stopwords.txt', 'r') as f:

        stop_words = f.read().upper().split('\n')

    with open('books.json', 'r') as f:

        books = loads(f.read())

    for book in books:

        vector = list()

        print "Starting {}\n\n".format(book['book_title'])

        with open('books/{}.txt'.format(book['book_id'])) as f:

            for w in findall("(([A-Za-z'])+)", f.read()):

                word = w[0].upper()

                if word in stop_words:

                    continue

                if word not in master_dict.keys():

                    master_dict[word] = word_count
                    word_count += 1

                index = master_dict[word]

                if index >= len(vector):
                    vector.extend([0] * (index + 1 - len(vector)))

                vector[index] += 1

        print "Finished #{}: {}\n\n".format(book['book_id'], book['book_title'])

        book_vectors[book['book_id']] = vector

    max_len = 0

    for tup in book_vectors.iteritems():

        if len(tup[1]) > max_len:

            max_len = len(tup[1])

    for key in book_vectors.keys():

        if len(book_vectors[key]) == max_len:
            continue

        if max_len >= len(book_vectors[key]):
            book_vectors[key].extend([0] * (max_len - len(book_vectors[key])))

    for book_1 in books:

        for book_2 in books:

            if book_1 == book_2:

                continue

            similarity = dict()

            similarity['first_book_id'] = book_1['book_id']
            similarity['second_book_id'] = book_2['book_id']
            similarity['cosine_similarity'] = cosine_similarity(book_vectors[book_1['book_id']],
                                                                book_vectors[book_2['book_id']])

            similarities.append(similarity)

    with open('similarities.json', 'w+') as f:

        f.write(dumps(similarities, indent=4))
