import pytest

@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [('authorization', 'DUMMY')],
        "filter_query_parameters": [('key', 'DUMMY')],
        "filter_post_data_parameters": [('key', 'DUMMY')]
    }

# with my_vcr.use_cassette('test.yml', filter_query_parameters=['api_key']):
#     requests.get('http://api.com/getdata?api_key=secretstring')

# with my_vcr.use_cassette('test.yml', filter_post_data_parameters=['client_secret']):
#     requests.post('http://api.com/postdata', data={'api_key': 'secretstring'})