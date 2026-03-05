import html
import re

def sanitize_string(value: str) -> str:
    """
    Sanitize a string to prevent XSS and other injection attacks.
    """
    if not isinstance(value, str):
        value = str(value)
    # HTML Escape
    value = html.escape(value)
    # Aggressive Scrubbing
    value = re.sub(r"&lt;script.*?&gt;.*?&lt;/script&gt;", "", value, flags=re.DOTALL)
    # Null Byte Removal
    value = value.replace("\0", "")
    return value

def sanitize_email(email: str) -> str:
    """
    Sanitize and validate an email address format.
    """
    email = sanitize_string(email)
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        raise ValueError("Invalid email format")
    return email.lower()
