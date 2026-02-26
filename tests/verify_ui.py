import requests
from bs4 import BeautifulSoup

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

def verify_ui():
    print("--- Verifying UI Elements ---")
    
    # Check Doctor Dashboard Form
    doc_session = login('doctor', 'doctor123')
    if doc_session:
        resp = doc_session.get(f'{BASE_URL}/doctor/dashboard')
        if 'Heart Disease Prediction' in resp.text and '<form method="post">' in resp.text:
            print("[PASS] Doctor Dashboard contains prediction form.")
        else:
            print("[FAIL] Doctor Dashboard missing form.")
    else:
        print("[FAIL] Doctor login failed.")

    # Check Admin Dashboard Controls
    admin_session = login('admin', 'admin123')
    if admin_session:
        resp = admin_session.get(f'{BASE_URL}/admin/dashboard')
        if 'Start New Round' in resp.text and 'Aggregate Updates' in resp.text:
            print("[PASS] Admin Dashboard contains FL controls.")
        else:
            print("[FAIL] Admin Dashboard missing controls.")
    else:
        print("[FAIL] Admin login failed.")

    # Check Hospital Dashboard Button
    hosp_session = login('hospital', 'hospital123')
    if hosp_session:
        resp = hosp_session.get(f'{BASE_URL}/hospital/dashboard')
        if 'Train Local Model' in resp.text:
            print("[PASS] Hospital Dashboard contains Train button.")
        else:
            print("[FAIL] Hospital Dashboard missing button.")
    else:
        print("[FAIL] Hospital login failed.")

if __name__ == "__main__":
    verify_ui()
