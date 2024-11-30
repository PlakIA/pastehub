from django.contrib import admin

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


__all__ = []
