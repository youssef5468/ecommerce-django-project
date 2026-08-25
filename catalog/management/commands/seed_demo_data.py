from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """
    Quick demo data for local testing / showing the instructor.
    Run with: python manage.py seed_demo_data
    """
    help = "Creates a few demo categories and products."

    def handle(self, *args, **options):
        demo = {
            "Laptops": [
                ("Dell XPS 13", "Lightweight 13-inch ultrabook.", 899.99, 5),
                ("MacBook Air M2", "Apple silicon laptop.", 1199.00, 3),
            ],
            "Smartphones": [
                ("iPhone 15", "Apple's latest smartphone.", 999.00, 10),
                ("Samsung Galaxy S24", "Flagship Android phone.", 849.00, 8),
            ],
            "Accessories": [
                ("Wireless Mouse", "Ergonomic wireless mouse.", 19.99, 50),
                ("USB-C Hub", "7-in-1 USB-C hub.", 29.99, 25),
            ],
        }
        for cat_name, products in demo.items():
            category, _ = Category.objects.get_or_create(
                name=cat_name, defaults={"slug": cat_name.lower().replace(" ", "-")}
            )
            for name, desc, price, stock in products:
                Product.objects.get_or_create(
                    name=name,
                    defaults={
                        "category": category,
                        "slug": name.lower().replace(" ", "-"),
                        "description": desc,
                        "price": price,
                        "stock": stock,
                        "is_active": True,
                    },
                )
        self.stdout.write(self.style.SUCCESS("Demo categories and products created."))
