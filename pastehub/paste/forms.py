from django import forms

from core.forms import BootstrapFormMixin
from paste.models import Paste


class PasteForm(BootstrapFormMixin, forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(),
        label="Содержимое",
        required=True,
    )

    class Meta:
        model = Paste
        fields = [
            model.title.field.name,
            model.category.field.name,
        ]

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if content and len(content.encode("utf-8")) > 10 * 1024 * 1024:
            raise forms.ValidationError("Содержимое не должно превышать 10 МБ")

        return content


class ProtectForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пароль",
                "disabled": "disabled",
            },
        ),
    )

    class Meta:
        model = Paste
        fields = [model.is_protected.field.name]

        widgets = {
            model.is_protected.field.name: forms.CheckboxInput(
                attrs={"class": "form-check-input"},
            ),
        }


class GetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Ключ"},
        ),
    )


__all__ = ["GetPasswordForm", "PasteForm", "ProtectForm"]
