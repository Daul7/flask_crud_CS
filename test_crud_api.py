import requests

# --- Config ---
BASE_URL = "http://127.0.0.1:5000/company"
LOGIN_URL = "http://127.0.0.1:5000/login"
USERNAME = "admin"
PASSWORD = "adminpassword"

# --- Helper function ---
def print_response(title, response):
    print(f"\n=== {title} ===")
    print("Status Code:", response.status_code)
    try:
        print(response.json())
    except:
        print(response.text)

# --- Step 1: Login to get JWT token ---
login_resp = requests.post(LOGIN_URL, json={"username": USERNAME, "password": PASSWORD})
if login_resp.status_code != 200:
    print("Login failed:", login_resp.json())
    exit()

token = login_resp.json()["token"]
headers = {"Authorization": f"Bearer {token}"}

# --- Step 2: Test formats ---
formats = ["json", "xml"]

# --- Step 3: GET all companies ---
for fmt in formats:
    resp = requests.get(f"{BASE_URL}?format={fmt}", headers=headers)
    print_response(f"GET all companies ({fmt})", resp)

# --- Step 4: POST a new company ---
new_company = {
    "HONDA": "HondaTest",
    "YAMAHA": "YamahaTest",
    "SUZUKI": "SuzukiTest",
    "RUSI": "RusiTest",
    "KAWASAKI": "KawasakiTest"
}
resp = requests.post(BASE_URL, json=new_company, headers=headers)
print_response("POST new company", resp)
company_id = resp.json().get("id")

# --- Step 5: GET single company by ID ---
for fmt in formats:
    resp = requests.get(f"{BASE_URL}/{company_id}?format={fmt}", headers=headers)
    print_response(f"GET company ID {company_id} ({fmt})", resp)

# --- Step 6: UPDATE company ---
update_data = {
    "HONDA": "HondaUpdated",
    "YAMAHA": "YamahaUpdated",
    "SUZUKI": "SuzukiUpdated",
    "RUSI": "RusiUpdated",
    "KAWASAKI": "KawasakiUpdated"
}
resp = requests.put(f"{BASE_URL}/{company_id}", json=update_data, headers=headers)
print_response(f"PUT update company ID {company_id}", resp)

# --- Step 7: SEARCH companies (by HONDA) ---
for fmt in formats:
    resp = requests.get(f"{BASE_URL}?search=HondaUpdated&format={fmt}", headers=headers)
    print_response(f"SEARCH companies for HondaUpdated ({fmt})", resp)

# --- Step 8: DELETE company ---
resp = requests.delete(f"{BASE_URL}/{company_id}", headers=headers)
print_response(f"DELETE company ID {company_id}", resp)

# --- Step 9: GET all companies after deletion ---
for fmt in formats:
    resp = requests.get(f"{BASE_URL}?format={fmt}", headers=headers)
    print_response(f"GET all companies after deletion ({fmt})", resp)
