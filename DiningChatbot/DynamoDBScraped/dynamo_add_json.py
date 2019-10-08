from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import time
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


table = dynamodb.Table('yelp-restaurants')
# while table.table_status != 'ACTIVE':
#     table.reload()

json_file = "../data/businesses_dynamo.json"
businesses = json.load(open(json_file, "r"), parse_float = decimal.Decimal)
count = len(businesses)
i = 0
for buz in businesses:
    item = dict(
        insertedAtTimestamp = decimal.Decimal(time.time()),
        business_id = buz['id'],
        name = buz['name'],
        category = buz['category'],
        address = buz['address'],
        coordinates = buz['coordinates'],
        review_count = buz['review_count'],
        rating = buz['rating'],
        zip_code = buz['zip_code']
    )
    table.put_item(Item=item)
    i += 1
    if i % 100 == 0:
        print("{}/{} items added...".format(i, count))

