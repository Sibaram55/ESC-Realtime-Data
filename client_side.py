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
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

load_dotenv()

API_URL = os.getenv("API_URL")
SECRET_KEY = os.getenv('SECRET_KEY')


def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
        

data = load_data_from_json('payload.json')

# print(data,'lllllllll')


data_json = json.dumps(data)




# AES Encryption - encrypt the payload data

def encrypt_data(data, secret_key):

    key = hashlib.sha256(secret_key.encode()).digest()[:16] 
    
    # print(key,'secret_key_encoded')

    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])  
    # print(cipher,'cipher_key')

    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))  
    # print(encrypted_data,'full_encryted_data')

    return base64.b64encode(encrypted_data).decode('utf-8')




# HMAC Signature - generate the signature for integrity and authentication


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




# Generate timestamp (to ensure it's within a valid range)

def get_timestamp():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')  # Use a public NTP server
        ntp_time = datetime.fromtimestamp(response.tx_time, tz=pytz.UTC)
        return ntp_time.strftime('%Y-%m-%dT%H:%M:%SZ')  # Return timestamp in required format
    except Exception as e:
        print(f"Error fetching NTP time: {e}")
        return None




# Prepare headers with Timestamp and Signature

# timestamp = get_timestamp()

timestamp = data[0]['timestamp']

signature = generate_signature(data, SECRET_KEY, timestamp)
b= get_timestamp()

headers = {
    'Timestamp': timestamp,
    'Signature': signature,
    'Authorization': 'Bearer ' + SECRET_KEY
}


# Encrypt the data before sending it
encrypted_data = encrypt_data(data_json, SECRET_KEY)

# Prepare the payload to send to the server
payload = {
    "data": encrypted_data,
    "metadata": {
        "data_format": "JSON",
        "encryption_method": "AES-256-CBC",
        "timestamp": timestamp
    }
}

# print(payload,'payload')

with open('payload.json', 'r') as f:
    data = json.load(f)
curr_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

data[0]['timestamp'] = get_timestamp()

with open('payload.json', 'w') as f:
    json.dump(data, f, indent=2)

# Send the POST request
response = requests.post(API_URL, json=payload, headers=headers, verify=False)

# Print the response from the server
print(response.status_code)
print(response.json())

