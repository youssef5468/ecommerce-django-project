from .models import Category


def categories(request):
    """Makes the category list available to every template (nav/footer/search)."""
    return {"categories": Category.objects.all()}
