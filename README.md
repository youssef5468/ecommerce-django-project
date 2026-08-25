# E-Commerce — Django Final Project

Full-stack Django (MVT) e-commerce app. Frontend is the **Electro** theme
(Bootstrap, by ThemeWagon/Colorlib) converted into Django templates, plus six
pages that didn't exist in the original theme (login, register, profile,
cart, order confirmation, order history/detail) built to match its style.

## Project layout

```
ecommerce_project/   # settings.py, urls.py — project config
accounts/            # custom User model (email login + Egyptian phone), auth views
catalog/             # Category, Product models — browsing, search, filter, sort
cart/                # session-based cart (no DB table, per spec)
orders/              # checkout, Order/OrderItem, order history
templates/            # base.html + one folder per app
static/               # css/js/fonts/img copied from the Electro theme
```

## Setup

1. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create the PostgreSQL database** (you already used Postgres in the course)
   ```bash
   createdb ecommerce_db
   ```

3. **Copy the environment file and adjust if needed**
   ```bash
   cp .env.example .env
   ```
   Then either `pip install python-decouple` and load it, or just `export`
   the values from `.env` before running `manage.py` — the settings already
   read `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` from the
   environment with safe local defaults (`postgres`/`postgres`/`localhost`).

4. **Migrate and create an admin account**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **(Optional) Seed a few demo products so the site isn't empty**
   ```bash
   python manage.py seed_demo_data
   ```

6. **Run it**
   ```bash
   python manage.py runserver
   ```
   Site: http://127.0.0.1:8000/  •  Admin: http://127.0.0.1:8000/admin/

## Requirement checklist (maps 1:1 to the project PDF)

| # | Requirement | Where it lives |
|---|---|---|
| 1-5 | Registration, unique email, password confirm, Egyptian phone validation | `accounts/forms.py: RegisterForm`, `accounts/models.py: egyptian_phone_validator` |
| 6-7 | Login/logout by email | `accounts/backends.py: EmailAuthBackend`, `accounts/views.py` |
| 8 | Profile page | `accounts/views.py: profile_view` |
| 9 | Customer-only pages blocked when logged out | `@login_required` on checkout/profile/order views |
| 10-12 | Category CRUD, delete blocked if it has products | Django Admin + `Product.category` uses `on_delete=PROTECT` |
| 13-14 | Browse by category, one category per product | `catalog/views.py: product_list_view` |
| 15-24 | Product CRUD + fields (name, description, price, stock, image, category, active flag) | Django Admin, `catalog/models.py: Product` |
| 25-26 | View active products / product detail page | `catalog/views.py`, `templates/catalog/product_detail.html` |
| 27-31 | Search, category filter, price range, sort, "no results" message | `catalog/views.py: product_list_view`, `templates/catalog/product_list.html` |
| 32-41 | Cart: add/qty/increase/decrease/remove/clear, subtotal/total, stock cap, session-based | `cart/cart.py`, `cart/views.py` |
| 42-50 | Checkout: auth required, shipping form, review, server-side total, Order+OrderItem, stock reduction, cart clear, redirect | `orders/views.py: checkout_view` |
| 51-54 | Order history, order detail, owner-only access | `orders/views.py: order_history_view`, `order_detail_view` (uses `get_object_or_404(..., customer=request.user)`) |

## Notes for the team (worth knowing before you're asked about the code)

- **Why no cart model?** The spec explicitly says the cart lives in the
  session, so `cart/cart.py` stores `{product_id: quantity}` straight in
  `request.session` — nothing is written to the database until checkout.
- **Why is the total recalculated at checkout instead of trusted from the
  cart page?** Requirement 45 says the server must calculate the total.
  `checkout_view` re-reads each product's live price and re-checks stock
  right before creating the order, inside `transaction.atomic()`, so a
  half-finished order (order created but stock not reduced, or vice versa)
  can't happen if something fails mid-way.
- **Why a custom `User` model instead of Django's default?** The default
  user logs in with a username; the spec requires email + password login
  and a validated Egyptian phone number, so `accounts/models.py` extends
  `AbstractUser` with those fields and a custom auth backend.
- **Order ownership check:** `order_detail_view` fetches the order with
  `customer=request.user` in the same query — if it belongs to someone
  else, Django returns a plain 404, so you can't even tell whether the
  order ID exists.

## Not yet done

- The original theme's header had a live-preview cart dropdown (thumbnails
  on hover) built with static demo data. That was dropped in favor of a
  simple cart counter linking to the real `/cart/` page — the dropdown
  wasn't in the project spec and would need extra JS/AJAX to stay in sync
  with real data.
- Deployment config (Render, custom domain) — ask when you're ready for
  that phase.
