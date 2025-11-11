from django import forms
from .models import UserSolicitation, Policy
from datetime import datetime

class UserSolicitationForm(forms.ModelForm):
    policy = forms.ModelChoiceField(
        queryset=Policy.objects.none(),
        label="Póliza a reclamar",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    diligenciamiento_city = forms.ChoiceField(
        label="Ciudad de Diligenciamiento",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = UserSolicitation
        fields = [
            'policy',
            'diligenciamiento_city',
            'claimant_cc',
            'claimant_address',
            'claimant_phone',
            'claimant_email',
            'claimant_celular',
            'incident_location',
            'incident_date',
            'incident_time',
            'incident_cause',
            'incident_description',
            'occupation_at_incident',
            'last_work_date',
            'has_recent_hospitalization',
            'disability_date',
            'is_drunk_accident',
            'accident_injuries',
            'accident_details',
            'medical_reimbursement_value',
            'hospitalization_days',
            'hospital_entry_date',
            'hospital_exit_date',
            'temp_disability_start',
            'temp_disability_end',
            'document_link',
            'declaration_accepted',
            'claimant_signature',
        ]
        widgets = {
            'incident_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'incident_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'last_work_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disability_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hospital_entry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hospital_exit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'temp_disability_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'temp_disability_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'declaration_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        colombian_cities = kwargs.pop('colombian_cities', [])
        super().__init__(*args, **kwargs)
        if user:
            self.fields['policy'].queryset = Policy.objects.filter(policy_users__user=user)
        
        self.fields['diligenciamiento_city'].choices = [(city, city) for city in colombian_cities]
        self.fields['diligenciamiento_city'].choices.insert(0, ('', 'Seleccione ciudad')) # Add a default option
        
        for field_name, field in self.fields.items():
            if field_name not in ['policy', 'diligenciamiento_city', 'declaration_accepted']:
                field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        today = datetime.now().date()

        date_fields = [
            'incident_date', 'last_work_date', 'disability_date',
            'hospital_entry_date', 'hospital_exit_date',
            'temp_disability_start', 'temp_disability_end'
        ]

        for field_name in date_fields:
            date_value = cleaned_data.get(field_name)
            if date_value and date_value > today:
                self.add_error(field_name, "La fecha no puede ser en el futuro.")
        
        return cleaned_data



