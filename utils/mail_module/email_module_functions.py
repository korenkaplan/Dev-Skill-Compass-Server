from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from dotenv import load_dotenv
import os

from utils.functions import get_formatted_date_time_now
load_dotenv()


def send_scan_recap_email(recipient_email, website_name, date_and_time, text):
    """
    Send a recap email with scan results.

    Args:
        recipient_email (str): The recipient's email address.
        website_name (str): The name of the website being scanned.
        date_and_time (str): The date and time of the scan.
        text (str): The text content of the scan results.
    """
    subject = f'Skills Compass: Scan Result Of {website_name}!'
    from_email = os.environ.get('EMAIL_HOST_USER')
    to_email = recipient_email

    # Context variables to pass to the template
    context = {
        'website_name': website_name,
        'date_and_time': date_and_time,
        'text': text
    }

    # Render the HTML template with context
    html_content = render_to_string('scan_result_template.html', context)
    text_content = strip_tags(html_content)  # Fallback text content

    # Create the email message
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")

    # Send the email
    try:
        email.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


def send_recap_email_prepared(text: str, website_name: str):
    """
    Send a prepared recap email with scan results.

    Args:
        text (str): The text content of the scan results.
        website_name (str): The name of the website being scanned.
    """
    recipient_email = os.environ.get('EMAIL_HOST_USER')
    date_and_time = get_formatted_date_time_now()

    try:
        send_scan_recap_email(recipient_email, website_name, date_and_time, text)
    except Exception as e:
        print(f"Error sending email: {e}")
