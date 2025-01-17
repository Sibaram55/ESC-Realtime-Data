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

faker = Faker()

env_path = '.env'

BASE_URL = "https://mppcb-dev:9443/backend/v1"

REGISTER_OTP_CREATION = "/industry/registration-otp-creation/"
VALIDATE_REGISTRATION_OTP = "/industry/validate-registration-otp/"
USER_REGISTRAION = "/industry/user-registration/"
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


register_otp_payload = {
    "mobile_number":"8281570374",
    "applicant_email":"sm60785@gmail.com",
    "alternate_mobile":"8281570375",
    "applicant_aadharcard":"123123231123",
    "applicant_pancard":None
}

url = BASE_URL + REGISTER_OTP_CREATION
requests.post(url=url, data=register_otp_payload, verify=False)

validate_registration_payload = {
    "mobile_number":"8281570374", 
    "mobile_otp":"123456",
    "applicant_email":"sm60785@gmail.com",
    "email_otp":"123456",
    "applicant_type":"self"
}

url = BASE_URL + VALIDATE_REGISTRATION_OTP
requests.post(url=url, data=validate_registration_payload, verify=False)

uat_district = 981
uat_tehsil = 307
uat_village = 51991
sdc_district = 50
sdc_tehsil = 332
sdc_village = 54273

user_registraion_payload = {
    "contact_number": "8281570374",
    "applicant_email": "sm60785@gmail.com",
    "industry_email": "ts@gmail.com",
    "sector_id": "34",
    "constitution_type": "1",
    "category": "Red Category",
    "type_of_activity": "3",
    "name_industry": fname+lname,
    "location_of_unit": "tghsgayirtyhbvft",
    "survey_plot_no": "672",
    "district": sdc_district,
    "tehsil": sdc_tehsil,      
    "village": sdc_village,
    "latitude": 23.524300,
    "longitude": 77.812200,
    "pincode": "464001",
    "applicant_fname": "John",
    "applicant_lname": "Williams",
    "applicant_designation": "Director",
    "applicant_adharcard": "397788000234",
    "applicant_pancard": "BNFOS5629J",
    "applicant_email_otp": 123456,
    "mobile_otp": 123456,
    "applicant_mobile_2": "8381570375",
    "applicant_type": "self"
}

url = BASE_URL + USER_REGISTRAION
response = requests.post(url=url, data=user_registraion_payload, verify=False)
# print(response.status_code)
# print(response.json())
mppcb_id = response.json()['data']['mppcb_id']
password = response.json()['plain_password']

# print("ID: ",  mppcb_id)
# print("Password: ", password)
login_payload = {
    "mppcb_id":mppcb_id,
    "password":password
}
# print("ID: ", mppcb_id)
# print("Password: ", password)
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
# print(fn0)
# print(cn0)
# print(em0)
# print(cn1)
# print(fn1)
# print(em1)
# print(headers)

def generate_station_id():
    random_number = random.randint(30, 9999999)
    station_id = f"Ambient_Station_{random_number}"
    return station_id

esc_industry_details_payload = {
    "no_of_caaqms": 1,
    "no_of_cems": 0,
    "no_of_ceqms": 0,
    "no_of_flow_meter": 3,
    "no_of_ip_camera": 2,
    "primary_contact_name": fn0,
    "primary_phone_number": cn0,
    "primary_email": em0,
    "secondary_contact_name": fn1,
    "secondary_phone_number": cn1,
    "secondary_email": em1,
    "data_transmission": "Pc-Server",
    "historical_data": True,
    "rtm_check":True,
    "ip_address": "192.168.2.55"
}

url = BASE_URL + POST_INDUSTRY_DETAILS
response = requests.post(url=url, verify=False, data=esc_industry_details_payload, headers=headers)

print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu", response.json())

response1 = requests.get(url=url, headers=headers, verify=False)

url = BASE_URL + POST_AMBIENT_DETAILS
response = requests.get(url=url, verify=False, headers=headers)

# print(response.json())

ambient_id_1 = response.json()["data"]["ambient_data"][0]["id"]

# print(ambient_id_1)

def generate_latitude():
    return round(random.uniform(-90, 90), 6)

def generate_longitude():
    return round(random.uniform(-180, 180), 6)

