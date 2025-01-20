import requests
import json
import random
from faker import Faker
import requests
import json
import hmac
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from datetime import datetime
import pytz
import ntplib
from dotenv import load_dotenv, set_key
import os
from datetime import datetime, timezone
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

faker = Faker()

env_path = '.env'

BASE_URL = "https://mppcb-dev:9443/backend/v1"

LOGIN_ENDPOINT = "/industry/industry_login/"
VERIFY_OTP_ENDPOINT = "/industry/validate-login-otp/"
POST_INDUSTRY_DETAILS = "/esc_erc/IndustryDetails/"
POST_AMBIENT_DETAILS = "/esc_erc/AmbientDetails/"
POST_EMISSION_DETAILS = "/esc_erc/EmissionDetails/"
POST_EFFLUENT_DETAILS = "/esc_erc/EffluentDetails/"
POST_CBWTF_DETAILS = "/esc_erc/CbwtfDetails/"
POST_SUBMIT = "/esc_erc/SubmitDetails/"

def generate_email_address(fname, lname=None, domain='gmail.com'):
    fname = fname.strip().lower()
    domain = domain.strip().lower()
    if lname:
        lname = lname.strip().lower()
        email = f"{fname}.{lname}@{domain}"
    else:
        email = f"{fname}@{domain}"
    return email

def generate_mobile_number():
    first_digit = random.randint(6,9)
    remaining_digits = ''.join(str(random.randint(0, 9)) for _ in range(9))
    return f"{first_digit}{remaining_digits}"

name = faker.name()
fname = name.split(" ")[0]
lname = name.split(" ")[1]
email = generate_email_address(fname=fname, lname=lname, domain="gmail.com")

df = pd.read_csv("esc_ids.csv")

login_payload = {
    "mppcb_id":mppcb_id,
    "password":password
}

url = BASE_URL + LOGIN_ENDPOINT
requests.post(url=url, data=login_payload, verify=False)

validate_otp_payload = {
    "mppcb_id":mppcb_id,
    "otp_code":123456
}

url = BASE_URL + VERIFY_OTP_ENDPOINT
response = requests.post(url=url, verify=False, data=validate_otp_payload)

refresh_token = response.json()['data']['refresh']
access_token = response.json()['data']['access']

headers = {
    'Authorization': 'Bearer ' + access_token
}
fn0 = faker.name()
cn0 = generate_mobile_number()
em0 = generate_email_address(fname=fn0)
fn1 = faker.name()
cn1 = generate_mobile_number()
em1 = generate_email_address(fname=fn1)

def generate_latitude():
    return round(random.uniform(-90, 90), 6)

def generate_longitude():
    return round(random.uniform(-180, 180), 6)

secret_k = response['data']['secret_key']

set_key(env_path, "SECRET_KEY", secret_k)

# print(payload,'payload')

def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_timestamp():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')  # Use a public NTP server
        ntp_time = datetime.fromtimestamp(response.tx_time, tz=pytz.UTC)
        return ntp_time.strftime('%Y-%m-%dT%H:%M:%SZ')  # Return timestamp in required format
    except Exception as e:
        print(f"Error fetching NTP time: {e}")
        return None

load_dotenv()

data = load_data_from_json('payload.json')

def generate_random_val():
    return round(random.uniform(0.1, 1000), 2)

data[0]['station_id'] = ambient_id_1
data[0]['parameter'][0]['parameter_name'] = k0
data[0]['parameter'][0]['unit'] = v0
data[0]['parameter'][0]['value'] = generate_random_val()
data[0]['parameter'][1]['parameter_name'] = k1
data[0]['parameter'][1]['unit'] = v1
data[0]['parameter'][1]['value'] = generate_random_val()
data[0]['parameter'][2]['parameter_name'] = k2
data[0]['parameter'][2]['unit'] = v2
data[0]['parameter'][2]['value'] = generate_random_val()
data[0]['parameter'][3]['parameter_name'] = k3
data[0]['parameter'][3]['unit'] = v3
data[0]['parameter'][3]['value'] = generate_random_val()
data[0]['parameter'][4]['parameter_name'] = k4
data[0]['parameter'][4]['unit'] = v4
data[0]['parameter'][4]['value'] = generate_random_val()
data[0]['parameter'][5]['parameter_name'] = k5
data[0]['parameter'][5]['unit'] = v5
data[0]['parameter'][5]['value'] = generate_random_val()
data[0]['parameter'][6]['parameter_name'] = k6
data[0]['parameter'][6]['unit'] = v6
data[0]['parameter'][6]['value'] = generate_random_val()
data[0]['timestamp'] = get_timestamp()

with open('payload.json', 'w') as f:
    json.dump(data, f, indent=2)

API_URL = os.getenv("API_URL")
SECRET_KEY = os.getenv('SECRET_KEY')
data_json = json.dumps(data)

with open('payload.json', 'r') as f:
    data = json.load(f)
curr_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

timestamp = data[0]['timestamp']

def encrypt_data(data, secret_key):

    key = hashlib.sha256(secret_key.encode()).digest()[:16] 
    
    # print(key,'secret_key_encoded')

    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))

    # print(encrypted_data,'full_encryted_data')

    return base64.b64encode(encrypted_data).decode('utf-8')

def generate_signature(data, secret_key, timestamp):
    """
    Generate the HMAC signature for the data payload, ensuring that it's correctly serialized.
    """
    serialized_data = []
    for item in data:
        item_string = ''.join([f'{key}={value}' for key, value in sorted(item.items())])
        serialized_data.append(item_string)

    data_string = '&'.join(serialized_data)
    
    data_string += f"&timestamp={timestamp}"

    signature = hmac.new(secret_key.encode(), data_string.encode(), hashlib.sha256).hexdigest()
    return signature

signature = generate_signature(data, SECRET_KEY, timestamp)
b= get_timestamp()

headers = {
    'Timestamp': timestamp,
    'Signature': signature,
    'Authorization': 'Bearer ' + SECRET_KEY
}

encrypted_data = encrypt_data(data_json, SECRET_KEY)

payload = {
    "data": encrypted_data,
    "metadata": {
        "data_format": "JSON",
        "encryption_method": "AES-256-CBC",
        "timestamp": timestamp
    }
}

response = requests.post(API_URL, json=payload, headers=headers, verify=False)

# Print the response from the server
print(response.status_code)
print(response.json())

print(ambient_id_1)
print(mppcb_id)
print(password)
print(SECRET_KEY)
print(secret_k)