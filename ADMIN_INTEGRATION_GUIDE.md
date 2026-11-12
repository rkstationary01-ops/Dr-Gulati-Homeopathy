# Custom Admin Dashboard — Integration and Operating Manual

This guide is for the integrated `homeopathy_clinic` Django project. The custom staff dashboard is a separate Django app named `clinic_dashboard`. It uses the existing models from `website` and does not replace the public website or Django's built-in admin.

## A. Before you start

1. Make a backup of your current project folder and `db.sqlite3` (if it exists).
2. Extract `homeopathy_clinic_with_custom_admin.zip`.
3. Open the extracted `homeopathy_clinic` folder in VS Code. The folder containing `manage.py` is the project root.
4. Use Python 3.11 or later.

## B. Install and initialize

Open the VS Code terminal in the folder containing `manage.py` and run these commands in PowerShell:

```powershell
py -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations website
python manage.py migrate
python manage.py seed_demo_data
python manage.py createsuperuser
python manage.py check
python manage.py test clinic_dashboard website
python manage.py runserver
```

If you already have a database with existing website data, back it up first. Do not delete `db.sqlite3` or run `flush`. Run migrations against that same database so the existing appointments, treatments, testimonials and enquiries are retained. The `seed_demo_data` command may add sample content; skip it if you do not want demo records.

## C. Open the interfaces

- Public website: `http://127.0.0.1:8000/`
- Custom staff dashboard: `http://127.0.0.1:8000/clinic-admin/`
- Custom staff login: `http://127.0.0.1:8000/clinic-admin/login/`
- Original Django admin: `http://127.0.0.1:8000/admin/`

Sign in to the custom dashboard using the superuser credentials created above. A user must be active and have `is_staff=True`. Do not give staff credentials to patients or enable public staff registration.

## D. What the dashboard manages

| Dashboard section | Data source | Available actions |
|---|---|---|
| Overview | Appointment, Treatment, ContactMessage | Live totals, status counts, weekly chart, recent activity |
| Appointments | Existing `website.Appointment` | Search, filter, edit patient details, change status |
| Patients | Derived from Appointment rows | Search patient name, phone, email and booking count |
| Treatments | Existing `website.Treatment` | Add, edit, delete and feature treatment pages |
| Testimonials | Existing `website.Testimonial` | Add, edit, publish/unpublish and delete |
| Enquiries | Existing `website.ContactMessage` | Search, read message, mark as read |

The patient directory is intentionally derived from appointment data. This avoids introducing a second patient database that could drift out of sync.

## E. Appointment workflow

1. A patient submits the existing public booking form at `/appointments/book/`.
2. The website stores the booking in the existing `Appointment` table with `pending` status.
3. Staff opens `/clinic-admin/appointments/` and searches or filters the booking.
4. Staff opens **Manage**, checks the details and changes the status to Confirmed, Cancelled or Completed.
5. The change is saved to the same database row used by the public booking/check-appointment pages.
6. Cancelled bookings release the slot under the existing database constraint. Active bookings cannot share the same date/time slot.

The dashboard does not send email, SMS or WhatsApp notifications. Configure a notification provider separately if the clinic requires automatic messages.

## F. How the separation protects the public site

- `website` app models, views, forms, templates and public URL names are retained.
- Custom admin URLs are namespaced as `clinic_dashboard:*` and mounted at `/clinic-admin/`.
- Existing `/admin/` continues to use Django's standard admin.
- Dashboard templates live in `templates/clinic_dashboard/`.
- Dashboard CSS and JavaScript live in `static/dashboard/`; public `static/css/style.css` is not replaced.
- Dashboard actions use staff-only access checks, CSRF-protected forms and POST requests for deletion/logout/read-state changes.
- Appointment edits validate slot conflicts and still rely on the database uniqueness constraint for race-condition protection.

## G. If you are integrating into your own existing copy instead of using this ZIP

Prefer using the complete integrated ZIP. If merging manually, copy the `clinic_dashboard/` app folder, `templates/clinic_dashboard/`, and `static/dashboard/` into the project. Then add `'clinic_dashboard'` to `INSTALLED_APPS`, add `'clinic_dashboard.context_processors.clinic_dashboard_context'` to the template context processors, and add `path('clinic-admin/', include('clinic_dashboard.urls'))` to the root URL configuration. Keep `path('', include('website.urls'))` and `path('admin/', admin.site.urls)` in place. Do not replace the existing `website` models or public views.

## H. Troubleshooting

- **No module named django:** activate the virtual environment and run `pip install -r requirements.txt`.
- **Login works but dashboard says access denied:** confirm the account is active and `is_staff=True`; a superuser created with `createsuperuser` has staff access by default.
- **Dashboard CSS is missing:** confirm `STATIC_URL`, `STATICFILES_DIRS`, and that `static/dashboard/css/admin.css` exists; restart `runserver` and hard-refresh the browser.
- **A time slot cannot be saved:** another active appointment may already own that date/time. Choose another slot or cancel the conflicting booking first.
- **Existing content disappeared:** stop immediately and restore the pre-change database backup. Do not delete the database or run `flush`.

## I. Production checklist

Before deployment, set `DEBUG=False`, use a strong environment-based `SECRET_KEY`, configure `ALLOWED_HOSTS`, HTTPS and secure cookies, use PostgreSQL or another production database, configure backups, and test staff permissions. Review patient-data privacy, retention and consent requirements. The included local-development settings are not production-ready.
