from django.core.management.base import BaseCommand
from client.models import UserSolicitation, Policy
from django.contrib.auth.models import User
from datetime import datetime

class Command(BaseCommand):
    help = 'Creates sample solicitations'

    def handle(self, *args, **options):
        # Get a user and a policy
        user = User.objects.first()
        policy = Policy.objects.first()

        if not user or not policy:
            self.stdout.write(self.style.ERROR('Could not find a user or a policy in the database. Please create them first.'))
            return

        # Create some solicitations
        solicitations = [
            {
                'title': 'Car Accident Claim',
                'description': 'My car was hit from behind.',
                'occurred_at': datetime(2025, 10, 20, 10, 0, 0),
                'status': 'Pending',
            },
            {
                'title': 'Water Damage in Kitchen',
                'description': 'A pipe burst and flooded my kitchen.',
                'occurred_at': datetime(2025, 10, 25, 15, 30, 0),
                'status': 'Under Review',
            },
        ]

        for sol_data in solicitations:
            UserSolicitation.objects.create(
                user_id=user,
                policy_id=policy,
                title=sol_data['title'],
                description=sol_data['description'],
                occurred_at=sol_data['occurred_at'],
                status=sol_data['status'],
            )

        self.stdout.write(self.style.SUCCESS('Successfully created sample solicitations.'))