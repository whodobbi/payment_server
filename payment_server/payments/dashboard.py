from payments.models import Invoice, PaymentAttempt, InvoiceStatus, PaymentStatus


def dashboard_callback(request, context):
    invoice_counts = {
        status.label: Invoice.objects.filter(status=status).count()
        for status in InvoiceStatus
    }
    payment_counts = {
        status.label: PaymentAttempt.objects.filter(status=status).count()
        for status in PaymentStatus
    }

    context["invoice_counts"] = invoice_counts
    context["payment_counts"] = payment_counts
    return context
