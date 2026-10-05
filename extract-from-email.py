import imaplib
import email
import re
import urllib.request
from datetime import date, timedelta
from config import *

# 1. Connect to the IMAP server
mail = imaplib.IMAP4_SSL(emailServer) # Replace with your mail server
mail.login(emailUser, emailPassword)
mail.select("inbox")

# 2. Search for the relevant email (e.g., matching the subject)
status, data = mail.search(None, '(SUBJECT "Payment Summary Export Result for")')
mail_ids = data[0].split()

if mail_ids:
    # Get the latest matching email
    latest_id = mail_ids[-1]
    status, data = mail.fetch(latest_id, "(RFC822)")
    raw_email = data[0][1]
    
    # 3. Parse the email contents
    msg = email.message_from_bytes(raw_email)
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html" or part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()

    # 4. Use Regex to find the download link containing '.csv'
    # Adjust this regex depending on how the URL looks in your specific email
    links = re.findall(r'https?://[^\s<>"]+?\.csv[^\s<>"]*', body)
    
    if not links:
        # Alternative regex if the URL doesn't end in .csv but contains a download token
        links = re.findall(r'https?://[^\s<>"]+', body)
        links = [l for l in links if "download" in l.lower()]

    if links:
        download_url = links[0]
        print(f"Found download link: {download_url}")
        
        # 5. Download and save the .csv file        
        output_file = downloadPath+"payment-report-"+(date.today()-timedelta(days=1)).strftime("%Y-%m-%d")+".csv"
        urllib.request.urlretrieve(download_url, output_file)
        print(f"File successfully saved as {output_file}")
    else:
        print("No matching CSV download link found in the email.")
else:
    print("No matching email found.")

mail.close()
mail.logout()

