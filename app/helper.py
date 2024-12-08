from datetime import datetime
from zoneinfo import ZoneInfo

# We used ChatGPT for this since we could not figure out time zone localization with datetime
def convert_to_local_time(utc_time, timezone="America/New_York"):
    """Convert a UTC time string to a local timezone."""
    utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")  # Parse UTC time
    local_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo(timezone))  # Convert to local timezone
    return local_dt.strftime("%A, %d %b %Y %H:%M")  # Format the local time