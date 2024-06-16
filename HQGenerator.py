from Hype import *
from threading import Thread
import string
import random
import time

# Game stream info is sent via join_game().
# Non HTTP request is used to join game stream.
# Use fiddler, non-http interceptor.
# Drop all requests apart from join_game().
# MORE TESTING!

# Look at a successful join game request, see what is sent.
# See what packets are sent and recieved from stream address returned from join_game().
# Drop any requests that have no relation to the api with a referral account and see if lives register.
# Intercept requests before game starts, to see which request triggers the stream.
# Maybe an auth token is sent to the stream address to register we have joined?

# Run this script with UK account and my account as a referal as soon as game starts.
# See if life registers.
# Create a debug file.

# Google stream URL protocol.
# Create UK account and sniff network all the way until the game starts.
# Test this with UK account and my account as referal.
# Sniff network packets on game join.

# Generates a random username
def generate_username():
	# Character list.
	char_list = string.digits + string.ascii_letters
	# Generates a random username.
	return ''.join(char_list[random.randrange(0, len(char_list))] for x in range(0, random.randrange(5, 15)))

# Iterates through the accounts and attempts to join a game.
def accounts_join():
	# Loops forever
	while True:
		# Uses the accounts lock.
		# with accounts_lock:
		# Iterates through the accounts.
		for account in accounts:
			# Error handling.
			try:
				# Attempts to join a game
				account.join_game()
			# If a Hype error has occured.
			except HypeError as err_msg:
				# Ignores the error.
				pass

if __name__ == '__main__':
	# A linked list of created user accounts.
	# accounts = []
	# Creates an account lock
	# accounts_lock = Thread.Lock()
	# Creates a new thread for accounts to join games.
	# thread = Thread(target=accounts_join)
	# Starts the thread.
	# thread.start()
	# Gets the users referral username
	# ref_usrname = input('Please enter you referral account username: ')
	# Account creation loop
	while True:
		# Error handling.
		try:
			# Gets a phone number from the user.
			phone_num = input('Please enter your phone number: ')
			# Sends a verification code to the given phone number.
			ver_id = Hype.send_verification_code(phone_num, 'sms')
			# Gets the verification code from the user.
			ver_code = input('Please enter your verification code: ')
			# Verifies the verification id.
			Hype.verify_phone(ver_id, ver_code)
			# Generates a username for the account
			usrname = generate_username()
			# Notifies the user.
			print("Creating account:", usrname)
			# Register an acount with the verfication id.
			account = Hype.register(usrname, None, None, None, 'jommy273737', ver_id, None)
			# Uses the accounts lock.
			# with accounts_lock:
			# Adds the account to the accounts linked list.
			# accounts.append(account)
			# Waits for a game.
			while True:
				# Error handling.
				try:
					# Attempts to join a game
					account.join_game()
				# If a Hype error has occured.
				except HypeError as err_msg:
					# Notifies the user.
					print(err_msg)
					# Ignores the error.
					pass
				# Waits to try again.
				time.sleep(3)
		# If a Hype error has occured.
		except HypeError as err_msg:
			# Notifies the user
			print(err_msg)
			# Goes back to the top of the loop
			continue