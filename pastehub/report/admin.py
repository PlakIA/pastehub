from django.conf import settings
from django.contrib import admin
from django.core import mail

from report.models import Person, Report, ReportReview


class ReportInline(admin.TabularInline):
    model = Report
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        Report.id.field.name,
        Report.paste.field.name,
        Report.status.field.name,
        Report.created.field.name,
    ]

    list_filter = [
        Report.status.field.name,
        Report.created.field.name,
    ]

    readonly_fields = [
        Report.paste.field.name,
        Report.created.field.name,
        Report.person.field.name,
        Report.text.field.name,
    ]

    def save_model(self, request, obj, form, change):
        if change:
            new_status = form.cleaned_data.get("status")
            if new_status == "approved":
                obj.paste.is_blocked = True
                obj.paste.save()
                mail.send_mail(
                    subject=f"Жалоба на пасту " f'"{obj.paste.title}"',
                    message=f'Ваша жалоба по пасте "{obj.paste.title}" '
                    f"({obj.paste.short_link}) удовлетворена, "
                    f"паста заблокирована",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.person.email],
                )

            elif new_status == "rejected":
                mail.send_mail(
                    subject=f"Жалоба на пасту " f'"{obj.paste.title}"',
                    message=f'Ваша жалоба по пасте "{obj.paste.title}" '
                    f"({obj.paste.short_link}) не удовлетворена, "
                    f"нарушения не выявлены",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.person.email],
                )

        super().save_model(request, obj, form, change)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    can_delete = False

    list_display = [
        Person.email.field.name,
    ]

    readonly_fields = [
        Person.email.field.name,
        Person.name.field.name,
    ]

    inlines = [ReportInline]


@admin.register(ReportReview)
class ReportReviewAdmin(admin.ModelAdmin):
    list_display = [
        ReportReview.id.field.name,
        ReportReview.status.field.name,
        ReportReview.paste.field.name,
        ReportReview.created.field.name,
    ]

    list_filter = [
        ReportReview.status.field.name,
        ReportReview.created.field.name,
    ]

    readonly_fields = [
        ReportReview.created.field.name,
        ReportReview.paste.field.name,
        ReportReview.user.field.name,
    ]

    def save_model(self, request, obj, form, change):
        if change:
            new_status = form.cleaned_data.get("status")
            if new_status == "approved":
                obj.paste.is_blocked = False
                obj.paste.save()

        super().save_model(request, obj, form, change)


__all__ = []
