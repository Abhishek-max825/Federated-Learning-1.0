import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'

def login(username, password):
    session = requests.Session()
    try:
        # Get CSRF token
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token_input = soup.find('input', {'name': 'csrf_token'})
        csrf_token = csrf_token_input['value'] if csrf_token_input else None
        
        print(f"Login CSRF: {csrf_token}")

        # Post credentials
        login_data = {
            'username': username,
            'password': password,
            'submit': 'Sign In'
        }
        if csrf_token:
            login_data['csrf_token'] = csrf_token

        response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        if "You are logged in as" in response.text or "Admin Dashboard" in response.text:
            print(f"Login successful for {username}")
            return session
        else:
            print(f"Login failed for {username}. Status: {response.status_code}")
            print(response.text[:200])
            return None
    except Exception as e:
        print(f"Error logging in {username}: {e}")
        return None

def test_admin_actions():
    print("\n--- Testing Admin API Actions ---")
    # Try 'password' first as per walkthrough
    session = login('admin', 'password')
    if not session:
        print("Retrying with 'admin123'...")
        session = login('admin', 'admin123')
    
    if session:
        # Test Start Round
        print("\n[POST] /api/fl/start_round")
        res = session.post(f'{BASE_URL}/api/fl/start_round')
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")

        # Test Aggregate
        print("\n[POST] /api/fl/aggregate")
        res = session.post(f'{BASE_URL}/api/fl/aggregate')
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")

if __name__ == "__main__":
    test_admin_actions()
