import requests
from datetime import datetime
import pytz

def get_timestamp():
    try:
        # Use the timeapi.io service
        response = requests.get('https://timeapi.io/api/Time/current/zone?timeZone=UTC', timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        utc_time_str = data['dateTime']
        
        # Convert the time string to a datetime object
        utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        
        # Return the formatted timestamp
        return utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    except Exception as e:
        print(f"Error fetching time: {e}")
        return None

# Example usage
timestamp = get_timestamp()
if timestamp:
    print(f"Current UTC Time: {timestamp}")
