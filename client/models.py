from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
class Policy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class UserPolicy(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_policies')
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='policy_users')

    class Meta:
        unique_together = ('user_id', 'policy_id')


class UserSolicitation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Successful', 'Successful'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitations')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='solicitations')
    ocurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    evidence_url = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
