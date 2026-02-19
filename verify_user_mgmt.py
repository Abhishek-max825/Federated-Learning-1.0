import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'
API_USERS = f'{BASE_URL}/api/users'

def login(username, password):
    session = requests.Session()
    try:
        # Get CSRF token
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token_input = soup.find('input', {'name': 'csrf_token'})
        csrf_token = csrf_token_input['value'] if csrf_token_input else None
        
        login_data = {
            'username': username,
            'password': password,
            'submit': 'Sign In'
        }
        if csrf_token:
            login_data['csrf_token'] = csrf_token

        response = session.post(LOGIN_URL, data=login_data)
        if "Admin Dashboard" in response.text or "You are logged in" in response.text:
            print(f"Login successful for {username}")
            return session
        else:
            print(f"Login failed for {username}")
            return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def verify_user_mgmt():
    print("\n--- Testing User Management API ---")
    session = login('admin', 'admin123')
    if not session:
        return

    # 1. List Users
    print("\n[GET] List Users")
    res = session.get(API_USERS)
    print(f"Status: {res.status_code}")
    users = res.json()
    print(f"Users found: {len(users)}")
    for u in users:
        print(f" - {u['username']} ({u['role']})")

    # 2. Add User
    print("\n[POST] Add User 'test_doctor'")
    new_user = {
        'username': 'test_doctor',
        'email': 'test_doc@example.com',
        'password': 'password',
        'role': 'Doctor'
    }
    res = session.post(API_USERS, json=new_user)
    print(f"Status: {res.status_code}")
    print(res.text)

    # 3. List again to find ID
    res = session.get(API_USERS)
    users = res.json()
    test_user = next((u for u in users if u['username'] == 'test_doctor'), None)
    
    if test_user:
        print(f"Verified 'test_doctor' exists with ID: {test_user['id']}")
        
        # 4. Delete User
        print(f"\n[DELETE] Delete User {test_user['id']}")
        res = session.delete(f"{API_USERS}/{test_user['id']}")
        print(f"Status: {res.status_code}")
        print(res.text)
        
        # 5. Verify Deletion
        res = session.get(API_USERS)
        users = res.json()
        deleted_user = next((u for u in users if u['username'] == 'test_doctor'), None)
        if not deleted_user:
             print("Verified 'test_doctor' is deleted.")
        else:
             print("Error: 'test_doctor' still exists!")
    else:
        print("Error: Could not find created user!")

if __name__ == "__main__":
    verify_user_mgmt()
