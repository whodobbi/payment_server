from __future__ import annotations

from django.db import models
from datetime import datetime


class InvoiceStatus(models.TextChoices):
    PENDING = "pending", "Ожидает оплату"
    PAID = "paid", "Оплачен"
    EXPIRED = "expired", "Просрочен"


class PaymentStatus(models.TextChoices):
    SUCCESS = "success", "Успешно"
    INSUFFICIENT_FUNDS = "insufficient", "Недостаточно средств"
    DECLINED = "declined", "Отказ"


class Invoice(models.Model):
    """Represents an invoice issued for payment by the system"""

    amount: int = models.PositiveIntegerField()
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    status: str = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.PENDING,
    )
    expires_at: datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.status == InvoiceStatus.PENDING:
            from payments.tasks import mark_invoice_as_expired

            mark_invoice_as_expired.apply_async((self.pk,), eta=self.expires_at)

    def __str__(self) -> str:
        return f"Invoice #{self.pk} - {self.status}"


class PaymentAttempt(models.Model):
    """Represents a user's attempt to pay a specific invoice"""

    amount: int = models.PositiveIntegerField()
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    status: str = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
    )
    invoice: Invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="attempts"
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            invoice = self.invoice

            if invoice.status == InvoiceStatus.EXPIRED:
                self.status = PaymentStatus.DECLINED

            elif invoice.status == InvoiceStatus.PENDING:
                if invoice.amount > 100:
                    self.status = PaymentStatus.INSUFFICIENT_FUNDS
                else:
                    self.status = PaymentStatus.SUCCESS
                    invoice.status = InvoiceStatus.PAID
                    invoice.save()

            else:
                self.status = PaymentStatus.DECLINED

    def __str__(self) -> str:
        return f"PaymentAttempt #{self.pk} - {self.status}"
