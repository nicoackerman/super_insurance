from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from client.models import Policy, UserPolicy

class Command(BaseCommand):
    help = 'Seeds the database with initial policies and user associations.'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing policies and users...')
        UserPolicy.objects.all().delete()
        Policy.objects.all().delete()
        User.objects.filter(username='roro').delete()

        self.stdout.write('Creating new policies...')
        policy1 = Policy.objects.create(
            name='Seguro de Vida Básico',
            policy_number='LIFE-001',
            policy_type='life',
            coverage_amount=50000.00
        )
        policy2 = Policy.objects.create(
            name='Plan de Salud Completo',
            policy_number='HEALTH-001',
            policy_type='health',
            coverage_amount=25000.00
        )
        policy3 = Policy.objects.create(
            name='Seguro de Accidentes Personales',
            policy_number='ACC-001',
            policy_type='accident',
            coverage_amount=100000.00
        )
        policy4 = Policy.objects.create(
            name='Seguro de Vida Plus',
            policy_number='LIFE-002',
            policy_type='life',
            coverage_amount=150000.00
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
        UserPolicy.objects.create(user=roro, policy=policy1)
        UserPolicy.objects.create(user=roro, policy=policy2)

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
