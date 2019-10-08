import boto3

class fromSqs():
    def receive_func(self):
        # Create SQS client
        sqs = boto3.client('sqs')

        queue_url = 'https://sqs.us-east-1.amazonaws.com/916570745604/Q1'

        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
            )
        # reponse: {'Messages': [{dict}]} 
        # print("response**", response)
        if 'Messages' in response:  # response['ResponseMetadata']
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']

            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            #print('Received and deleted message: %s' % message)
            print('Received and deleted message')
            return message
        
        else:
            print("No message in SQS")
            return None
            
# if __name__ == "__main__":
#     fro = fromSqs()
#     fro.receive_func()