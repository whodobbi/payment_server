from unfold.sites import UnfoldAdminSite
from payments.models import Invoice, PaymentAttempt
from payments.unfold_admin import InvoiceUnfoldAdmin, PaymentAttemptUnfoldAdmin

unfold_admin_site = UnfoldAdminSite(name="unfold_admin")
unfold_admin_site.register(Invoice, InvoiceUnfoldAdmin)
unfold_admin_site.register(PaymentAttempt, PaymentAttemptUnfoldAdmin)