parameters = {
    "PM 2.5":"µg/m³",
    "PM 10":"µg/m³",
    "CO":"mg/m³",
    "NH3":"µg/m³",
    "O3 (Ozone)":"µg/m³",
    "Nitrogen Dioxide":"µg/m³",
    "Sulphur Dioxide":"µg/m³"
}

param_list = list(parameters.items())
random.shuffle(param_list)

k0, v0 = param_list[0]
k1, v1 = param_list[1]
k2, v2 = param_list[2]
k3, v3 = param_list[3]
k4, v4 = param_list[4]
k5, v5 = param_list[5]
k6, v6 = param_list[6]

ambient_details_payload = {
    "id":ambient_id_1,
    "station_name":generate_station_id(),
    "latitude":generate_latitude(),
    "longitude":generate_longitude(),
    "ambient_remarks":"None",
    "ip_camera_details[0][camera_port]":8080,
    "ip_camera_details[0][camera_access_link]":"https://localhost",
    # "ip_camera_details[0][file]":"",
    "ip_camera_details[0][ip_remarks]":"remarks",
    "ip_camera_details[0][ptz]":True,
    "analyzer_details":[
        {
            "analyser_make": "Analyzer Co.",
            "analyser_model": "Model X1",
            "minimum_range": "0",
            "maximum_range": "100",
            "parameter": k0,
            "unit": v0,
            "measurement_principle": "Optical",
            "stack_height": 15.5,
            "stack_diameter": 2.5,
            "stack_velocity": 5.2,
            "flue_gas_discharge_rate": 50.5
        },
        {
            "analyser_make": "Analyzer Cddo.",
            "analyser_model": "Model X2",
            "minimum_range": "0",
            "maximum_range": "100",
            "parameter": k1,
            "unit": v1,
            "measurement_principle": "Optical",
            "stack_height": 15.5,
            "stack_diameter": 2.5,
            "stack_velocity": 5.2,
            "flue_gas_discharge_rate": 50.5
        },
        {
            "analyser_make": "Analyzer Cddo.",
            "analyser_model": "Model X2",
            "minimum_range": "0",
            "maximum_range": "100",
            "parameter": k2,
            "unit": v2,
            "measurement_principle": "Optical",
            "stack_height": 15.5,
            "stack_diameter": 2.5,
            "stack_velocity": 5.2,
            "flue_gas_discharge_rate": 50.5
        },
        {
            "analyser_make": "Analyzer Cddo.",
            "analyser_model": "Model X2",
            "minimum_range": "0",
            "maximum_range": "100",
            "parameter": k3,
            "unit": v3,
            "measurement_principle": "Optical",
            "stack_height": 15.5,
            "stack_diameter": 2.5,
            "stack_velocity": 5.2,
            "flue_gas_discharge_rate": 50.5
        },
        {
            "analyser_make": "Analyzer Cddo.",
            "analyser_model": "Model X2",
            "minimum_range": "0",
            "maximum_range": "100",
            "parameter": k4,
            "unit": v4,
            "measurement_principle": "Optical",
            "stack_height": 15.5,
            "stack_diameter": 2.5,
            "stack_velocity": 5.2,
            "flue_gas_discharge_rate": 50.5
        },
        {
            "analyser_make": "Analyzer Cddo.",
            "analyser_model": "Model X2",
            "minimum_range": "0",
            "maximum_range": "100",
            "parameter": k5,
            "unit": v5,
            "measurement_principle": "Optical",
            "stack_height": 15.5,
            "stack_diameter": 2.5,
            "stack_velocity": 5.2,
            "flue_gas_discharge_rate": 50.5
        },
        {
            "analyser_make": "Analyzer Cddo.",
            "analyser_model": "Model X2",
            "minimum_range": "0",
            "maximum_range": "100",
            "parameter": k6,
            "unit": v6,
            "measurement_principle": "Optical",
            "stack_height": 15.5,
            "stack_diameter": 2.5,
            "stack_velocity": 5.2,
            "flue_gas_discharge_rate": 50.5
        }
    ]
}

url = BASE_URL + POST_AMBIENT_DETAILS
response = requests.post(url=url, headers=headers, verify=False, data=ambient_details_payload)
print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBB", response.json())
url = BASE_URL + POST_SUBMIT
response = requests.post(url=url, headers=headers, verify=False).json()

secret_k = response['data']['secret_key']
id = response['data']['mppcb_id']

# print(json.dumps(ambient_details_payload))