from datetime import datetime, timezone


curr_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

print(curr_timestamp)