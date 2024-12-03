from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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


class ProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = users.models.CustomUser
        fields = (
            model.email.field.name,
            model.username.field.name,
            model.image.field.name,
            model.first_name.field.name,
            model.last_name.field.name,
        )

        widgets = {model.image.field.name: forms.ClearableFileInput()}


__all__ = ()
