import os

import requests
from datetime import datetime
from msal import ConfidentialClientApplication
from django.template.loader import render_to_string

def clean_date(value):
    """Return a valid date or None. Handles blank strings and multiple formats."""
    if not value or not str(value).strip():
        return None
    value = str(value).strip()
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y'):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None
    # or raise/log if you want to reject bad input


def send_email_notification(data, template_name, subject, mail_to, cc_email):
    # try:
    #     outlook = win32com.client.Dispatch("Outlook.Application")
    #     html_text = render_to_string(template_name, data)
    #     mail = outlook.CreateItem(0)
    #     mail.To = mail_to
    # mail_to = "robolution@adani.com"
    #     if cc_email:
    #         mail.cc = cc_email
    #     mail.Subject = "Compliance Governance Tracker"
    #     mail.HTMLBody = html_text
    #     if EMAIL_SENDING == True:
    #         print("final mail call")
    #         mail.Send()
    #     else:
    #         print("email sending is false")
    # except Exception as e:
    #     print("error", e)

    TENANT_ID = os.environ.get("TENANT_ID")
    print(TENANT_ID, "tena")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

    # Get access token
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=f'https://login.microsoftonline.com/{TENANT_ID}',
        client_credential=CLIENT_SECRET
    )

    token_response = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    access_token = token_response.get('access_token')

    print(access_token, "access token")
    if not access_token:
        print("Failed to get access token")
        return

    # Render HTML body
    html_text = render_to_string(template_name, data)
    print(html_text, "html textttt")

    # Prepare email payload
    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": html_text
            },
            # "toRecipients": [{"emailAddress": {"address": mail_to}}],
        }
    }

    # To and CC Email
    # import code
    # code.interact(local=dict(**globals(), **locals()))
    to_emails = [email.strip() for email in mail_to.split(',') if email.strip()]
    if cc_email:
        cc_emails = [email.strip() for email in cc_email.split(',') if email.strip()]
    else:
        cc_emails = []

    if len(to_emails) >= 1:
        email_msg["message"]["toRecipients"] = [
            {"emailAddress": {"address": email}} for email in to_emails
        ]

    if cc_email:
        if len(cc_emails) >= 1:
            email_msg["message"]["ccRecipients"] = [
                {"emailAddress": {"address": email}} for email in cc_emails
            ]

    # if cc_email:
    #     email_msg["message"]["ccRecipients"] = [{"emailAddress": {"address": cc_email}}]


    # Send email
    response = requests.post(
        f'https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json=email_msg
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    return None
