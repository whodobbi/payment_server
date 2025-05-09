# from django.contrib.admin import AdminSite
from unfold.sites import UnfoldAdminSite
from payments.admin import InvoiceAdmin, PaymentAttemptAdmin
from payments.models import Invoice, PaymentAttempt


# class ClassicAdminSite(AdminSite):
class ClassicAdminSite(UnfoldAdminSite):
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

    def each_context(self, request):
        context = super().each_context(request)
        context["site_header"] = self.site_header
        context["site_title"] = self.site_title
        return context

classic_admin_site = ClassicAdminSite(name="classic")
classic_admin_site.register(Invoice, InvoiceAdmin)
classic_admin_site.register(PaymentAttempt, PaymentAttemptAdmin)
