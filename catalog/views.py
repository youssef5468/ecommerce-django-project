from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home_view(request):
    featured = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    return render(request, "catalog/home.html", {"featured": featured, "categories": categories})


def product_list_view(request):
    """Requirements 25, 27-31: browse, search, filter, sort active products."""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Requirement 13/27: filter by category.
    category_slug = request.GET.get("category")
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Requirement 27: search by name/title (description included for usefulness).
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Requirement 29: optional min/max price filter.
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Requirement 30: ordering by price or name.
    sort = request.GET.get("sort", "")
    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "name_asc": "name",
        "name_desc": "-name",
    }
    if sort in sort_map:
        products = products.order_by(sort_map[sort])

    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
        "query": query,
        "min_price": min_price or "",
        "max_price": max_price or "",
        "sort": sort,
    }
    return render(request, "catalog/product_list.html", context)


def product_detail_view(request, slug):
    """Requirement 26."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})
