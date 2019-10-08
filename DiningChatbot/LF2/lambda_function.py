from fromSqs import fromSqs
from searchES import searchES
import boto3
from boto3.dynamodb.conditions import Key, Attr

class Lambda2():
    def __init__(self):
        pass
        
    def fromSqs(self):
        fro = fromSqs()
        msg = fro.receive_func()
        return msg
    
    def searchES(self, cuisine_type='American', num_restaurants=1): 
        """Query Elasticsearch index for restaurants in given cuisine type. 
        :param cuisine_type: the category of restaurants you want to search for
                             Supported inputs: ['American', 'Chinese', 'Japanese', 'Italian', 'Mexican', 'Indian', 'Thai', 'Greek']
        :param num_restaurants: number of results to get
        
        :return hits: list of restaurants in cuisine type. 
                      Example: [{'type': 'Restaurant', 'restaurant_id': 'Rc1lxc5lSKJYd162JHNMfQ', 'cuisine': 'American'}]
        """
        index_name = 'restaurants'
        s = searchES(index_name)
        hits = s.search_es(cuisine_type, num_restaurants)
        return hits
        
    def searchDynamo(self, restaurant_id): 
        """Query DynamoDB for restaurant details using restaurant_id. 
        :param restaurant_id: business ID of the restaurant as a string. 
                              Example: 'Rc1lxc5lSKJYd162JHNMfQ'
        
        :return item: restaurant details stored in Dynamo. 
                      Example: [{'business_id': 'qgY41g_eg0eNzewCXmKcaA', 'rating': Decimal('5'), ...}]
                      Headers: ['business_id', 'rating', 'zip_code', 'insertedAtTimestamp', 'category', 'address', 'name', 'review_count', 'coordinates']
        """
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('yelp-restaurants')
        response = table.scan(
                FilterExpression=Attr('business_id').eq(restaurant_id)
            )
        item = response['Items']
        return item
        
    def toSNS(self, msg, phoneNumber):
        # Create an SNS client
        sns = boto3.client('sns')
        # Publish a simple message to the specified SNS topic

        response = sns.publish(
            PhoneNumber=phoneNumber,
            Message=msg)   # TopicArn='arn:aws:sns:us-east-1:916570745604:HW1-SNS', 
        
def lambda_handler(event, context):
    lf2 = Lambda2()
    msg = lf2.fromSqs()
    cuisine = None
    rest_info = None
    
    if 'Body' in msg:
        msg_intent = eval(msg['Body'])
        # for k, v in msg_intent.items():
        #     print(k)
        cuisine = msg_intent['currentIntent']['slots']['cuisineType']
        peopleNumber = msg_intent['currentIntent']['slots']['peopleNumber']
        dining_time = msg_intent['currentIntent']['slots']['diningTime']
        date = msg_intent['currentIntent']['slots']['diningDate']
        phoneNumber = msg_intent['currentIntent']['slots']['phoneNumber']

    if cuisine:
        restaurants = lf2.searchES(cuisine_type=cuisine, num_restaurants=3)
        # print(restaurants)
        rest_info = []
        for restaurant in restaurants:
            rest_info.append(lf2.searchDynamo(restaurant['restaurant_id'])[0])

    if rest_info:
        msg_SNS = "Thanks, Here are my {} restaurant suggestions for {} people, for dining at {} on {}: \
        \n  - {} located at {}; \n  - {} located at {}; \n  - {} located at {}. \
        enjoy your meal!".format(cuisine, peopleNumber, dining_time, date, rest_info[0]['name'], rest_info[0]['address'],
        rest_info[1]['name'], rest_info[1]['address'],rest_info[2]['name'], rest_info[2]['address'])
        lf2.toSNS(msg_SNS, phoneNumber)
    
    
if __name__ == "__main__":
    lambda_handler(None, None) 
    