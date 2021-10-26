import pytest

@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [('authorization', 'DUMMY')],
        "filter_query_parameters": [('key', 'DUMMY')],
        "filter_post_data_parameters": [('key', 'DUMMY')]
    }
    