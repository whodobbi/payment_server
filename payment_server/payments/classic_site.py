from django.contrib.admin import AdminSite
from payments.admin import InvoiceAdmin, PaymentAttemptAdmin
from payments.models import Invoice, PaymentAttempt


class ClassicAdminSite(AdminSite):
    site_header = "Classic Django Admin"
    site_title = "Classic Admin"
    name = "classic"

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        auth_urls = [
            path("login/", self.login, name="login"),
            path("logout/", self.login, name="logout"),
        ]
        return auth_urls + urls


classic_admin_site = ClassicAdminSite(name="classic")
classic_admin_site.register(Invoice, InvoiceAdmin)
classic_admin_site.register(PaymentAttempt, PaymentAttemptAdmin)
