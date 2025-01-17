import requests
import json
import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from datetime import datetime
import pytz
import ntplib
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")
SECRET_KEY = os.getenv('SECRET_KEY')


# AES Encryption - encrypt the payload data
def encrypt_data(data, secret_key):
    key = hashlib.sha256(secret_key.encode()).digest()  # Full 32-byte key
    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])  # IV is first 16 bytes of key
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(encrypted_data).decode('utf-8')


# HMAC Signature - generate the signature for integrity and authentication
def generate_signature(data, secret_key, timestamp):
    data_string = json.dumps(data, separators=(',', ':'), sort_keys=True)
    data_string += f"&timestamp={timestamp}"
    signature = hmac.new(secret_key.encode(), data_string.encode(), hashlib.sha256).hexdigest()
    return signature


# Generate timestamp (to ensure it's within a valid range)
def get_timestamp():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')  # Use a public NTP server
        ntp_time = datetime.fromtimestamp(response.tx_time, tz=pytz.UTC)
        return ntp_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    except Exception as e:
        print(f"Error fetching NTP time: {e}")
        return datetime.now(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


# Dynamic Payload Data
data = [
    {
        "station_id": "AMBIENT_STATION_102",
        "station_type": "ambient",
        "parameter": [
            {"parameter_name": "PM 2.5", "unit": "µg/m³", "value": "700", "analyzer_status": "active"},
            {"parameter_name": "Sulphur Dioxide", "unit": "µg/m³", "value": "799", "analyzer_status": "active"}
        ],
        "timestamp": get_timestamp()
    },
    {
        "station_id": "AMBIENT_STATION_103",
        "station_type": "ambient",
        "parameter": [
            {"parameter_name": "PM 10", "unit": "µg/m³", "value": "708", "analyzer_status": "active"},
            {"parameter_name": "Sulphur Dioxide", "unit": "µg/m³", "value": "580", "analyzer_status": "active"}
        ],
        "timestamp": get_timestamp()
    }
]


# Generate Timestamp and Signature
timestamp = get_timestamp()
signature = generate_signature(data, SECRET_KEY, timestamp)

# Prepare Headers
headers = {
    'Timestamp': timestamp,
    'Signature': signature,
    'Authorization': 'Bearer ' + SECRET_KEY
}

# Encrypt the Data
data_json = json.dumps(data)
encrypted_data = encrypt_data(data_json, SECRET_KEY)

# Prepare the Payload
payload = {
    "data": encrypted_data,
    "metadata": {
        "data_format": "JSON",
        "encryption_method": "AES-256-CBC",
        "timestamp": timestamp
    }
}

# Send the POST Request
try:
    response = requests.post(API_URL, json=payload, headers=headers, verify=False)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.json()}")
except Exception as e:
    print(f"Error sending request: {e}")
