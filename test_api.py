import requests

BASE_URL = "http://127.0.0.1:5000"

# 1. Login to get token
login_data = {"username": "admin", "password": "adminpassword"}
login_response = requests.post(f"{BASE_URL}/login", json=login_data)
token = login_response.json().get("token")
print("Token:", token)

# 2. Use token to access /company
headers = {"Authorization": f"Bearer {token}"}
company_response = requests.get(f"{BASE_URL}/company", headers=headers)
print(company_response.json())
