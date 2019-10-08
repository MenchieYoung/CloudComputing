from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import time

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('yelp-restaurants')
#print(table.item_count)

count = 0
response = table.scan()
count += len(response['Items'])
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    count += len(response['Items'])
print("Total number of items in table is: {}.".format(count))