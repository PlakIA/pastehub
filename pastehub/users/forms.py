from django.contrib.auth.forms import UserCreationForm
from django import forms

import users.models


class SignUpForm(UserCreationForm):
    class Meta:
        model = users.models.CustomUser
        fields = (
            model.email.field.name,
            model.username.field.name,
            "password1",
            "password2",
        )

        help_texts = {
            model.email.field.name: "Введите вашу почту",
            model.username.field.name: "Введите имя пользователя",
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = users.models.CustomUser
        fields = (
            model.email.field.name,
            model.username.field.name,
            model.image.field.name,
            model.first_name.field.name,
            model.last_name.field.name,
        )


__all__ = ()
