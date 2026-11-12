# Dr. Aashish Gulati — Homeopathy Clinic (Django)

A multi-page Django clinic website starter with an online appointment request workflow, available-slot lookup, booking reference, appointment status lookup, contact form, and Django Admin management.

## Pages
- `/` — Home
- `/about/` — About the doctor
- `/treatments/` — Treatment directory
- `/treatments/<slug>/` — Treatment details
- `/appointments/book/` — Appointment booking
- `/appointments/success/<uuid>/` — Booking request confirmation
- `/appointments/check/` — Check appointment status
- `/testimonials/` — Published patient testimonials
- `/contact/` — Contact form
- `/privacy-policy/` — Privacy policy starter
- `/admin/` — Admin dashboard

## Windows installation

Install Python 3.11 or later. In PowerShell, open this project folder and run:

```powershell
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
py manage.py makemigrations website
py manage.py migrate
py manage.py seed_demo_data
py manage.py createsuperuser
py manage.py runserver
```

Open `http://127.0.0.1:8000/`. Admin is at `http://127.0.0.1:8000/admin/`.

## Add clinic content

1. Log in to Django Admin.
2. Add Treatment records (e.g. Chronic Diseases, Skin Problems, Respiratory Issues, Digestive Disorders, Hormonal Imbalance, Allergies, Child Health, General Wellness).
3. Add approved patient testimonials. Use only genuine testimonials with patient permission.
4. Manage incoming appointments and change their status from Pending confirmation to Confirmed, Cancelled, or Completed.
5. Add the clinic's verified address, actual opening hours, doctor qualifications and profile photo before publishing.

## Appointment workflow

- Clinic time zone is set to `Asia/Kolkata`.
- The booking form requests patient name, phone, optional email, treatment, date, time and optional reason.
- Available slots are loaded from the server for the selected date. The example clinic schedule is 09:00–17:30 in 30-minute intervals; Sunday is closed.
- The database enforces one active appointment per date/time slot. Cancelled appointments release the slot.
- New bookings are saved as **Pending confirmation**. Patients are told that the clinic must confirm the request.
- The patient can look up a booking using the booking reference and the same phone number.

## Important before production

This is a local development starter, not a production deployment. Before going live:
- Replace `SECRET_KEY`, set `DEBUG = False`, configure `ALLOWED_HOSTS`, HTTPS, secure cookies and production static/media hosting.
- Use PostgreSQL (or another production database), configure automated backups and add rate limiting / spam protection to public forms.
- Set the real clinic address, hours, contact details, doctor qualifications and actual clinic imagery.
- Configure email/SMS/WhatsApp notifications if required. This starter does not send automatic messages.
- Review privacy, consent, data retention and applicable healthcare/legal requirements with the clinic. Do not make unsupported medical claims or promise outcomes.
- Configure clinic-specific working days, holidays, slot durations and consultation lengths before launch.


## Custom clinic staff dashboard (integrated)

The project includes a separate custom staff dashboard at `/clinic-admin/`. It uses the existing `website` app models and database tables; it does not create parallel appointment, treatment, testimonial or enquiry records. The original public website routes and the built-in Django admin at `/admin/` are retained.

### Dashboard access and setup

1. Create an administrator/staff account if you do not already have one: `python manage.py createsuperuser`.
2. Start the server: `python manage.py runserver`.
3. Open `http://127.0.0.1:8000/clinic-admin/` and sign in with that account.
4. Only active users with `is_staff=True` can access dashboard pages. Ordinary registered users receive HTTP 403.
5. The existing Django admin remains at `http://127.0.0.1:8000/admin/`.

### Custom dashboard features

- Live appointment totals and status counts, recent appointments, last-seven-days chart.
- Search/filter appointments and update patient/booking details and status.
- Patient directory derived from appointment records (no duplicate patient table).
- Create, edit and delete treatment categories; public treatment pages use the same records.
- Create, edit, publish/unpublish and delete testimonials; public testimonial pages use the same records.
- View/search contact enquiries and mark them as read.
- Separate templates, CSS and JavaScript under `templates/clinic_dashboard/` and `static/dashboard/`.

### Safety and isolation

- Custom dashboard routes are namespaced under `clinic_dashboard` and mounted only at `/clinic-admin/`.
- Public website URL patterns, views, forms and models are not replaced.
- Dashboard mutations are POST-only where destructive, use CSRF tokens, and are staff-protected.
- Appointment status changes update the existing `Appointment` row; the database's existing active-slot uniqueness constraint remains in force.
- Do not make staff accounts available for public self-registration. Use strong passwords and keep staff credentials private.

Run the checks after installation:

```powershell
python manage.py check
python manage.py test clinic_dashboard website
```

Before production, configure HTTPS, secure cookies, `DEBUG=False`, `ALLOWED_HOSTS`, a production database, backups and monitoring as described above.
