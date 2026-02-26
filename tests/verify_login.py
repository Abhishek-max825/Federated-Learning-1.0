import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'
INDEX_URL = f'{BASE_URL}/index'

def verify_login():
    session = requests.Session()
    
    # 1. Get the login page to retrieve CSRF token
    try:
        response = session.get(LOGIN_URL)
        print(f"GET {LOGIN_URL}: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        print(f"CSRF Token: {csrf_token[:10]}...")
        
        # 2. Post credentials
        login_data = {
            'csrf_token': csrf_token,
            'username': 'admin',
            'password': 'admin123',
            'submit': 'Sign In'
        }
        
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        print(f"POST {LOGIN_URL}: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        # 3. Verify login success
        if "You are logged in as" in response.text:
            print("SUCCESS: Login successful. User is logged in.")
            return True
        else:
            print("FAILURE: Login failed. 'You are logged in as' not found in response.")
            return False

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    verify_login()
