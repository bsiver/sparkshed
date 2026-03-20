# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sparkshed is a Django-based inventory management system for SparkShop. It manages four primary entities:
- **Items**: Individual products with names, descriptions, and quantities
- **Kits**: Collections of items (many-to-many with quantity per item)
- **Orders**: Requests for items or kits (KitOrder and ItemOrder)
- **Deliveries**: Fulfillment of orders (KitDelivery and ItemDelivery)

## Architecture

### Database Models (`sparkshed/models.py`)
The data model centers on two inheritance hierarchies:

**Orders (abstract base class):**
- `KitOrder`: Orders for kits (ForeignKey to Kit)
- `ItemOrder`: Orders for individual items (ForeignKey to Item)
- Common fields: customer (User), order_quantity, recipient, updated_date

**Deliveries (abstract base class):**
- `KitDelivery`: Fulfillment of kit orders
- `ItemDelivery`: Fulfillment of item orders
- Linked to orders via ForeignKey

**Complex Calculation Logic:**
- `ItemManager.with_quantities_and_kits()` is the core data aggregation method
  - Uses raw SQL queries to calculate `quantity_ordered` and `quantity_delivered` for each item
  - Accounts for both direct orders and orders via kits
  - Attaches `_kit_names` to items to show which kits contain them
  - Used extensively in views and templates
  - Performance-critical: makes 3 raw SQL queries, should be optimized if adding more features

### Views (`sparkshed/views.py`)
Function-based views with login_required decorator. Key patterns:
- Views often fetch raw data (e.g., `list(KitOrder.objects.all())`) rather than using query optimization
- Order and delivery views follow a pattern of rendering the full list on form submission
- Kit creation uses an inline formset (`KitItemFormSet`) with custom DELETE handling
- Delivery creation auto-populates item/kit from order

### Frontend Technology
- Bootstrap 5 via `django-crispy-forms`
- HTMX for dynamic interactions (`django-htmx` middleware enabled)
- Static files served by WhiteNoise (in production)
- FontAwesome 6.2.0 for icons

### Database Configuration
Development vs. Production use different databases:
- **DEVELOPMENT_MODE=True**: MySQL on localhost:3306 (database: `inventory`)
- **DEVELOPMENT_MODE=False** (production): PostgreSQL via `dj_database_url` (Render deployment)
- Set via `DEVELOPMENT_MODE` environment variable

## Common Development Tasks

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set DEVELOPMENT_MODE for MySQL
export DEVELOPMENT_MODE=True

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser
# OR use the custom command (sets admin/admin)
python manage.py createsu
```

### Running Locally
```bash
# Start development server
python manage.py runserver

# Navigate to http://localhost:8000 (redirects to login)
```

### Database Migrations
```bash
# Make changes to models.py, then:
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
# Needed before deployment or when adding new static assets
python manage.py collectstatic --no-input
```

### Testing
The test file (`sparkshed/tests.py`) is currently empty. Django tests follow the standard pattern:
```bash
python manage.py test sparkshed
```

### Deployment
The `build.sh` script runs on Render:
1. Installs dependencies
2. Collects static files
3. Runs migrations
4. Creates superuser

## Key Files and Their Responsibilities

| File | Purpose |
|------|---------|
| `sparkshed/models.py` | All ORM models, custom ItemManager with quantity calculations |
| `sparkshed/views.py` | All view functions (30+ functions) |
| `sparkshed/forms.py` | ModelForms, inline formset for kits, form validation |
| `sparkshed/urls.py` | URL routing (46 paths, organized by feature) |
| `sparkshed/settings.py` | Django config, database setup, installed apps |
| `sparkshed/helpers.py` | Utility functions (e.g., namedtuplefetchall for raw SQL) |
| `sparkshed/context_processors.py` | Template context processors (stats_bar) |
| `sparkshed/decorators.py` | Custom decorators (if any) |
| `user/` | User authentication and profile views (separate app) |
| `templates/dashboard/` | All templates organized by feature |

## Performance Considerations

- **ItemManager.with_quantities_and_kits()**: Makes raw SQL queries. If slow, consider database indexes on:
  - `sparkshed_kititem(item_id, kit_id)`
  - `sparkshed_kitorder(kit_id)`
  - `sparkshed_itemorder(item_id)`
- **Form rendering**: Order and delivery lists re-render entirely on form submission (not AJAX updates)
- **Static files**: WhiteNoise handles compression and caching headers in production

## Common Patterns to Follow

1. **Login-protected views**: Always use `@login_required(login_url='user-login')`
2. **Type polymorphism**: Use `if type == 'kit'` / `elif type == 'item'` pattern in order/delivery views
3. **Formsets**: Use `inlineformset_factory()` for one-to-many relationships (like KitItem in Kit)
4. **Custom managers**: Attach properties like `_quantity_ordered` in manager methods to avoid N+1 queries
5. **Redirect after POST**: Always redirect to a list view after successful form submission (form.save() → redirect)

## Known Issues / TODO

From README.md:
- [ ] Update item grid to show which kit(s) each item is part of
- [ ] Implement deliveries (partially done)
- [ ] Update dashboard with something useful
- [ ] Fix kit item deletion so delete happens at item level (custom delete logic in formset)

## Render Deployment

The app is deployed on Render.com. Key settings:
- Uses `RENDER_EXTERNAL_HOSTNAME` environment variable to configure allowed hosts
- Static files served via WhiteNoise with compression
- PostgreSQL database via `dj_database_url`
- Build command runs `build.sh`
