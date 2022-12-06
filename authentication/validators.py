import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def custom_email_validator(email):

	if(re.fullmatch(regex, email)):
		return True

	else:
		return False
