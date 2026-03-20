# Sparkshed Improvement Plan

Each task below is self-contained and can be executed independently. Check off tasks as completed.

---

## Phase 1 — Critical Bug Fixes

- [ ] **1.1** Fix `create_delivery` saving records on GET requests
  - **File:** `sparkshed/views.py` (~line 309)
  - **Problem:** No `request.method == 'POST'` check. Clicking "Deliver" from the order list immediately creates a DB delivery record without any form or confirmation.
  - **Fix:** Wrap the save logic in `if request.method == 'POST':`. On GET, render an empty confirmation/delivery form.

- [ ] **1.2** Fix `return Http404()` → `raise Http404()` in 3 views
  - **Files:** `sparkshed/views.py` lines ~210 (`order_delete`), ~344 (`delivery_edit`), ~360 (`delivery_delete`)
  - **Problem:** `return Http404()` returns a 200 HTTP response with the exception object rendered as text instead of raising a proper 404 error.
  - **Fix:** Change all three occurrences to `raise Http404()`.

- [ ] **1.3** Add `@login_required` to profile views
  - **File:** `user/views.py` (`profile` and `profile_update` views)
  - **Problem:** Both views are unprotected — unauthenticated users can access them; the templates access `request.user.profile` which will fail.
  - **Fix:** Add `@login_required(login_url='user-login')` to both views.

- [ ] **1.4** Fix wrong URL name in `KitOrder.get_deliver_url()`
  - **File:** `sparkshed/models.py` line ~201
  - **Problem:** References `"delivery-create"` which is not registered. The correct registered name is `"sparkshed-delivery-create"`.
  - **Fix:** Change `reverse("delivery-create", ...)` to `reverse("sparkshed-delivery-create", ...)`.

- [ ] **1.5** Remove broken URL references on Kit and KitItem model methods
  - **File:** `sparkshed/models.py` lines ~142–178
  - **Problem:** `Kit.get_absolute_url()` and `Kit.get_hx_url()` reference `'kit-detail'` (unregistered). `KitItem.get_delete_url()` and `KitItem.get_hx_edit_url()` reference `'kit-item-delete'` and `'kit-item-detail'` (unregistered). These are leftovers from the old HTMX system. Calling them raises `NoReverseMatch`.
  - **Fix:** Remove `get_absolute_url`, `get_hx_url` from `Kit`. Remove `get_delete_url` and `get_hx_edit_url` from `KitItem`. Keep `Kit.get_edit_url()` and `Kit.get_delete_url()` (these reference valid URLs).

- [ ] **1.6** Fix template syntax error in `kit_create.html` line 1
  - **File:** `templates/dashboard/kit_create.html` line 1
  - **Problem:** Trailing `>` after extends tag: `{% extends 'partials/base.html' %}>`.
  - **Fix:** Remove the trailing `>`.

- [ ] **1.7** Make `createsu` management command idempotent
  - **File:** `sparkshed/management/commands/createsu.py`
  - **Problem:** The command always tries to create `admin/admin` without checking if the user exists. Running `build.sh` twice (or running locally after a deploy) will fail or silently corrupt.
  - **Fix:** Check `User.objects.filter(username='admin').exists()` and return early if already created.

---

## Phase 2 — Local Development Setup

- [ ] **2.1** Switch default dev database from MySQL to SQLite
  - **File:** `sparkshed/settings.py`
  - **Problem:** Local dev requires a MySQL server, `DEVELOPMENT_MODE=True`, an `inventory` database, and root access with no password — a complex and fragile setup.
  - **Fix:** Remove `DEVELOPMENT_MODE` branch. New logic:
    - If `DATABASE_URL` env var is set: use `dj_database_url.config()` (covers production and local Postgres)
    - Otherwise: use SQLite (`BASE_DIR / 'db.sqlite3'`)
  - Also add `db.sqlite3` to `.gitignore`.

- [ ] **2.2** Add `.env.example` file
  - **File:** `.env.example` (new)
  - **Content:** Document all environment variables (`SECRET_KEY`, `DATABASE_URL`, `RENDER_EXTERNAL_HOSTNAME`) with example values and explanations. Reference this from README.

