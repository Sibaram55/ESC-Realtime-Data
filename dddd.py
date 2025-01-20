import pandas as pd

df = pd.read_csv("esc_ids.csv")

for index, row in df.iterrows():
    mppcb_id = row['mppcb_id']
    password = row['password']
    secret_k = row['secret_key']
    ambient_id = row['ambient_id']
    
    login_payload = {
        "mppcb_id":mppcb_id,
        "password":password
    }

    print(login_payload)