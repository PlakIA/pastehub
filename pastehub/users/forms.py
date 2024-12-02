from django.contrib.auth.forms import UserCreationForm

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


__all__ = ()
