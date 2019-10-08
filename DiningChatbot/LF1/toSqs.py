import logging
import boto3
from botocore.exceptions import ClientError


class toSqs():
    def __init__(self):
        pass
    
    def send_func(self, sqs_queue_url, msg_body):
        """
        :param sqs_queue_url: String URL of existing SQS queue
        :param msg_body: String message body
        :return: Dictionary containing information about the sent message. If
            error, returns None.
        """
    
        # Send the SQS message
        sqs_client = boto3.client('sqs')
        try:
            msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                          MessageBody=msg_body)
        except ClientError as e:
            logging.error(e)
            return None
        return msg

            
    def send_sqs_message(self, event):
    
        sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/916570745604/Q1'
    
        # Set up logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s: %(message)s')
    
        # Send some SQS messages

        # msg_body = f'SQS message #{i}' 
        # msg_body = self.getResp(event)
        msg_body = str(event)
        # print(msg_body)
        # print(type(msg_body))
        msg = self.send_func(sqs_queue_url, msg_body)
        if msg is not None:
            logging.info(f'Sent SQS message ID: {msg["MessageId"]}')


if __name__ == '__main__':
    event = {
          "messageVersion": "1.0",
          "invocationSource": "DialogCodeHook",
          "userId": "John",
          "sessionAttributes": {},
          "bot": {
            "name": "diningSuggestion",
            "alias": "$LATEST",
            "version": "$LATEST"
          },
          "outputDialogMode": "Text",
          "currentIntent": {
            "name": "diningSuggestionIntent",
            "slots": {
              "locationType": "uptown",
              "diningDate": "2019-11-08",
              "diningTime": "10:00",
              "phoneNumber": "+19173304793",
              "peopleNumber": "12",
              "cuisineType": "chinese"
            },
            "confirmationStatus": "None"
          }
        }
    toSqs().send_sqs_message(event)