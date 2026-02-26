import requests
import json
import os

BASE_URL = 'http://127.0.0.1:5000'
SESSION = requests.Session()

def get_csrf_token(html_content):
    import re
    match = re.search(r'name="csrf_token" value="([^"]+)"', html_content)
    if match:
        return match.group(1)
    return None

def login(username, password):
    res = SESSION.get(f'{BASE_URL}/auth/login')
    csrf_token = get_csrf_token(res.text)
    
    data = {
        'username': username,
        'password': password,
        'csrf_token': csrf_token,
        'submit': 'Sign In'
    }
    res = SESSION.post(f'{BASE_URL}/auth/login', data=data)
    if "Invalid username or password" in res.text:
        print(f"Failed to login as {username}")
        return False
        
    # Also save the CSRF token in session headers for future POSTs
    SESSION.headers.update({'X-CSRFToken': csrf_token})
    print(f"Logged in as {username}")
    return True

def reset_fl():
    res = SESSION.post(f'{BASE_URL}/api/fl/reset')
    print("Reset FL:", res.json())

def test_hospital_train():
    res = SESSION.post(f'{BASE_URL}/api/fl/train')
    try:
        print("Hospital Train:", res.json())
        return res.json().get('metrics')
    except Exception as e:
        print("Hospital Train Error:", res.text)
        return None

def test_aggregate():
    res = SESSION.post(f'{BASE_URL}/api/fl/aggregate')
    try:
        print("Aggregate:", res.json())
    except:
        print("Aggregate Error:", res.text)

def test_evaluate():
    # Use hospital_client1.csv as dummy test set
    filepath = os.path.join('heart_disease_dataset', 'hospital_client1.csv')
    with open(filepath, 'rb') as f:
        files = {'file': f}
        res = SESSION.post(f'{BASE_URL}/api/fl/evaluate', files=files)
        try:
            print("Evaluate Global Model:", res.json())
        except:
            print("Evaluate Error:", res.text)

def test_history():
    res = SESSION.get(f'{BASE_URL}/api/fl/history')
    print("FL History:", res.json())

def test_rollback(round_num):
    res = SESSION.post(f'{BASE_URL}/api/fl/rollback/{round_num}')
    try:
        print(f"Rollback to Round {round_num}:", res.json())
    except:
        print("Rollback Error:", res.text)

if __name__ == "__main__":
    # 1. Login as Admin and reset
    login('testadmin', 'password')
    reset_fl()
    
    # 2. Login as Hospital and train
    SESSION.cookies.clear()
    login('testhospital', 'password')
    metrics = test_hospital_train()
    
    # 3. Login as Admin, Aggregate, and Evaluate
    SESSION.cookies.clear()
    login('testadmin', 'password')
    test_aggregate()
    test_evaluate()
    test_history()
    
    # 4. Train one more time
    SESSION.cookies.clear()
    login('testhospital', 'password')
    test_hospital_train()
    
    # 5. Admin aggregates round 2, then rollbacks to round 1
    SESSION.cookies.clear()
    login('testadmin', 'password')
    test_aggregate()
    test_history()
    test_rollback(1)
    test_history()
    print("End-to-end verification complete!")
