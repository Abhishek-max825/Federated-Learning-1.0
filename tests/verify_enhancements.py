import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'
START_ROUND_URL = f'{BASE_URL}/api/fl/start_round'
AGGREGATE_URL = f'{BASE_URL}/api/fl/aggregate'
HISTORY_URL = f'{BASE_URL}/api/fl/history'

def verify_enhancements():
    print("--- Verifying Enhancements ---")
    session = requests.Session()
    
    # 1. Login as Admin
    try:
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        
        login_data = {'csrf_token': csrf_token, 'username': 'admin', 'password': 'admin123', 'submit': 'Sign In'}
        response = session.post(LOGIN_URL, data=login_data)
        if "Admin Dashboard" not in response.text:
             print("[FAIL] Admin login failed.")
             return
    except Exception as e:
        print(f"[FAIL] Error during login: {e}")
        return

    # 2. Simulate FL Activity to generate logs and history
    print("Simulating Round...")
    session.post(START_ROUND_URL)
    # Ideally should train, but we can try to aggregate to generate a log entry (even if empty error)
    # Actually, aggregator log is only on success.
    # Let's check history endpoint first (empty or init state)
    
    resp = session.get(HISTORY_URL)
    if resp.status_code == 200:
        data = resp.json()
        print(f"[PASS] History endpoint accessible. Data: {data}")
    else:
        print(f"[FAIL] History endpoint failed. Status: {resp.status_code}")

    # 3. Check Dashboard for Audit Logs
    # We are already on dashboard page from login rediect or can curl it
    resp = session.get(f'{BASE_URL}/admin/dashboard')
    if "Recent Audit Logs" in resp.text:
         print("[PASS] Audit Logs section present in Dashboard.")
    else:
         print("[FAIL] Audit Logs section missing.")
         
    if "accuracyChart" in resp.text:
        print("[PASS] Chart.js canvas present.")
    else:
        print("[FAIL] Chart.js canvas missing.")

if __name__ == "__main__":
    verify_enhancements()
