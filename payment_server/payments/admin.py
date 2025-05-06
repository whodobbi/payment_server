from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html
from payments.models import Invoice, PaymentAttempt, InvoiceStatus, PaymentStatus


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "colored_status",
        "amount",
        "expires_at",
        "created_at",
    )
    list_filter = ("status",)
    readonly_fields = ("created_at",)

    def colored_status(self, obj: Invoice) -> str:
        color_map = {
            InvoiceStatus.PENDING: "orange",
            InvoiceStatus.PAID: "green",
            InvoiceStatus.EXPIRED: "red",
        }
        color = color_map.get(obj.status, "black")
        return format_html(f'<b style="color: {color}">{obj.get_status_display()}</b>')

    colored_status.short_description = "Status"


class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice", "colored_status", "amount", "created_at")
    list_filter = ("status",)
    readonly_fields = ("created_at",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "invoice":
            kwargs["queryset"] = Invoice.objects.filter(status=InvoiceStatus.PENDING)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def colored_status(self, obj: PaymentAttempt) -> str:
        color_map = {
            PaymentStatus.SUCCESS: "green",
            PaymentStatus.INSUFFICIENT_FUNDS: "orange",
            PaymentStatus.DECLINED: "red",
        }
        color = color_map.get(obj.status, "black")
        return format_html(f'<b style="color: {color}">{obj.get_status_display()}</b>')

    colored_status.short_description = "Status"
