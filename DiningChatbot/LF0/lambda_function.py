import json
import boto3

def lambda_handler(event, context):
    
    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='diningSuggestion',
        botAlias='diningSuggestion',
        userId='LF0',
        sessionAttributes={},
        requestAttributes={},
        inputText=event['input']
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        'body': response['message']
    }