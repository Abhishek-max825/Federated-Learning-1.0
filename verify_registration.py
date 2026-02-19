import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'http://127.0.0.1:5000'
REGISTER_URL = f'{BASE_URL}/auth/register'
LOGIN_URL = f'{BASE_URL}/auth/login'

def verify_registration():
    print("--- Verifying Registration ---")
    session = requests.Session()
    
    # 1. Get CSRF token
    try:
        response = session.get(REGISTER_URL)
        if response.status_code != 200:
            print(f"[FAIL] Register page inaccessible. Status: {response.status_code}")
            print(f"URL: {REGISTER_URL}")
            # print(response.text)
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    except Exception as e:
        print(f"[FAIL] Error accessing register page: {e}")
        return

    # 2. Register new user
    new_user = {
        'csrf_token': csrf_token,
        'username': 'new_doctor',
        'email': 'new_doc@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'Doctor',
        'submit': 'Register'
    }
    
    response = session.post(REGISTER_URL, data=new_user)
    
    # 3. Check for redirection to login or success message
    if response.url == LOGIN_URL or "Congratulations" in response.text:
        print("[PASS] Registration successful. Redirected to login.")
    else:
        print(f"[FAIL] Registration failed. URL: {response.url}")
        # print(response.text) # Debug if needed

    # 4. Try Login with new user
    print("\n--- Verifying Login for New User ---")
    
    # Need fresh CSRF from login page
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    
    login_data = {
        'csrf_token': csrf_token,
        'username': 'new_doctor',
        'password': 'password123',
        'submit': 'Sign In'
    }
    
    response = session.post(LOGIN_URL, data=login_data)
    
    if "You are logged in as" in response.text and "Doctor Dashboard" in response.text: # Should redirect to dashboard
         # Actually we redirected, so check specific dashboard content
         resp = session.get(f'{BASE_URL}/doctor/dashboard')
         if resp.status_code == 200:
             print("[PASS] New user login and dashboard access successful.")
         else:
             print(f"[FAIL] Dashboard access failed. Status: {resp.status_code}")
    elif "Doctor Dashboard" in response.text: # If redirect happened directly
        print("[PASS] New user login and dashboard access successful.")
    else:
        print("[FAIL] New user login failed.")

if __name__ == "__main__":
    verify_registration()
