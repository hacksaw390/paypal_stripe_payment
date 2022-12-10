from django.conf import settings
from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string

def send_email(to_email: str, subject: str, text: str) -> None:
    print(settings.EMAIL_HOST_PASSWORD)
    html_message = render_to_string('mail_template.html', {'context': text})
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_message
    )
    try:
        sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except HTTPError as e:
        print(e.to_dict)