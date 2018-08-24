# Define shell
SHELL = /bin/bash

# Add paths
API_TESTS_PATH = $(abspath .)
PYTHONPATH := $(API_TESTS_PATH):$(PYTHONPATH)
PATH := $(API_TESTS_PATH):$(PATH)

export PYTHONPATH
export PATH

test:
	# pytest -s api_tests/thread/test_kick_user_from_thread.py::KickUserFromThreadTestSuite::test_kick_single_user_from_thread_as_thread_owner
	pytest -s api_tests
