import requests
import datetime

# Register returns a user class that has methods that can be called to interact with the user.
# Custom exceptions depending on status code, exceptions will raise the errors returned in the JSON.
# send_verification_code will return an object that will have the method Verify(code) and allow for a code to be sent to the verification address.
# Linked list of user accounts.
# Constanly checking for game start on seperate thread.
# When game starts linked list of user is iterated and .Join(game) is called on each.
# Linked list is then cleared to make room for new accounts.
# .ini configuration file.
# Accounts should be stored on disk in case program crashes.
# Potentially overide requests methods to implement API methods.

# Create UK account and sniff network all the way until the game starts.
# Test this with UK account and my account as referal.

# Raised when the Hype API encounters an error
class HypeError(Exception):

	# Creates a new instance of the hype error class.
    def __init__(self, message, err_code):
        # Call the base excepetion class.
        super(HypeError, self).__init__(message)
        # Sets the error code
        self.err_code = err_code


# A class used for dealing with Hype API responses.
class HypeResponse:

	# Creates a new instance of the hype response class.
	def __init__(self, response):
		# Sets the response attribute.
		self.response = response

	# Raises an exception if there is an error associated with the given response.
	def check_for_error(self):
		# Validates the response status code.
		if self.response.status_code != 200:
			# Casts the response data to json.
			res_data = self.response.json()
			# Gets the error message
			err_msg = res_data['error']
			# Gets the error code
			err_code = res_data['errorCode']
			# Raises a hype error.
			raise HypeError(err_msg, err_code)

	# Returns the response data in json format.
	def get_data(self, **kwargs):
		# Returns the response data in json format.
		return self.response.json(**kwargs)


# A Python wrapper for the Hype API.
class Hype:
	
	# Creates a new instance of the verification class.
	def __init__(self, auth):
		# Sets the account auth token.
		self.__auth = auth

	# Attempts to join an active game.
	def join_game(self):
		# Constructs the auth headers.
		auth_headers = {"Authorization": "Bearer {}".format(self.__auth)}
		# Constructs the type params.
		type_params = {'type': 'hq'}
		# Sends the game request.
		res = HypeResponse(requests.get('https://api-quiz.hype.space/shows/now', headers=auth_headers, params=type_params))
		# Raise an exception if there is an error.
		res.check_for_error()
		# Casts the response data to json.
		res_data = res.get_data()
		# Checks if a game is active.
		if not res_data['active']:
			# Raises a hype error.
			raise HypeError("There are no active games.", None)
		# Checks if the game is full.
		elif res_data['atCapacity']:
			# Raises a hype error.
			raise HypeError("The current game is full.", None)

	# Returns the next game time.
	def next_game_time(self):
		# Constructs the auth headers.
		auth_headers = {"Authorization": "Bearer {}".format(self.__auth)}
		# Constructs the type params.
		type_params = {'type': 'hq'}
		# Sends the game request.
		res = HypeResponse(requests.get('https://api-quiz.hype.space/shows/now', headers=auth_headers, params=type_params))
		# Raise an exception if there is an error.
		res.check_for_error()
		# Casts the response data to json.
		res_data = res.get_data()
		# Returns the next show time.
		return datetime.datetime.strptime(res_data['nextShowTime'], "%Y-%m-%dT%H:%M:%S.%fZ")

	# Sends a verification code to the specified phone number via SMS.
	@staticmethod
	def send_verification_code(phone, method):
		# Constructs the verification request data.
		ver_data = {"phone": phone, "method": method}
		# Posts the verfication request to the Hype API.
		res = HypeResponse(requests.post('https://api-quiz.hype.space/verifications', data=ver_data))
		# Raise an exception if there is an error.
		res.check_for_error()
		# Casts the response data to json.
		res_data = res.get_data()
		# Creates and returns a new hype verification object.
		return res_data['verificationId']

	# Verifies the phone number via the given code.
	@staticmethod
	def verify_phone(ver_id, code):
		# Constructs the verification request data.
		ver_data = {"code": code}
		# Posts the verfication code to the Hype API.
		res = HypeResponse(requests.post('https://api-quiz.hype.space/verifications/{}'.format(ver_id), data=ver_data))
		# Raise an exception if there is an error.
		res.check_for_error()
		# Casts the response data to json.
		res_data = res.get_data()
		# If an account already exists with this phone.
		if res_data['auth']:
			# Raises a hype error.
			# raise HypeError("Account with this phone number already exists.", None)
			# Creates and returns a new hype account object.
			return Hype(res_data['auth']['authToken'])

	# Registers a new user account if there is not already one linked with the verification id.
	@staticmethod
	def register(username, locale, language, time_zone, ref_username, ver_id, country):
		# Constructs the register request data.
		reg_data = {"username": username, "locale": locale, "language": language, "timeZone": time_zone, "referringUsername": ref_username, "verificationId": ver_id, "country": country}
		# Posts the register request to the Hype API.
		res = HypeResponse(requests.post('https://api-quiz.hype.space/users', data=reg_data))
		# Raise an exception if there is an error.
		res.check_for_error()
		# Casts the response data to json.
		res_data = res.get_data()
		# Creates and returns a new hype object.
		return Hype(res_data['authToken'])

if __name__ == '__main__':
	# Sends a verification code to the given phone number.
	ver_id = Hype.send_verification_code('+447504531139', 'sms')
	# Gets the verification code from the user.
	ver_code = input('Please enter your verification code: ')
	# Verifies the verification id.
	account = Hype.verify_phone(ver_id, ver_code)

	# Constructs the auth headers.
	auth_headers = {"Authorization": "Bearer {}".format(account._Hype__auth)}
	while True:
		# Sends the game request.
		res = HypeResponse(requests.get('https://api-quiz.hype.space/{}'.format(input('enter:')), headers=auth_headers))
		print(res.get_data())
	input()