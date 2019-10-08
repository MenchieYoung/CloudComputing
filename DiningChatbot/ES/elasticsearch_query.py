from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk
from requests_aws4auth import AWS4Auth
import json
import secrets

HOST = secrets.es_host
AUTH = AWS4Auth(secrets.aws_access_key_id, secrets.aws_secret_access_key, 'us-east-1', 'es')


def search_es(es, index_name, query_body, offset, size):
    res = es.search(index=index_name, body=query_body, from_=offset, size=size)
    hits = [hit for hit in res['hits']['hits']]
    return hits


if __name__ == '__main__':
    # connect to elasticsearch cluster
    es = Elasticsearch(
        hosts=[HOST],
        http_auth=AUTH,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    #print("Retrieved cluster info: {}\n".format(es.info()))
    # refresh all indices
    es.indices.refresh(index='')
    # get index info
    index_name = 'restaurants'
    print("Index info: \n", es.indices.get(index=index_name), '\n')

    # get a restaurant using cuisine
    offset, size = 0, 5
    query = {'query': {'match': {'cuisine': 'American'}}}
    hits = search_es(es, index_name, query, offset, size)
    print("{} hits returned from query: ".format(len(hits)))
    for hit in hits:
        print(hit)

    count = es.cat.count(index=index_name)
    print("Number of documents in index: ", count)

    #doc1 = es.get(index=index_name, id=1)
    #es.delete_by_query(index=index_name, body=query)