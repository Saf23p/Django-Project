from django.contrib import admin, messages
from .models import Tfcargo, Category


@admin.register(Tfcargo)
class TfcargoAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'photo', 'slug', 'cat']
    # readonly_fields = ['slug']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ('time_create', 'title')
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['cat__name', 'is_published']


    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, tfcargo: Tfcargo):
        return f"Описание {len(tfcargo.content)} символов"

    @admin.action(description="Опубликовать записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Tfcargo.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Tfcargo.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации.", messages.WARNING)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


