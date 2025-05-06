from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.models import Invoice, InvoiceStatus
from payments.tasks import mark_invoice_as_expired


@receiver(post_save, sender=Invoice)
def schedule_invoice_expiration(
    sender, instance: Invoice, created: bool, **kwargs
) -> None:
    """Schedule a Celery task to expire the invoice when its expiration time is reached."""
    if created and instance.status == InvoiceStatus.PENDING:
        mark_invoice_as_expired.apply_async(args=[instance.pk], eta=instance.expires_at)
