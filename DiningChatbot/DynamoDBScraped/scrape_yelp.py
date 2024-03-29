from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib

# For Python 3.0 and later
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

# Yelp API Key
import secrets
API_KEY = secrets.yelp_api_key

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def search(api_key, url_params):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = url_params
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)

# app constants
CUISINES = ['American', 'Chinese', 'Japanese', 'Italian', 'Mexican', 'Indian', 'Thai', 'Greek']

def main():
    """Scrape 5000+ restaurants from Yelp in 8 cuisine types:
       'American', 'Chinese', 'Japanese', 'Italian', 'Mexican', 'Indian', 'Thai', 'Greek'
    """
    # search for restaurants in each cuisine type
    businesses_all = dict()
    id_set = set()
    for cuisine in CUISINES:
        print("Processing request for {}...".format(cuisine))
        businesses_all[cuisine] = list()
        # define search parameters
        term = cuisine + ' restaurants'
        location = 'Manhattan, NY'
        for i in range(20):
            search_limit = 50
            offset = 50*i
            url_params = {
                'term': term.replace(' ', '+'),
                'location': location.replace(' ', '+'),
                'limit': search_limit,
                'offset': offset
            }
            # get business search response
            response = search(API_KEY, url_params)
            # check for duplicates
            for buz in response['businesses']:
                if buz['id'] not in id_set:
                    businesses_all[cuisine].append(buz)
                    id_set.add(buz['id'])
            print("Query {}/20 complete".format(i+1))

    # save to json file
    save_file = '../data/businesses_raw.json'
    json.dump(businesses_all, open(save_file, "w"))

if __name__ == '__main__':
    main()