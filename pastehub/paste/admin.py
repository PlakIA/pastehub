from django.contrib import admin

from core.utils import delete_from_storage
from paste.models import Category, Paste


@admin.register(Paste)
class PasteAdmin(admin.ModelAdmin):
    list_display = [
        Paste.id.field.name,
        Paste.title.field.name,
        Paste.category.field.name,
        Paste.created.field.name,
    ]

    list_filter = [
        Paste.category.field.name,
        Paste.created.field.name,
    ]

    readonly_fields = [
        Paste.is_protected.field.name,
    ]

    def delete_model(self, request, obj):
        delete_from_storage(f"pastes/{obj.pk}")
        super().delete_model(request, obj)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


__all__ = []
