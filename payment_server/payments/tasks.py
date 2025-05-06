from __future__ import annotations

from celery import shared_task
from django.utils import timezone

from payments.models import Invoice, InvoiceStatus


@shared_task
def mark_invoice_as_expired(invoice_id: int) -> None:
    """Celery task to mark an invoice as expired if it is still pending."""

    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        if invoice.status == InvoiceStatus.PENDING and invoice.due_at < timezone.now():
            invoice.status = InvoiceStatus.EXPIRED
            invoice.save()
    except Invoice.DoesNotExist:
        return
