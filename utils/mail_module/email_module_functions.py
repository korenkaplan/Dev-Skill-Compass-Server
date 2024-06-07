# views.py or any appropriate file
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from dotenv import load_dotenv
import os
load_dotenv()


def send_scan_recap_email(recipient_email, website_name, date_and_time, text):
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
    email.send()
