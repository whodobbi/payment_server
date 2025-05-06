from unfold.admin import ModelAdmin as UnfoldModelAdmin
from payments.admin import InvoiceAdmin, PaymentAttemptAdmin


class InvoiceUnfoldAdmin(InvoiceAdmin, UnfoldModelAdmin):
    pass


class PaymentAttemptUnfoldAdmin(PaymentAttemptAdmin, UnfoldModelAdmin):
    pass
