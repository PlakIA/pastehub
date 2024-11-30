from django import forms

from core.froms import BootstrapFormMixin
from paste.models import Paste


class PasteForm(BootstrapFormMixin, forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(),
        label="Содержимое",
        required=True,
    )

    class Meta:
        model = Paste
        fields = [model.title.field.name, model.category.field.name]

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if content and len(content.encode("utf-8")) > 10 * 1024 * 1024:
            raise forms.ValidationError("Содержимое не должно превышать 10 МБ")

        return content


__all__ = ["PasteForm"]
