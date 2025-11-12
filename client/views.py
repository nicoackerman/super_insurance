from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from .forms import UserSolicitationForm
from .models import (
    UserSolicitation, Policy, UserPolicy, ClaimPaymentDetails, 
)

# Constantes de soporte
COLOMBIAN_CITIES = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Barrancabermeja", "Otro"]
COLOMBIAN_BANKS = ["Banco de Bogotá", "Bancolombia", "Davivienda", "BBVA Colombia", "Otro"]

@login_required
def home(request):
    total_solicitations = UserSolicitation.objects.filter(user=request.user).count()
    return render(request, 'client/home.html', {'total_solicitations': total_solicitations})

@login_required
@transaction.atomic
def create_claim_solicitation(request: HttpRequest) -> HttpResponse:
    user = request.user

    if request.method == 'POST':
        form = UserSolicitationForm(request.POST, user=user, colombian_cities=COLOMBIAN_CITIES)
        if form.is_valid():
            form_data = request.POST
            is_draft = 'save_draft' in form_data
            
            # Related models logic for ClaimPaymentDetails
            payment_details = None
            if form_data.get('payment_method') == 'transfer':
                payment_details = ClaimPaymentDetails.objects.create(
                    payment_method='transfer',
                    bank_name=form_data.get('bank_name'),
                    account_type=form_data.get('account_type'),
                    account_number=form_data.get('account_number')
                )
            elif form_data.get('payment_method') == 'check':
                payment_details = ClaimPaymentDetails.objects.create(payment_method='check')

            solicitation = form.save(commit=False)
            solicitation.user = user
            solicitation.payment_details = payment_details
            solicitation.status = 'Draft' if is_draft else 'Pending'
            solicitation.save()
            
            if is_draft:
                return redirect('client:solicitations')
            else:
                return redirect('client:claim_success', pk=solicitation.pk)
        else:
            context = {
                'form': form,
                'COLOMBIAN_CITIES': COLOMBIAN_CITIES,
                'COLOMBIAN_BANKS': COLOMBIAN_BANKS,
            }
            return render(request, 'client/claim_form.html', context)

    else:
        form = UserSolicitationForm(user=user, colombian_cities=COLOMBIAN_CITIES)

    context = {
        'form': form,
        'COLOMBIAN_CITIES': COLOMBIAN_CITIES,
        'COLOMBIAN_BANKS': COLOMBIAN_BANKS,
    }
    return render(request, 'client/claim_form.html', context)

@login_required
def solicitations(request):
    status = request.GET.get('status')
    
    solicitations_list = UserSolicitation.objects.filter(user=request.user).order_by('-created_at')

    if status:
        solicitations_list = solicitations_list.filter(status=status)

    paginator = Paginator(solicitations_list, 10)
    page = request.GET.get('page')

    try:
        solicitations = paginator.page(page)
    except PageNotAnInteger:
        solicitations = paginator.page(1)
    except EmptyPage:
        solicitations = paginator.page(paginator.num_pages)
    
    status_choices = UserSolicitation.STATUS_CHOICES
    
    return render(request, 'client/solicitations.html', {
        'solicitations': solicitations,
        'status_choices': status_choices,
        'status': status,
    })

@login_required
def solicitation_details(request, pk):
    solicitation = UserSolicitation.objects.get(pk=pk, user=request.user)
    return render(request, 'client/solicitation_details.html', {'solicitation': solicitation})