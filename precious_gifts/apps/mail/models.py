from django.db import models
from django.core.exceptions import ValidationError
from djangocms_text_ckeditor.fields import HTMLField

class MailTemplate(models.Model):
    template_name = models.CharField(max_length=25)
    mail_subject = models.CharField(max_length=255)
    mail_body = HTMLField()

    def __str__(self):
        return self.template_name

