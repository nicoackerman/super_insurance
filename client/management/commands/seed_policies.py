from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from client.models import Policy, UserPolicy, UserSolicitation

class Command(BaseCommand):
    help = 'Seeds the database with initial policies and user associations.'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing solicitations, policies and users...')
        UserSolicitation.objects.all().delete() # Delete existing solicitations
        UserPolicy.objects.all().delete()
        Policy.objects.all().delete()
        User.objects.filter(username='roro').delete()

        self.stdout.write('Creating new policies...')
        policy1 = Policy.objects.create(
            name='Seguro de Vehículo Básico',
            policy_number='VEH-001',
            policy_type='vehicle',
            coverage_amount=50000.00
        )
        policy2 = Policy.objects.create(
            name='Seguro de Propiedad Hogar',
            policy_number='PROP-001',
            policy_type='property',
            coverage_amount=250000.00
        )
        policy3 = Policy.objects.create(
            name='Seguro de Vehículo Premium',
            policy_number='VEH-002',
            policy_type='vehicle',
            coverage_amount=100000.00
        )
        policy4 = Policy.objects.create(
            name='Seguro de Propiedad Comercial',
            policy_number='PROP-002',
            policy_type='property',
            coverage_amount=500000.00
        )

        self.stdout.write('Creating user "roro"...')
        roro, created = User.objects.get_or_create(
            username='roro',
            defaults={'first_name': 'Rodrigo', 'last_name': 'Rosales', 'email': 'roro@example.com'}
        )
        if created:
            roro.set_password('password123')
            roro.save()
            self.stdout.write(self.style.SUCCESS('User "roro" created.'))
        else:
            self.stdout.write(self.style.WARNING('User "roro" already exists.'))

        self.stdout.write('Associating policies with "roro"...')
        UserPolicy.objects.create(user=roro, policy=policy1) # Associate VEH-001
        UserPolicy.objects.create(user=roro, policy=policy2) # Associate PROP-001

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))