import os.path
import pickle
import traceback

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

KEYWORD = "bitcoin turing quincy getcontact webex uphold buddy twitter team sanket cloudflare noice admob ip2location analytics location deviantart glitch sourcery gopay ruangguru binance jotform github"
KEYWORD = KEYWORD.split()

def getEmails():
	# Variable creds will store the user access token.
	# If no valid token found, we will create one.
	c = 0
	creds = None

	# The file token.pickle contains the user access token.
	# Check if it exists
	if os.path.exists('token.pickle'):
		# Read the token from the file and store it in the variable creds
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# If credentials are not available or are invalid, ask the user to log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
			creds = flow.run_local_server(port=0)

		# Save the access token in token.pickle file for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	# Connect to the Gmail API
	service = build('gmail', 'v1', credentials=creds)

	# request a list of all the messages
	result = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=500).execute()
	messages = result.get('messages')
	# messages is a list of dictionaries where each dictionary contains a message id.
	# iterate through all the messages
	for msg in messages:
		# Get the message from its id
		txt = service.users().messages().get(userId='me', id=msg['id']).execute()
		# Use try-except to avoid any Errors
		try:
			# Get value of 'payload' from dictionary 'txt'
			payload = txt['payload']
			headers = payload['headers']

			# Look for Sender Email in the headers
			for d in headers:
				if d['name'] == 'From':
					subject = d['value']
					# check if keyword is present in sender
					# mark as read and move it to trash
					for keyword in KEYWORD:
						if keyword in subject.lower():
							c += 1
							print(f"{keyword} found in subject")
							service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()
							service.users().messages().trash(userId='me', id=msg['id']).execute()
							break
		except Exception as e:
			print(traceback.format_exc())
			return
	print(f"{c} emails have been moved to trash!")

if __name__ == '__main__':
	getEmails()