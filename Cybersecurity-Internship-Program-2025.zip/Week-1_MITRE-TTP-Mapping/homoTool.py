import unicodedata
import string
from urllib.parse import urlparse

# Set of standard printable ASCII characters (A-Z, 0-9, punctuation, space)
standard_chars = set(string.ascii_letters + string.digits + string.punctuation + " ")
safe_invisible_chars = {'\n', '\r', '\t'}

# Check if character is standard ASCII
def is_allowed_standard_char(ch):
    return ch in standard_chars

# Check if a character is suspicious (non-standard or unsafe control char)
def is_suspicious(ch):
    if ch in safe_invisible_chars:
        return False
    if ch in standard_chars:
        return False
    return True

# Scan text for suspicious characters and return details
def scan_text(text):
    results = []
    for ch in text:
        if is_suspicious(ch):
            try:
                name = unicodedata.name(ch)
            except ValueError:
                name = "Unknown or Non-character"
            codepoint = f"U+{ord(ch):04X}"
            results.append((ch, name, codepoint))
    return results

# Extract domain part from a full URL (or treat input as a domain)
def extract_domain(url):
    parsed = urlparse(url)
    return parsed.netloc or parsed.path

# Complete scan pipeline for a domain or full URL
def scan_domain(domain_or_url):
    domain = extract_domain(domain_or_url)
    return scan_text(domain)
if __name__ == "__main__":
    url = input("Enter a domain or full URL to scan: ").strip()
    suspicious = scan_domain(url)

    if suspicious:
        print("Suspicious characters found:")
        for ch, name, code in suspicious:
            print(f" - {ch}: {name} ({code})")
    else:
        print("No suspicious characters found.")
