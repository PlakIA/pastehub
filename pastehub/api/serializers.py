from rest_framework import serializers

from core.storage import get_from_storage
from paste.models import Category, Paste
from users.models import CustomUser


class PasteSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return get_from_storage(f"pastes/{obj.id}")

    class Meta:
        model = Paste
        fields = (
            model.title.field.name,
            model.category.field.name,
            model.author.field.name,
            model.is_published.field.name,
            model.short_link.field.name,
            "content",
        )
        extra_kwargs = {"short_link": {"required": False}}


class UserSerializer(serializers.ModelSerializer):
    pastes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Paste.objects.all(),
    )

    class Meta:
        model = CustomUser
        fields = (
            model.id.field.name,
            model.username.field.name,
            model.email.field.name,
            model.first_name.field.name,
            model.last_name.field.name,
            "pastes",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (model.name.field.name,)


__all__ = ()