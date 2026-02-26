import requests
from bs4 import BeautifulSoup
import json

s = requests.Session()
login_url = 'http://127.0.0.1:5000/auth/login'

r1 = s.get(login_url)
soup = BeautifulSoup(r1.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

data = {
    'username': 'testadmin',
    'password': 'password',
    'csrf_token': csrf_token,
    'submit': 'Sign In'
}

r2 = s.post(login_url, data=data, allow_redirects=True)
print("Login status:", r2.status_code)

r3 = s.get('http://127.0.0.1:5000/api/users')
print("GET /api/users status:", r3.status_code)

users = r3.json()
target_id = None
for u in users:
    if u['username'] == 'testuser':
        target_id = u['id']
        break

if target_id:
    print(f"Deleting user {target_id}")
    r4 = s.delete(f'http://127.0.0.1:5000/api/users/{target_id}', allow_redirects=False)
    print("DELETE status:", r4.status_code)
    if r4.status_code == 302:
        print("Redirect Location:", r4.headers.get('Location'))
else:
    print("Test user not found")
