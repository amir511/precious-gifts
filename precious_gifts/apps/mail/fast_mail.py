from django.core.mail import send_mail, mail_admins
from django.conf import settings
from threading import Thread
from precious_gifts.apps.mail.models import MailTemplate
from logzero import logger
from html2text import html2text


def send_fast_mail(email_to, template_name, context):
    try:
        template = MailTemplate.objects.get(template_name=template_name)
    except MailTemplate.DoesNotExist:
        logger.error("Couldn't find the requested email template, mail not sent!")
        return False

    html_body = template.mail_body.format(**context)
    text_body = html2text(html_body)
    recipient_list = [email_to] if isinstance(email_to, str) else email_to

    params = {
        'subject': template.mail_subject,
        'message': text_body,
        'html_message': html_body,
    }

    if email_to == 'admins':
        t = Thread(target=mail_admins, kwargs=params)
    else:
        params['from_email'] = settings.DEFAULT_FROM_EMAIL
        params['recipient_list'] =  recipient_list
        t = Thread(target=send_mail, kwargs=params)
    
    t.start()
    return True
