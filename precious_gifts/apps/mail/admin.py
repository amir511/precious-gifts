from django.contrib import admin
from precious_gifts.apps.mail.models import MailTemplate

@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    # Comment out this list if you need to edit email templates
    readonly_fields = [
        'template_name',
        'mail_subject',
        'mail_body',
    ]
    
    # Comment out those two methods, if you need to delete email templates
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop('delete_selected')
        return actions