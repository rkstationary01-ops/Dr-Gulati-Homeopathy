from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from website.models import Appointment, Treatment
from datetime import date, timedelta

class DashboardAccessTests(TestCase):
    def test_anonymous_user_is_redirected_to_dashboard_login(self):
        response = self.client.get(reverse('clinic_dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/clinic-admin/login/', response.url)

    def test_non_staff_user_is_forbidden(self):
        user = get_user_model().objects.create_user(username='visitor', password='test-pass-123')
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('clinic_dashboard:dashboard')).status_code, 403)

    def test_staff_can_open_dashboard(self):
        user = get_user_model().objects.create_user(username='manager', password='test-pass-123', is_staff=True)
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('clinic_dashboard:dashboard')).status_code, 200)

    def test_public_home_remains_available(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
