from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import CheckoutForm
from .models import Order, OrderItem


@login_required
def checkout_view(request):
    """
    Requirements 42-50.
    - login_required covers requirement 42 (only authenticated users checkout).
    - Total is computed here, on the server, from live Product prices —
      never trusted from the client (requirement 45).
    - Stock is re-checked at this point (not just when items were added to
      the cart) because it may have changed since, then reduced atomically
      together with Order/OrderItem creation so a crash can't leave stock
      decremented without an order, or vice versa.
    """
    cart = Cart(request)
    if cart.is_empty():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Re-validate stock right before committing (requirement 40's
            # guarantee has to hold at checkout time too, not just at add-time).
            for item in cart:
                if item["quantity"] > item["product"].stock:
                    messages.error(
                        request,
                        f"Only {item['product'].stock} of {item['product'].name} left in stock.",
                    )
                    return redirect("cart:cart_detail")

            with transaction.atomic():
                order = Order.objects.create(
                    customer=request.user,
                    shipping_full_name=form.cleaned_data["full_name"],
                    shipping_phone=form.cleaned_data["phone"],
                    shipping_address=form.cleaned_data["address"],
                    shipping_city=form.cleaned_data["city"],
                    total_price=cart.get_total(),  # requirement 45
                )
                for item in cart:
                    product = item["product"]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item["quantity"],
                        price=product.price,
                    )
                    # Requirement 48: reduce stock after a successful order.
                    product.stock -= item["quantity"]
                    product.save(update_fields=["stock"])

            cart.clear()  # requirement 49
            return redirect("orders:order_confirmation", order_id=order.id)  # requirement 50
    else:
        form = CheckoutForm()

    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "orders/order_confirmation.html", {"order": order})


@login_required
def order_history_view(request):
    """Requirement 51."""
    orders = Order.objects.filter(customer=request.user)
    return render(request, "orders/order_history.html", {"orders": orders})


@login_required
def order_detail_view(request, order_id):
    """Requirements 52-54: only the owner can view their own order."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


# Orders that haven't shipped yet can still be cancelled by the customer.
CANCELLABLE_STATUSES = ("pending", "confirmed")


@login_required
def order_cancel_view(request, order_id):
    """
    Extra feature (not in the original spec): lets a customer cancel an
    order that hasn't shipped yet, and puts the stock back.
    Only POST is accepted so a stray link/crawler can't trigger it, and the
    owner check + status check are re-verified here even though the
    template only shows the button when it should be allowed — never trust
    the client.
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if order.status not in CANCELLABLE_STATUSES:
        messages.error(request, "This order can no longer be cancelled.")
        return redirect("orders:order_detail", order_id=order.id)

    if request.method == "POST":
        with transaction.atomic():
            for item in order.items.select_related("product"):
                item.product.stock += item.quantity
                item.product.save(update_fields=["stock"])
            order.status = "cancelled"
            order.save(update_fields=["status"])
        messages.success(request, f"Order #{order.id} was cancelled and stock was restored.")
        return redirect("orders:order_detail", order_id=order.id)

    return redirect("orders:order_detail", order_id=order.id)
