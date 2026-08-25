from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "product_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    def product_count(self, obj):
        return obj.products.count()

    def has_delete_permission(self, request, obj=None):
        # Requirement 12: category can only be deleted when it has no
        # dependent products. Product uses on_delete=PROTECT, which raises
        # ProtectedError automatically; this just hides the button up front.
        if obj is not None and obj.products.exists():
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
