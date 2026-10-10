import re, threading
from decouple import config
from twilio.rest import Client
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

email_regex = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}")

phone_regex = re.compile(r"^\+998[0-9]{9}$")

username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")

def check_email_or_phone(email_phone_number):
    if re.fullmatch(email_regex, email_phone_number):
        email_phone_number = "email"
    elif re.fullmatch(phone_regex, email_phone_number):
        email_phone_number = "phone"
    else:
        data = {
            "success":False,
            "message": "Email or phone number is invalid",
        }
        raise ValidationError(data)
    return email_phone_number

def check_user_type(user_input):
    
    if re.fullmatch(email_regex, user_input):
           user_input = "email"
    elif re.fullmatch(phone_regex, user_input):
        user_input = "phone_number"
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"
    else:
        raise ValidationError({
            'success':False,
            'message': 'Email, username, or phone number is invalid'
        })
    return user_input

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send()
    
class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject = data['subject'],
            body = data['body'],
            to = [data['to_email']],
        )
        if data.get('content_type') == 'html':
            email.content_subtype = 'html'
        EmailThread(email).start()
        
def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {'code': code}
        )
    Email.send_email(
        {
            'subject': 'Ro\'yxatdan o\'tish',
            'body': html_content,
            'to_email': email,
            'content_type': 'html'
        }
    )
def send_phone_code(phone_number, code):
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f'Hey there, Your activation code is {code} \n',
        from_= '+998958412715',
        to= f'{phone_number}'
    )