from rest_framework import serializers

from paste.models import Paste


class PasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paste
        fields = (
            model.title.field.name,
            model.category.field.name,
            model.author.field.name,
            model.is_published.field.name,
            model.short_link.field.name,
        )


__all__ = ()
