from django.db import models
from django.contrib.auth.models import User

# ------------------------
# POLICY (Base, basada en la estructura original)
# ------------------------
class Policy(models.Model):
    POLICY_TYPES = [
        ('vehicle', 'Vehicle Insurance'),
        ('property', 'Property Insurance'),
    ]

    name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50, unique=True)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES, default='vehicle')
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.policy_number} - {self.name}"

class UserPolicy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_policies')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='policy_users')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'policy')

    def __str__(self):
        return f"{self.user.username} - {self.policy.policy_number}"


# -------------------------------------------------------------------------------------------------
# NUEVOS MODELOS DE RECLAMACIÓN (Simplificados)
# -------------------------------------------------------------------------------------------------

class ClaimPaymentDetails(models.Model):
    """5. Información para el Pago de la Reclamación."""
    PAYMENT_CHOICES = [
        ('check', 'Cheque'),
        ('transfer', 'Transferencia Electrónica'),
    ]
    ACCOUNT_TYPES = [
        ('savings', 'Ahorros'),
        ('checking', 'Corriente'),
    ]

    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, verbose_name="Medio de Pago", default='check')
    bank_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Entidad Financiera")
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, blank=True, null=True, verbose_name="Tipo de Cuenta")
    account_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Cuenta")

    def __str__(self):
        return f"Pago: {self.get_payment_method_display()}"


class UserSolicitation(models.Model):
    """Formulario de Reclamación Principal (MetLife)."""
    STATUS_CHOICES = [
        ('Pending', 'Pendiente'), ('Approved', 'Aprobado'), ('Rejected', 'Rechazado'), ('Draft', 'Borrador'),
    ]
    # 1. Lugar y Fecha de Diligenciamiento
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitations') # Reclamante
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='solicitations', null=True) # Poliza asociada
    diligenciamiento_city = models.CharField(max_length=50, verbose_name="Ciudad de Diligenciamiento", blank=True, default='-')
    document_link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Enlace a Documentos (Drive, etc.)")

    # 3. Información del Reclamante (CAMPOS CORREGIDOS)
    claimant_cc = models.CharField(max_length=20, verbose_name="C.C.", blank=True, default='-')
    claimant_address = models.CharField(max_length=255, verbose_name="Dirección de Correspondencia", blank=True, default='-')
    claimant_phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, default='-')
    claimant_email = models.EmailField(verbose_name="Email", blank=True, default='ejemplo@metlife.com')
    claimant_celular = models.CharField(max_length=20, verbose_name="Celular", blank=True, default='-')
    
    # 5. Pago
    payment_details = models.OneToOneField(
        ClaimPaymentDetails, on_delete=models.SET_NULL, null=True, blank=True
    )

    # 7. Información sobre el Siniestro (CAMPOS CORREGIDOS)
    incident_location = models.CharField(max_length=255, verbose_name="Lugar del Siniestro", blank=True, default='-')
    incident_date = models.DateField(verbose_name="Fecha del Siniestro")
    incident_time = models.TimeField(verbose_name="Hora del Siniestro")
    incident_cause = models.TextField(verbose_name="Causa del Siniestro", blank=True, default='-')
    incident_description = models.TextField(verbose_name="Descripción del Siniestro", blank=True, default='-')
    occupation_at_incident = models.CharField(max_length=100, verbose_name="Ocupación a la fecha del Siniestro", blank=True, default='-')
    last_work_date = models.DateField(null=True, blank=True, verbose_name="Último día de trabajo")
    has_recent_hospitalization = models.BooleanField(default=False, verbose_name="Estuvo hospitalizado/tratamiento en los últimos años")

    # 7. Campos condicionales adicionales
    disability_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Estructuración (Incapacidad T.P.)")
    is_drunk_accident = models.BooleanField(null=True, blank=True, verbose_name="Estaba en estado de embriaguez (Accidente)")
    accident_injuries = models.TextField(blank=True, verbose_name="Descripción de las lesiones (Accidente)")
    accident_details = models.TextField(blank=True, verbose_name="Detalle del Accidente")
    medical_reimbursement_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Valor de Reembolso")
    hospitalization_days = models.IntegerField(null=True, blank=True, verbose_name="Días de Hospitalización (Renta Diaria)")
    hospital_entry_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Ingreso (Renta Diaria)")
    hospital_exit_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Salida (Renta Diaria)")
    temp_disability_start = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio (Incapacidad Temporal)")
    temp_disability_end = models.DateField(null=True, blank=True, verbose_name="Fecha de Finalización (Incapacidad Temporal)")

    # 9. Declaración y Autorización
    declaration_accepted = models.BooleanField(default=False)
    claimant_signature = models.CharField(max_length=150, verbose_name="Firma del Reclamante", blank=True, default='-')

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft') # Cambiado el default a 'Draft'

    def __str__(self):
        return f"Reclamación {self.pk} de {self.user.username}"
