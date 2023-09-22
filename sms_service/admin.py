from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Mutualist, Sms
from . import tasks
from django.contrib import messages



@admin.register(Mutualist)
class MutualistAdmin(admin.ModelAdmin):
    list_display = ["full_name", 'phone']

    search_fields = ["full_name"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs =  super().get_queryset(request)
        return qs.order_by('full_name')


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ["content",]
    actions = ["send_sms"]


    @admin.action(description="Envoyez le message à tous les mutualistes")
    def send_sms(self, request, queryset):
        
        phone_numbers = []
        access_token = tasks.get_token.delay("https://api.orange.com/oauth/v3/token").get()

        for sms in queryset:
            msg = sms.content
            mutualists = sms.mutualists.all()
            for mutualist in mutualists:
                phone_numbers.append(mutualist.phone)

        tasks.send_mass_sms_task.delay(phone_numbers, msg, access_token)
        
        self.message_user(
            request,"Message envoyé à tous les mutualistes", messages.SUCCESS,
        )