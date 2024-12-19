from django import forms

from core.forms import BootstrapFormMixin
from report.models import Person, Report


class PersonForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            model.name.field.name,
            model.email.field.name,
        ]


class ReportForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Report
        fields = [model.text.field.name]


__all__ = ["PersonForm", "ReportForm"]
