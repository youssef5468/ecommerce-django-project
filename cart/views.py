from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product

from .cart import Cart


def cart_detail_view(request):
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart})


@require_POST
def cart_add_view(request, product_id):
    """Requirements 32-33."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
    else:
        cart.add(product, quantity=quantity)
        messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart:cart_detail")


@require_POST
def cart_update_view(request, product_id):
    """Requirements 34-35: increase/decrease via a single +/- form post."""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    action = request.POST.get("action")
    current = cart.cart.get(str(product.id), 0)
    if action == "increase":
        cart.set_quantity(product, current + 1)
    elif action == "decrease":
        cart.set_quantity(product, current - 1)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove_view(request, product_id):
    """Requirement 36."""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.info(request, "Item removed from your cart.")
    return redirect("cart:cart_detail")


@require_POST
def cart_clear_view(request):
    """Requirement 37."""
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Your cart is now empty.")
    return redirect("cart:cart_detail")
