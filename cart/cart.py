from decimal import Decimal

from catalog.models import Product

CART_SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """Requirements 32-33, 40: add product, respecting available stock."""
        product_id = str(product.id)
        current_qty = self.cart.get(product_id, 0)
        new_qty = current_qty + quantity
        new_qty = max(1, min(new_qty, product.stock))
        self.cart[product_id] = new_qty
        self.save()

    def set_quantity(self, product, quantity):
        """Requirements 34-35, 40: increase/decrease, clamped to stock."""
        product_id = str(product.id)
        quantity = max(0, min(quantity, product.stock))
        if quantity == 0:
            self.remove(product)
        else:
            self.cart[product_id] = quantity
            self.save()

    def remove(self, product):
        """Requirement 36."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Requirement 37."""
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """Yields dicts with product, quantity, and subtotal (requirement 38)."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}
        for product_id, quantity in self.cart.items():
            product = products_map.get(product_id)
            if product is None:
                continue
            subtotal = product.price * quantity
            yield {"product": product, "quantity": quantity, "subtotal": subtotal}

    def __len__(self):
        return sum(self.cart.values())

    def get_total(self):
        """Requirement 39."""
        return sum(item["subtotal"] for item in self) or Decimal("0.00")

    def is_empty(self):
        return len(self.cart) == 0
