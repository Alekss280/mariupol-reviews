from django.contrib import admin
from .models import Category, Enterprise, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'address')
    list_filter = ('category',)
    search_fields = ('name', 'address')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'enterprise', 'rating', 'sentiment', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'sentiment')
    list_editable = ('is_approved',)   # возможность менять флаг прямо в списке
    search_fields = ('text',)
    actions = ['approve_selected', 'disapprove_selected']

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)
    approve_selected.short_description = "Одобрить выбранные отзывы"

    def disapprove_selected(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_selected.short_description = "Снять одобрение с выбранных отзывов"