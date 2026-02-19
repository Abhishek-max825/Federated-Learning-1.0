import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'

def login(username, password):
    session = requests.Session()
    try:
        # Get CSRF token
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        
        # Post credentials
        login_data = {
            'csrf_token': csrf_token,
            'username': username,
            'password': password,
            'submit': 'Sign In'
        }
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        if "You are logged in as" in response.text:
            return session
        else:
            print(f"Login failed for {username}")
            return None
    except Exception as e:
        print(f"Error logging in {username}: {e}")
        return None

def check_access(session, role, target_role, url, expected_code):
    response = session.get(url)
    if response.status_code == expected_code:
        print(f"[PASS] {role} accessing {target_role} dashboard ({url}): Got {response.status_code}")
    else:
        print(f"[FAIL] {role} accessing {target_role} dashboard ({url}): Expected {expected_code}, Got {response.status_code}")

def verify_rbac():
    # Admin
    print("\n--- Testing Admin ---")
    session = login('admin', 'admin123')
    if session:
        check_access(session, 'Admin', 'Admin', f'{BASE_URL}/admin/dashboard', 200)
        check_access(session, 'Admin', 'Doctor', f'{BASE_URL}/doctor/dashboard', 403)
        check_access(session, 'Admin', 'Hospital', f'{BASE_URL}/hospital/dashboard', 403)

    # Doctor
    print("\n--- Testing Doctor ---")
    session = login('doctor', 'doctor123')
    if session:
        check_access(session, 'Doctor', 'Doctor', f'{BASE_URL}/doctor/dashboard', 200)
        check_access(session, 'Doctor', 'Admin', f'{BASE_URL}/admin/dashboard', 403)

    # Hospital
    print("\n--- Testing Hospital ---")
    session = login('hospital', 'hospital123')
    if session:
        check_access(session, 'Hospital', 'Hospital', f'{BASE_URL}/hospital/dashboard', 200)
        check_access(session, 'Hospital', 'Doctor', f'{BASE_URL}/doctor/dashboard', 403)

if __name__ == "__main__":
    verify_rbac()
