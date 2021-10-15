import request

def get_stories(lat, long):
    url = 'http://www.mapquestapi.com/search/v2/radius'
    params = {'year': year, 'author': author}
    response = requests.get(url, params=params)
    stories = response.json()
