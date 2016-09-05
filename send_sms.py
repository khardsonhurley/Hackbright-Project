import os
from twilio.rest import TwilioRestClient

def send_text(text):

	account_sid = "AC428aa93a3d8c72b43a86a7c4839b1ebb" # Your Account SID from www.twilio.com/console
	auth_token  = os.environ['TWILIO_SECRET_KEY']  # Your Auth Token from www.twilio.com/console

	client = TwilioRestClient(account_sid, auth_token)

	message = "You searched %s which means %s." % (text['phrase'],text['translation'])

	client.messages.create(body=message,
	    to="+18586826816",    # Replace with your phone number
	    from_="+18584139380") # Replace with your Twilio number
