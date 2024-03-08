import requests

'''
class Authenticator:
    
    def __init__(self, api_url):
        self.api_url = api_url

    def authenticate(self, email, password):
        # authenticates with database
        """
        data = {'email': email, 'password': password}
        response = requests.post(self.api_url, json=data)
        if response.ok and response.json().get('status') == 'success':
            return True
        else:
            return False
        """
'''

# test
def authenticate(email, password):
    # test email and password
    test_email = "test@gmail.com"
    test_password = "123456"
    if email == test_email and password == test_password:
        return True
    else:
        return False
