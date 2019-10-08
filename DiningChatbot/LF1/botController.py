import math
import dateutil.parser
import datetime
import time
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class botController():
    
    def get_slots(self, intent_request):
        return intent_request['currentIntent']['slots']
    
    
    def elicit_slot(self, session_attributes, intent_name, slots, slot_to_elicit, message):
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': intent_name,
                'slots': slots,
                'slotToElicit': slot_to_elicit,
                'message': message
            }
        }
    
    
    def close(self, session_attributes, fulfillment_state, message):
        response = {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': fulfillment_state,
                'message': message
            }
        }
    
        return response
    
    
    def delegate(self, session_attributes, slots):
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate',
                'slots': slots
            }
        }
    
    
    def parse_int(self,n):
        try:
            return int(n)
        except ValueError:
            return float('nan')
    
    
    def build_validation_result(self, is_valid, violated_slot, message_content):
        if message_content is None:
            return {
                "isValid": is_valid,
                "violatedSlot": violated_slot,
            }
    
        return {
            'isValid': is_valid,
            'violatedSlot': violated_slot,
            'message': {'contentType': 'PlainText', 'content': message_content}
        }
    
    
    def isvalid_date(self, date):
        try:
            dateutil.parser.parse(date)
            return True
        except ValueError:
            return False
    
    
    def validate_order_cuisines(self, location_type, cuisine_type, date, dining_time, people_number, phone_number):
        location_types = ['Manhattan']
        cuisine_types = ['Italian','Chinese', 'Japanese', 'Indian','Mexican']
        if location_type is not None and location_type.lower() not in location_types:
            return self.build_validation_result(False,
                                          'locationType',
                                          'We do not have {}, please try another place'.format(location_type))
    
        if cuisine_type is not None and cuisine_type.lower() not in cuisine_types:
            return self.build_validation_result(False,
                                           'cuisineType',
                                           'We do not have {}, would you like a different type of cuisine?  '
                                           'Our most popular cuisines are roses'.format(cuisine_type))
    
        if date is not None:
            if not self.isvalid_date(date):
                return self.build_validation_result(False, 'diningDate', 'I did not understand that, what date would you like to pick the cuisines up?')
            elif datetime.datetime.strptime(date, '%Y-%m-%d').date() <= datetime.date.today():
                return self.build_validation_result(False, 'diningDate', 'You can pick up the cuisines from tomorrow onwards.  What day would you like to pick them up?')
    
        if dining_time is not None:
            if len(dining_time) != 5:
                # Not a valid time; use a prompt defined on the build-time model.
                return self.build_validation_result(False, 'diningTime', None)
    
            hour, minute = dining_time.split(':')
            hour = self.parse_int(hour)
            minute = self.parse_int(minute)
            if math.isnan(hour) or math.isnan(minute):
                # Not a valid time; use a prompt defined on the build-time model.
                return self.build_validation_result(False, 'diningTime', None)
    
            if hour < 10 or hour > 23:
                # Outside of business hours
                return self.build_validation_result(False, 'diningTime', 'Our business hours are from ten a m. to eleven p m. Can you specify a time during this range?')
    
        if people_number < 1 or people_number > 20:
            # Too many people
            return self.build_validation_result(False, 'peopleNumber', 'Sorry. We can only host at most 20 people. ')
    
        if len(phone_number) != 10:
            # Wrong phone number
            return self.build_validation_result(False, 'phoneNumber', 'Sorry. Please input correct phone number. ')
    
    
        return self.build_validation_result(True, None, None)
    
    
    """ --- Functions that control the bot's behavior --- """
    
    
    def order_cuisines(self, intent_request):
        """
        Performs dialog management and fulfillment for ordering cuisines.
        Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
        in slot validation and re-prompting.
        """
        slots = self.get_slots(intent_request)
        location_type, cuisine_type, date, dining_time, people_number, phone_number, source = None, None, None, None, None, None, None
        
        if "locationType" in slots:
            location_type = slots["locationType"]
        if "cuisineType" in slots:
            cuisine_type = slots["cuisineType"]
        if "diningDate" in slots:
            date = slots["diningDate"]
        if "diningTime" in slots:
            dining_time = slots["diningTime"]
        if "peopleNumber" in slots:
            people_number = slots["peopleNumber"]
        if "phoneNumber" in slots:
            phone_number = slots["phoneNumber"]
        if "invocationSource" in slots:
            source = intent_request['invocationSource']
    
        if source == 'DialogCodeHook':
            # Perform basic validation on the supplied input slots.
            # Use the elicitSlot dialog action to re-prompt for the first violation detected.
            slots = self.get_slots(intent_request)
    
            validation_result = self.validate_order_cuisines(location_type, cuisine_type, date, dining_time, people_number, phone_number)
            if not validation_result['isValid']:
                slots[validation_result['violatedSlot']] = None
                return self.elicit_slot(intent_request['sessionAttributes'],
                                   intent_request['currentIntent']['name'],
                                   slots,
                                   validation_result['violatedSlot'],
                                   validation_result['message'])
    
            # Pass the price of the cuisines back through session attributes to be used in various prompts defined
            # on the bot model.
            output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
            # if cuisine_type is not None:
            #     output_session_attributes['Price'] = len(cuisine_type) * 5  # Elegant pricing model
    
            return self.delegate(output_session_attributes, self.get_slots(intent_request))
    
        # Order the cuisines, and rely on the goodbye message of the bot to define the message to the end user.
        # In a real bot, this would likely involve a call to a backend service.
        return self.close(intent_request['sessionAttributes'],
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': 'Thanks, your order for {} has been placed and will be ready for dining by {} on {}'.format(cuisine_type, dining_time, date)})