# Define shell
SHELL = /bin/bash

# Add paths
API_TESTS_PATH = $(abspath .)
PYTHONPATH := $(API_TESTS_PATH):$(PYTHONPATH)
PATH := $(API_TESTS_PATH):$(PATH)

export PYTHONPATH
export PATH

test:
	# pytest -s api_tests/user/test_get_users.py::GetUserTestSuite::test_get_users
	pytest -s api_tests
