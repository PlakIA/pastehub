from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.shortcuts import get_object_or_404, redirect, render

from paste.models import Paste
from report.forms import PersonForm, ReportForm
from report.models import ReportReview


def create(request, short_link):
    paste = get_object_or_404(Paste, short_link=short_link)

    person_form = PersonForm(None or request.POST)
    report_form = ReportForm(None or request.POST)

    if request.method == "POST" and report_form.is_valid() and person_form.is_valid():
        personal_instance = person_form.save()

        report_instance = report_form.save(commit=False)
        report_instance.person = personal_instance
        report_instance.paste = paste
        report_instance.save()

        mail.send_mail(
            subject=f'Жалоба на пасту "{paste.title}"',
            message=f'Ваша жалоба на пасту "{paste.title}" '
            f"({paste.short_link}) принята в работу",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[person_form.cleaned_data.get("email")],
        )

        messages.success(request, "Жалоба успешно отправлена")
        return redirect("paste:detail", short_link=short_link)

    return render(
        request=request,
        template_name="report/create.html",
        context={"forms": [person_form, report_form], "paste": paste},
    )


def review(request, short_link):
    paste = get_object_or_404(Paste, short_link=short_link)

    if not paste.is_blocked and request.user != paste.author:
        return redirect("paste:detail", short_link=short_link)

    ReportReview.objects.get_or_create(user=paste.author, paste=paste)

    messages.success(request, "Запрос на пересмотр успешно отправлен")

    return redirect("paste:detail", short_link=short_link)


__all__ = []
