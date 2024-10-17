from django.contrib import admin
from accounts.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "date_joined", "last_login", "is_admin")
    search_fields = ("email", "username")
    list_display_links = ("email", "username")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    readonly_fields = ("date_joined", "last_login", "password")
    ordering = ("-date_joined",)


admin.site.register(Account, AccountAdmin)