- [ ] **2.3** Clean up `requirements.txt` — remove unused packages
  - **File:** `requirements.txt`
  - **Remove:**
    - `django-autocomplete-light==3.9.7` (never used — `filter.py` is empty)
    - `django-easy-select2==1.5.8` (duplicate concern, unused)
    - `django-selectable==1.4.0` (unused)
    - `django-htmx-autocomplete==0.7.1` (unused)
    - `django-select2==8.1.2` (unused — verify no templates reference it first)
    - `mysqlclient==2.1.1` (after SQLite switch in 2.1)
    - `six==1.16.0` (Python 2 compat lib, unnecessary in Python 3)
    - `Pillow==9.2.0` (only needed for `Profile.image` — keep if profile image upload is intended)

- [ ] **2.4** Add `docker-compose.yml` for containerized dev
  - **File:** `docker-compose.yml` (new)
  - A minimal file that builds the Django app and serves it. Uses SQLite by default (no extra container needed). Optionally includes a Postgres service if `DATABASE_URL` is set.
  - Include a `Dockerfile` if one doesn't already exist.

---

## Phase 3 — Security & Data Model Fixes

- [ ] **3.1** Fix SQL injection risk in `ItemManager` raw SQL queries
  - **File:** `sparkshed/models.py` lines ~23–29 and ~61–66
  - **Problem:** Two raw SQL queries use Python f-string interpolation of `item_ids` list. While item IDs are integers from the ORM (low immediate risk), this is bad practice.
  - **Fix:** Use parameterized queries:
    ```python
    placeholders = ','.join(['%s'] * len(item_ids))
    sql = f"... WHERE ki.item_id IN ({placeholders})"
    cursor.execute(sql, item_ids)
    ```

- [ ] **3.2** Fix `ItemDelivery.clean()` stock validation
  - **File:** `sparkshed/models.py` lines ~222–224
  - **Problem:** `if self.item.quantity < self.order.order_quantity` only checks raw stock, not how much is already allocated to other pending orders or already delivered. Allows overselling.
  - **Fix:** Replace with a query that calculates actual remaining stock:
    ```python
    from django.db.models import Sum, Coalesce, Value
    already_delivered = ItemDelivery.objects.filter(item=self.item).exclude(pk=self.pk).aggregate(
        total=Coalesce(Sum('order__order_quantity'), Value(0))
    )['total']
    available = self.item.quantity - already_delivered
    if available < self.order.order_quantity:
        raise ValidationError(...)
    ```

- [ ] **3.3** Add `created_date` field to `Order` abstract model
  - **File:** `sparkshed/models.py`
  - **Problem:** The abstract `Order` class only has `updated_date = auto_now`. There is no creation timestamp for audit purposes.
  - **Fix:** Add `created_date = models.DateTimeField(auto_now_add=True)` to `Order`. Run `python manage.py makemigrations && python manage.py migrate`.

---

## Phase 4 — Code Quality Cleanup

- [ ] **4.1** Delete dead template files from old HTMX system
  - **Files to delete:**
    - `templates/dashboard/kit_create_old_htmx.html`
    - `templates/partials/kit-item-inline.html`
    - `templates/partials/kit-item-form.html`
    - `templates/partials/kit-item-inline-delete-response.html`
    - `templates/partials/kit-details.html`
    - `templates/partials/forms.html`
  - **Also:** Remove the dead HTMX toast block from `templates/dashboard/order.html` (the `htmx.on("showMessage", ...)` listener and Bootstrap Toast element — nothing currently triggers this event).
  - **Also:** Delete `sparkshed/filter.py` (empty placeholder file).

- [ ] **4.2** Fix duplicate jQuery loading in `base.html`
  - **File:** `templates/partials/base.html`
  - **Problem:** jQuery is loaded twice — once in `<head>` and once before `</body>`.
  - **Fix:** Remove the duplicate `<script>` tag from the `<head>` section.

- [ ] **4.3** Fix `customer_detail` view
  - **File:** `sparkshed/views.py` (`customer_detail` function, ~line 84)
  - **Problem:** The view ignores the `pk` parameter entirely and returns all `User` objects. Context key is `customers` (plural) not `customer`.
  - **Fix:** Use `get_object_or_404(User, pk=pk)` and pass the single user to context. Update the template to display a single customer's details.

