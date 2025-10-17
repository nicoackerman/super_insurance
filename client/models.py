from django.db import models
from django.contrib.auth.models import User

# ------------------------
# POLICY
# ------------------------
class Policy(models.Model):
    POLICY_TYPES = [
        ('vehicle', 'Vehicle Insurance'),
        ('property', 'Property Insurance'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    policy_number = models.CharField(max_length=50, unique=True)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES, default='vehicle')
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.policy_number} - {self.name}"


# ------------------------
# USER ↔ POLICY RELATIONSHIP
# ------------------------
class UserPolicy(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_policies')
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='policy_users')
    assigned_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    role = models.CharField(
        max_length=50,
        choices=[
            ('holder', 'Policy Holder'),
            ('beneficiary', 'Beneficiary'),
            ('dependent', 'Dependent'),
        ],
        default='holder'
    )

    class Meta:
        unique_together = ('user_id', 'policy_id')

    def __str__(self):
        return f"{self.user_id.username} - {self.policy_id.name}"


# ------------------------
# USER SOLICITATION / CLAIM
# ------------------------
class UserSolicitation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Successful', 'Successful'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitations')
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='solicitations')
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    evidence_url = models.URLField(max_length=255, blank=True)
    estimated_loss = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Approximate value of the claimed damage."
    )
    claim_location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Location where the incident occurred."
    )
    witnesses = models.TextField(
        blank=True,
        help_text="Names or contacts of witnesses, if any."
    )
    police_report_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Police or authority report reference number."
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    internal_notes = models.TextField(blank=True, help_text="Notes from claim evaluators or agents.")

    def __str__(self):
        return f"{self.title} ({self.status})"
