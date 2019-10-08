from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk
from requests_aws4auth import AWS4Auth
import json

import secrets

HOST = secrets.es_host
AUTH = AWS4Auth(secrets.aws_access_key_id, secrets.aws_secret_access_key, 'us-east-1', 'es')

def create_index(es, index_name):
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "type": {
                    "type": "keyword"
                },
                "restaurant_id": {
                    "type": "text"
                },
                "cuisine": {
                    "type": "text"
                },
            }
        }
    }

    try:
        if not es.indices.exists(index_name):
            es.indices.create(index=index_name, body=settings)
            print('Created index with name: {}'.format(index_name))
        else:
            print('Index with name {} already exist: '.format(index_name))
            print(es.indices.get(index=index_name), '\n')
    except Exception as e:
        print(str(e))


def single_upload(es, index_name, doc_body):
    try:
        es.index(index=index_name, body=doc_body)
        print("Single upload completed. ")
    except Exception as e:
        print(str(e))

def bulk_upload(es, index_name, json_file):
    # create generator that generates one doc at a time from json file
    def gendata(index_name, json_file):
        i = 0
        businesses = json.load(open(json_file, "r"))
        for buz in businesses:
            i += 1
            yield {
                "_index": index_name,
                "_id": i,
                "_source": buz,
            }
    # bulk upload using bulk helper api
    bulk(es, gendata(index_name, json_file))
    print("Bulk upload completed. ")

if __name__ == '__main__':
    # connect to elasticsearch cluster
    es = Elasticsearch(
        hosts=[HOST],
        http_auth=AUTH,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    print("Retrieved cluster info: {}\n".format(es.info()))
    # create index if not exist
    index_name = 'restaurants'
    create_index(es, index_name)
    # upload one doc to cluster
    restaurant = dict(
        type = 'Restaurant',
        restaurant_id = 'test-id',
        cuisine = 'test-cuisine'
    )
    #single_upload(es, index_name, restaurant)

    # bulk upload json file dataset
    json_file = '../data/businesses_es.json'
    bulk_upload(es, index_name, json_file)
