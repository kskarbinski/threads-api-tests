from random import choice, randint
from uuid import uuid4
from string import ascii_letters

from api_tests_framework.utils.helpers import nouns


def generate_random_words(min_words=1, max_words=1):
    words = [choice(nouns) for _ in xrange(randint(min_words, max_words))]
    return unicode(" ".join(words))


def generate_random_name():
    username = generate_random_words() + "_" + unicode(uuid4().hex)[:8]
    return unicode(username)


def generate_random_string(min_chars=1, max_chars=5):
    chars = [choice(ascii_letters) for _ in xrange(randint(min_chars, max_chars))]
    return unicode("".join(chars))
