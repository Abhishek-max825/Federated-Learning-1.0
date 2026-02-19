import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'

def login(username, password):
    session = requests.Session()
    try:
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        
        login_data = {'csrf_token': csrf_token, 'username': username, 'password': password, 'submit': 'Sign In'}
        response = session.post(LOGIN_URL, data=login_data)
        if "You are logged in as" in response.text:
            return session
        return None
    except:
        return None

def verify_fl_workflow():
    # 1. Admin starts round
    print("--- 1. Admin Starting Round ---")
    admin_session = login('admin', 'admin123')
    if not admin_session:
        print("Failed to login as admin")
        return

    resp = admin_session.post(f'{BASE_URL}/api/fl/start_round')
    print(f"Start Round: {resp.status_code} - {resp.json()}")

    # 2. Check Status (Round 1, 0 updates)
    resp = admin_session.get(f'{BASE_URL}/api/fl/status')
    print(f"Status: {resp.json()}")

    # 3. Hospital trains
    print("\n--- 2. Hospital Training ---")
    hospital_session = login('hospital', 'hospital123')
    if not hospital_session:
        print("Failed to login as hospital")
        return

    # Trigger training (simulates local training on server)
    print("Triggering training (this might take a few seconds)...")
    resp = hospital_session.post(f'{BASE_URL}/api/fl/train')
    print(f"Train Response: {resp.status_code} - {resp.text}")

    # 4. Check Status (Round 1, 1 update)
    resp = admin_session.get(f'{BASE_URL}/api/fl/status')
    print(f"Status after training: {resp.json()}")

    # 5. Aggregate
    print("\n--- 3. Aggregating ---")
    resp = admin_session.post(f'{BASE_URL}/api/fl/aggregate')
    print(f"Aggregate Response: {resp.status_code} - {resp.json()}")

    # 6. Check Status (Round 2, 0 updates)
    resp = admin_session.get(f'{BASE_URL}/api/fl/status')
    print(f"Final Status: {resp.json()}")

if __name__ == "__main__":
    verify_fl_workflow()
