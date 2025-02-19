import requests
import json
import random
from faker import Faker
import hmac
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from datetime import datetime, timezone
import pytz
import ntplib
from dotenv import load_dotenv, set_key
import os
import urllib3
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

faker = Faker()

load_dotenv()

BASE_URL = "https://www.mppcb-keltron.com:9443/backend/v1"
LOGIN_ENDPOINT = "/industry/industry_login/"
VERIFY_OTP_ENDPOINT = "/industry/validate-login-otp/"
POST_INDUSTRY_DETAILS = "/esc_erc/IndustryDetails/"
POST_AMBIENT_DETAILS = "/esc_erc/AmbientDetails/"
POST_SUBMIT = "/esc_erc/SubmitDetails/"

df = pd.read_csv("/home/shyena/ESC-Parameter-Data/ESC-Realtime-Data/esc_ids_irregular.csv")

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
    first_digit = random.randint(6, 9)
    remaining_digits = ''.join(str(random.randint(0, 9)) for _ in range(9))
    return f"{first_digit}{remaining_digits}"

def generate_station_id():
    random_number = random.randint(30, 9999999)
    station_id = f"Ambient_Station_{random_number}"
    return station_id

def generate_latitude():
    return round(random.uniform(-90, 90), 6)

def generate_longitude():
    return round(random.uniform(-180, 180), 6)

def get_timestamp():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        ntp_time = datetime.fromtimestamp(response.tx_time, tz=pytz.UTC)
        return ntp_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    except Exception as e:
        print(f"Error fetching NTP time: {e}")
        return None

def generate_random_val():
    return round(random.uniform(2, 900), 2)

