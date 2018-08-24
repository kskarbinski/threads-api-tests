from requests import session

from api_tests_framework.utils.helpers import generate_random_words, generate_random_name, generate_random_string


class Actor(object):
    def __init__(self):
        self.session = session()

        # Generate actor details
        self.firstname = generate_random_words()
        self.lastname = generate_random_words()
        self.username = generate_random_name()
        self.password = generate_random_string(5, 15)
