from django.contrib import admin

from core.models import WebsiteConfiguration

from solo.admin import SingletonModelAdmin


admin.site.register(WebsiteConfiguration, SingletonModelAdmin)
# admin.site.register(WebsiteConfiguration)