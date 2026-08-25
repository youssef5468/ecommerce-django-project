from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout_view, name="checkout"),
    path("confirmation/<int:order_id>/", views.order_confirmation_view, name="order_confirmation"),
    path("history/", views.order_history_view, name="order_history"),
    path("<int:order_id>/", views.order_detail_view, name="order_detail"),
    path("<int:order_id>/cancel/", views.order_cancel_view, name="order_cancel"),
]
