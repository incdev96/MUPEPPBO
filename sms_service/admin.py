from django.contrib import admin
from .models import Mutualist, Sms, SmsDetails
from . import tasks
from django.contrib import messages
from django.utils.translation import ngettext

@admin.register(Mutualist)
class MutualistAdmin(admin.ModelAdmin):
    list_display = ["full_name", 'phone']


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ["content",]
    actions = ["send_sms"]


    @admin.action(description="Envoyez le message à tous les mutualistes")
    def send_sms(self, request, queryset):

        phone_numbers = Mutualist.objects.values_list('phone', flat=True)
        for qs in queryset.all():
            tasks.send_mass_sms_task.delay(phone_numbers, qs.content)
        
        self.message_user(
            request,
            ngettext("Message envoyé à tous les mutualistes"),
            messages.SUCCESS,
        )


@admin.register(SmsDetails)
class SmsDetailsAdmin(admin.ModelAdmin):
    list_display = ["mutualist", "sms", "recepted"]