def encrypt_data(data, secret_key):
    key = hashlib.sha256(secret_key.encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(encrypted_data).decode('utf-8')

def generate_signature(data, secret_key, timestamp):
    serialized_data = []
    for item in data:
        item_string = ''.join([f'{key}={value}' for key, value in sorted(item.items())])
        serialized_data.append(item_string)

    data_string = '&'.join(serialized_data)
    data_string += f"&timestamp={timestamp}"
    signature = hmac.new(secret_key.encode(), data_string.encode(), hashlib.sha256).hexdigest()
    return signature

def load_data_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def run_script_for_row(mppcb_id, secret_key, ambient_id, emission_id, effluent_id):
    set_key('.env', "SECRET_KEY", secret_key)
    print(secret_key)

    # ambient_parameters = {
    #     "PM 2.5": "µg/m³",
    #     "PM 10": "µg/m³",
    #     "CO": "mg/m³",
    #     "NH3": "µg/m³",
    #     "O3 (Ozone)": "µg/m³",
    #     "Nitrogen Dioxide": "µg/m³",
    #     "Sulphur Dioxide": "µg/m³"
    # }
    
    # ambient_param_list = list(ambient_parameters.items())
    # random.shuffle(ambient_param_list)

    # k0, v0 = ambient_param_list[0]
    # k1, v1 = ambient_param_list[1]
    # k2, v2 = ambient_param_list[2]
    # k3, v3 = ambient_param_list[3]
    # k4, v4 = ambient_param_list[4]
    # k5, v5 = ambient_param_list[5]
    # k6, v6 = ambient_param_list[6]

    payload = load_data_from_json('/home/shyena/ESC-Parameter-Data/ESC-Realtime-Data/payload-irregular.json')

    # payload[0]['station_id'] = ambient_id
    # payload[0]['parameter'][0]['parameter_name'] = k0
    # payload[0]['parameter'][0]['unit'] = v0
    # payload[0]['parameter'][0]['value'] = generate_random_val()
    # payload[0]['parameter'][1]['parameter_name'] = k1
    # payload[0]['parameter'][1]['unit'] = v1
    # payload[0]['parameter'][1]['value'] = generate_random_val()
    # payload[0]['parameter'][2]['parameter_name'] = k2
    # payload[0]['parameter'][2]['unit'] = v2
    # payload[0]['parameter'][2]['value'] = generate_random_val()
    # payload[0]['parameter'][3]['parameter_name'] = k3
    # payload[0]['parameter'][3]['unit'] = v3
    # payload[0]['parameter'][3]['value'] = generate_random_val()
    # payload[0]['parameter'][4]['parameter_name'] = k4
    # payload[0]['parameter'][4]['unit'] = v4
    # payload[0]['parameter'][4]['value'] = generate_random_val()
    # payload[0]['parameter'][5]['parameter_name'] = k5
    # payload[0]['parameter'][5]['unit'] = v5
    # payload[0]['parameter'][5]['value'] = generate_random_val()
    # payload[0]['parameter'][6]['parameter_name'] = k6
    # payload[0]['parameter'][6]['unit'] = v6
    # payload[0]['parameter'][6]['value'] = generate_random_val()
    # payload[0]['timestamp'] = get_timestamp()

    emission_parameters = {
        "PM 2.5": "µg/m³",
        "PM 10": "µg/m³",
        "CO": "mg/m³",
        "NH3": "µg/m³",
        "O3 (Ozone)": "µg/m³",
        "Nitrogen Dioxide": "µg/m³",
        "Sulphur Dioxide": "µg/m³"
    }
    
    emission_param_list = list(emission_parameters.items())
    random.shuffle(emission_param_list)

    k0, v0 = emission_param_list[0]
    k1, v1 = emission_param_list[1]
    k2, v2 = emission_param_list[2]
    k3, v3 = emission_param_list[3]
    k4, v4 = emission_param_list[4]
    k5, v5 = emission_param_list[5]
    k6, v6 = emission_param_list[6]

    payload[0]['station_id'] = emission_id
    payload[0]['parameter'][0]['parameter_name'] = k0
    payload[0]['parameter'][0]['unit'] = v0
    payload[0]['parameter'][0]['value'] = generate_random_val()
    payload[0]['parameter'][1]['parameter_name'] = k1
    payload[0]['parameter'][1]['unit'] = v1
    payload[0]['parameter'][1]['value'] = generate_random_val()
    payload[0]['parameter'][2]['parameter_name'] = k2
    payload[0]['parameter'][2]['unit'] = v2
    payload[0]['parameter'][2]['value'] = generate_random_val()
    payload[0]['parameter'][3]['parameter_name'] = k3
    payload[0]['parameter'][3]['unit'] = v3
    payload[0]['parameter'][3]['value'] = generate_random_val()
    payload[0]['parameter'][4]['parameter_name'] = k4
    payload[0]['parameter'][4]['unit'] = v4
    payload[0]['parameter'][4]['value'] = generate_random_val()
    payload[0]['parameter'][5]['parameter_name'] = k5
    payload[0]['parameter'][5]['unit'] = v5
    payload[0]['parameter'][5]['value'] = generate_random_val()
    payload[0]['parameter'][6]['parameter_name'] = k6
    payload[0]['parameter'][6]['unit'] = v6
    payload[0]['parameter'][6]['value'] = generate_random_val()
    payload[0]['timestamp'] = get_timestamp()

    effluent_params = {
        "PM 2.5": "µg/m³",
        "PM 10": "µg/m³",
        "CO": "mg/m³",
        "NH3": "µg/m³",
        "O3 (Ozone)": "µg/m³",
        "Nitrogen Dioxide": "µg/m³",
        "Sulphur Dioxide": "µg/m³"
    }
    
    effluent_params_list = list(effluent_params.items())
    random.shuffle(effluent_params_list)

    k0, v0 = effluent_params_list[0]
    k1, v1 = effluent_params_list[1]
    k2, v2 = effluent_params_list[2]
    k3, v3 = effluent_params_list[3]
    k4, v4 = effluent_params_list[4]
    k5, v5 = effluent_params_list[5]
    k6, v6 = effluent_params_list[6]
    
    payload[1]['station_id'] = effluent_id
    payload[1]['parameter'][0]['parameter_name'] = k0
    payload[1]['parameter'][0]['unit'] = v0
    payload[1]['parameter'][0]['value'] = generate_random_val()
    payload[1]['parameter'][1]['parameter_name'] = k1
    payload[1]['parameter'][1]['unit'] = v1
    payload[1]['parameter'][1]['value'] = generate_random_val()
    payload[1]['parameter'][2]['parameter_name'] = k2
    payload[1]['parameter'][2]['unit'] = v2
    payload[1]['parameter'][2]['value'] = generate_random_val()
    payload[1]['parameter'][3]['parameter_name'] = k3
    payload[1]['parameter'][3]['unit'] = v3
    payload[1]['parameter'][3]['value'] = generate_random_val()
    payload[1]['parameter'][4]['parameter_name'] = k4
    payload[1]['parameter'][4]['unit'] = v4
    payload[1]['parameter'][4]['value'] = generate_random_val()
    payload[1]['parameter'][5]['parameter_name'] = k5
    payload[1]['parameter'][5]['unit'] = v5
    payload[1]['parameter'][5]['value'] = generate_random_val()
    payload[1]['parameter'][6]['parameter_name'] = k6
    payload[1]['parameter'][6]['unit'] = v6
    payload[1]['parameter'][6]['value'] = generate_random_val()
    payload[1]['timestamp'] = get_timestamp()

    with open('/home/shyena/ESC-Parameter-Data/ESC-Realtime-Data/payload-irregular.json', 'w') as f:
        json.dump(payload, f, indent=2)

    API_URL = os.getenv("API_URL")
    data_json = json.dumps(payload)
    
    with open('/home/shyena/ESC-Parameter-Data/ESC-Realtime-Data/payload-irregular.json', 'r') as f:
        data = json.load(f)
    curr_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    timestamp = data[0]['timestamp']

    signature = generate_signature(payload, secret_key, timestamp)
    b = get_timestamp()

    headers = {
    'Timestamp': timestamp,
    'Signature': signature,
    'Authorization': 'Bearer ' + secret_key
    }

    encrypted_data = encrypt_data(data_json, secret_key)

    payload = {
        "data": encrypted_data,
        "metadata": {
            "data_format": "JSON",
            "encryption_method": "AES-256-CBC",
            "timestamp": timestamp
        }
    }

    response = requests.post(API_URL, json=payload, headers=headers, verify=False)

    print(mppcb_id)
    print(response.status_code)
    print(response.json())
    
for index, row in df.iterrows():
    mppcb_id = row['mppcb_id']
    secret_k = row['secret_key']
    ambient_id = row['ambient_id']
    emission_id = row['emission_id']
    effluent_id = row['effluent_id']

    print(ambient_id)
    print(emission_id)
    print(effluent_id)
    run_script_for_row(mppcb_id, secret_k, ambient_id, emission_id, effluent_id)
