from datetime import datetime
from zoneinfo import ZoneInfo
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .config import DEFAULT_TIMEZONE, SENDGRID_API_KEY, DEFAULT_EMAIL

# We used ChatGPT for this since we could not figure out time zone localization with datetime
def convert_to_local_time(utc_time, timezone=DEFAULT_TIMEZONE):
    """
    Convert a UTC time string to a local timezone.
    :param utc_time: UTC time string in ISO 8601 format (e.g., "2024-12-12T18:30:00Z")
    :param timezone: Target timezone (default: "America/New_York")
    :return: Local time string in a readable format
    """
    utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")  # Parse UTC time
    local_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo(timezone))  # Convert to local timezone
    return local_dt.strftime("%A, %d %b %Y %H:%M")  # Format the local time

def format_game_dates(fixtures):
    """
    Format fixture dates for display.
    :param fixtures: List of fixtures with UTC date strings
    :return: Fixtures with formatted date strings
    """
    for fixture in fixtures.get("matches", []):
        fixture["formattedDate"] = convert_to_local_time(fixture["utcDate"])
    return fixtures.get("matches", [])

def send_email(to_email, subject, content):
    """
    Send an email using SendGrid.
    """
    try:
        message = Mail(
            from_email=DEFAULT_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=content
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent successfully! Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False