from django.core.management.base import BaseCommand
from website.models import Treatment

class Command(BaseCommand):
    help = 'Create starter treatment categories for the clinic website.'

    def handle(self, *args, **options):
        items = [
            ('Chronic Diseases', 'chronic-diseases', 'Discuss long-term health concerns with the doctor.', '✚', 1),
            ('Skin Problems', 'skin-problems', 'Consultation for common skin-related concerns.', '❋', 2),
            ('Respiratory Issues', 'respiratory-issues', 'Discuss breathing and respiratory concerns.', '♧', 3),
            ('Digestive Disorders', 'digestive-disorders', 'Consultation for digestive and gut-related concerns.', '◉', 4),
            ('Hormonal Imbalance', 'hormonal-imbalance', 'Discuss concerns that may need clinical assessment.', '⚕', 5),
            ('Allergies', 'allergies', 'Discuss allergy symptoms and care options.', '❄', 6),
            ('Child Health', 'child-health', 'Consultation for child and adolescent health concerns.', '☻', 7),
            ('General Wellness', 'general-wellness', 'General health discussion and wellness guidance.', '❀', 8),
        ]
        for title, slug, desc, icon, order in items:
            Treatment.objects.update_or_create(slug=slug, defaults={'title': title, 'short_description': desc, 'icon': icon, 'display_order': order, 'is_featured': True})
        self.stdout.write(self.style.SUCCESS('Starter treatment categories are ready.'))
