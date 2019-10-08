import time
import os
import logging
from toSqs import toSqs
from botController import botController

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class handleEvent():
    
    def __init__(self):
        self.toSqs = toSqs()
        self.bot =botController()

       
    """ --- Intents --- """
    def dispatch(self, intent_request):
        """
        Called when the user specifies an intent for this bot.
        """
        logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    
        intent_name = intent_request['currentIntent']['name']
        print(intent_name)
        # Dispatch to your bot's intent handlers
        if intent_name == 'diningSuggestionIntent':
            return self.bot.order_cuisines(intent_request)
    
        raise Exception('Intent with name ' + intent_name + ' not supported')
    
    
    """ --- Main handler --- """
    def lambda_handler_func(self, event): #, context):
        """
        Route the incoming request based on intent.
        The JSON body of the request is provided in the event slot.
        """
        # By default, treat the user request as coming from the America/New_York time zone.
        os.environ['TZ'] = 'America/New_York'
        time.tzset()
        print("**********", event)
        logger.debug('event.bot.name={}'.format(event['bot']['name']))
        
        self.toSqs.send_sqs_message(str(event))
        #message = event['Records'][0]['Sns']['Message']
        #print("From SNS: " + message)
    
        return self.dispatch(event)


def lambda_handler(event, context):
    hand = handleEvent()
    return hand.lambda_handler_func(event)