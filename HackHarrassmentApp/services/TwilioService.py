from twilio.rest import TwilioRestClient
from twilio.rest.lookups import TwilioLookupsClient
from twilio.rest.exceptions import TwilioRestException
from HackHarrassmentApp.services.ChatService import ChatService

chat_service = ChatService()

account_sid = "ACdec7e108adad1d36efa110d8ccef8038"
auth_token = "50027e74d5a028775fbdd5f4166d480a"
from_number = "+441244478115"

class TwilioService:

    def send_sms(self, number, message):
        if number is None or message is None:
            return

        if self.is_valid_number(number) is False:
            return
        client = TwilioRestClient(account_sid, auth_token)
        message = client.messages.createmessage = client.messages.create(
            body = message,  # Message body, if any
            to = number,
            from_= from_number,
        )
        return message



    def is_valid_number(self, number):
        if number[:1] != '+':
            number = '+' + number

        if chat_service.user_exists(number) is not None:
            return True
        return self.is_valid_number_twilio(number)

    def is_valid_number_twilio(self, number):
        client = TwilioLookupsClient(account_sid, auth_token)
        try:
            response = client.phone_numbers.get(number)
            response.phone_number  # If invalid, throws an exception.
            return True
        except TwilioRestException as e:
            if e.code == 20404:
                return False
            else:
                raise e