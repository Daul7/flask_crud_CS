import requests

# --- CONFIG ---
BASE_URL = "http://127.0.0.1:5000/company"
LOGIN_URL = "http://127.0.0.1:5000/login"
USERNAME = "admin"
PASSWORD = "adminpassword"

# --- GET JWT TOKEN ---
login_resp = requests.post(LOGIN_URL, json={"username": USERNAME, "password": PASSWORD})
if login_resp.status_code != 200:
    print("Login failed:", login_resp.text)
    exit()
token = login_resp.json()['token']
HEADERS = {"Authorization": f"Bearer {token}"}

# --- HELPER ---
def print_response(title, resp):
    print(f"\n=== {title} ===")
    print("Status Code:", resp.status_code)
    try:
        print(resp.json())
    except:
        print(resp.text)

# --- FORMATS ---
formats = ["json", "xml"]

# 1. GET all companies
for fmt in formats:
    resp = requests.get(f"{BASE_URL}?format={fmt}", headers=HEADERS)
    print_response(f"GET all companies ({fmt.upper()})", resp)

# 2. CREATE company
new_company = {
    "HONDA": "Honda A",
    "YAMAHA": "Yamaha B",
    "SUZUKI": "Suzuki C",
    "RUSI": "Rusi D",
    "KAWASAKI": "Kawasaki E"
}
resp = requests.post(f"{BASE_URL}?format=json", json=new_company, headers=HEADERS)
print_response("POST new company", resp)
company_id = resp.json().get("id")

# 3. GET single company
if company_id:
    for fmt in formats:
        resp = requests.get(f"{BASE_URL}/{company_id}?format={fmt}", headers=HEADERS)
        print_response(f"GET company ID {company_id} ({fmt.upper()})", resp)

# 4. UPDATE company
update_data = {
    "HONDA": "Honda Updated",
    "YAMAHA": "Yamaha Updated",
    "SUZUKI": "Suzuki Updated",
    "RUSI": "Rusi Updated",
    "KAWASAKI": "Kawasaki Updated"
}
resp = requests.put(f"{BASE_URL}/{company_id}?format=json", json=update_data, headers=HEADERS)
print_response(f"PUT update company ID {company_id}", resp)

# 5. SEARCH companies
search_terms = ["Honda", "Suzuki", "Rusi"]
for term in search_terms:
    for fmt in formats:
        resp = requests.get(f"{BASE_URL}?search={term}&format={fmt}", headers=HEADERS)
        print_response(f"SEARCH companies '{term}' ({fmt.upper()})", resp)

# 6. DELETE company
resp = requests.delete(f"{BASE_URL}/{company_id}?format=json", headers=HEADERS)
print_response(f"DELETE company ID {company_id}", resp)

# 7. GET all companies after deletion
for fmt in formats:
    resp = requests.get(f"{BASE_URL}?format={fmt}", headers=HEADERS)
    print_response(f"GET all companies after deletion ({fmt.upper()})", resp)
