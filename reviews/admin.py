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
    list_display = ('id', 'enterprise', 'rating', 'sentiment', 'created_at')
    list_filter = ('rating', 'sentiment', 'enterprise__category')
    search_fields = ('text',)
    readonly_fields = ('created_at', 'sentiment')