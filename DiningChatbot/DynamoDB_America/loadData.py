import boto3


# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.


import boto3
import json
import decimal

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('yelp-restaurants')

with open("DynamoDB/files/cleanData_5k_records.json") as json_file:
    restaurants = json.load(json_file, parse_float = decimal.Decimal)
    for res in restaurants:
        # address", 'business_id', 'categories', 'city', 'hours', 'is_open', 'name', 'stars', 'state'
        if res['address'] and res['business_id'] and res['categories'] and \
            res['city'] and res['hours'] and res['is_open'] and res['name'] and res['stars'] and  res['state']:
            table.put_item(
              Item={
                  # 'address': res['address'] if res['address'] else "",
                  'address': res['address'],
                  'business_id': res['business_id'],
                  'categories': res['categories'],
                  'city': res['city'],
                  'hours': res['hours'],
                  'is_open': res['is_open'],
                  'name': res['name'],
                  'stars': res['stars'],
                  'state': res['state']
                }
             )


# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
# print(table.creation_date_time)