- [ ] **4.4** Fix delivery list page to show both kit and item deliveries
  - **File:** `templates/dashboard/delivery.html`
  - **Problem:** Template only loops over `kit_deliveries`. The `delivery` view in `views.py` passes both `kit_deliveries` and `item_deliveries` in context, but item deliveries are never rendered.
  - **Fix:** Add a section/table for `item_deliveries` in the template.

- [ ] **4.5** Fix `stats_bar` context processor — skip unauthenticated requests
  - **File:** `sparkshed/context_processors.py`
  - **Problem:** Runs 5 `COUNT` SQL queries on every single request — including unauthenticated requests (login page, static files, etc).
  - **Fix:** Add early return at top of function:
    ```python
    if not request.user.is_authenticated:
        return {}
    ```

- [ ] **4.6** Fix Post-Redirect-Get violation in `_create_order`
  - **File:** `sparkshed/views.py` (`_create_order` helper, ~line 173)
  - **Problem:** After a successful order, the view re-renders the template instead of redirecting. This means refreshing the page re-submits the order. Also passes the wrong form in context (kit form vs item form mixup).
  - **Fix:** After `form.save()`, redirect to `reverse('sparkshed-orders')`.

- [ ] **4.7** Improve Django admin registrations
  - **File:** `sparkshed/admin.py`
  - **Problem:** All models use default `ModelAdmin` with no customization. `ItemDelivery` and `KitDelivery` are not registered at all.
  - **Fix:**
    - Register `ItemDelivery` and `KitDelivery`
    - Add `list_display` to Item, Kit, KitOrder, ItemOrder, KitDelivery, ItemDelivery
    - Add `search_fields` to Item (`name`), KitOrder/ItemOrder (`recipient`, `customer__username`)
    - Add `list_filter` to orders and deliveries

- [ ] **4.8** Fix `KitItemFormSet can_delete` mismatch
  - **Files:** `sparkshed/forms.py`, `sparkshed/views.py`, `templates/dashboard/kit_create.html`
  - **Problem:** Formset is declared with `can_delete=False`, but the view manually handles DELETE by checking `form.cleaned_data.get('DELETE')`. Also, JS-dynamically-added rows use prefix `kititem_set-N-DELETE` which doesn't match Django's actual prefix for the formset (`kititems-N-DELETE`).
  - **Fix:** Set `can_delete=True` on `KitItemFormSet`. Remove the manual DELETE aggregation logic in `create_or_edit_kit`. Update the JS in `kit_create.html` to use the correct formset prefix (`kititems`).

---

## Phase 5 — Tests

- [ ] **5.1** Write model tests
  - **File:** `sparkshed/tests.py`
  - Tests:
    - `test_item_manager_quantity_calculation` — `with_quantities_and_kits()` returns correct `_quantity_ordered` and `_quantity_delivered`
    - `test_kit_order_deliver_url_resolves` — `KitOrder.get_deliver_url()` doesn't raise `NoReverseMatch`
    - `test_item_delivery_clean_rejects_overdelivery` — delivering more than stock raises `ValidationError`
    - `test_kit_order_form_clean_rejects_insufficient_stock` — `KitOrderForm` rejects when stock is insufficient

- [ ] **5.2** Write view tests (critical path)
  - **File:** `sparkshed/tests.py`
  - Tests:
    - `test_create_delivery_get_does_not_save` — GET to `sparkshed-delivery-create` should not create any delivery records
    - `test_order_delete_invalid_type_raises_404` — invalid type param returns 404, not 200
    - `test_profile_requires_login` — anonymous GET to `/user/profile/` redirects to login
    - `test_profile_update_requires_login` — anonymous GET to `/user/profile/update/` redirects to login
    - `test_createsu_idempotent` — calling management command twice doesn't raise

- [ ] **5.3** Write basic CRUD smoke tests
  - **File:** `sparkshed/tests.py`
  - Tests:
    - `test_items_list_authenticated` — authenticated GET to items page returns 200
    - `test_create_item_post` — POST creates an item and redirects
    - `test_create_kit_order_post` — POST creates a kit order and redirects
    - `test_order_list_authenticated` — orders page returns 200

---

## README Update

- [ ] **6.1** Update README.md with simplified setup instructions
  - Remove MySQL setup section
  - Add: `cp .env.example .env` step
  - Add: SQLite is default, no DB setup needed for local dev
  - Add: `python manage.py runserver` as the one-liner to start
  - Update TODO list to reflect completed items
