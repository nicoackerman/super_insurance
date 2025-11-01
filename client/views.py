from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserSolicitationForm

from .models import UserSolicitation

def is_not_admin(user):
    return not user.is_superuser

# Create your views here.
@login_required(login_url="/users/login/")
@user_passes_test(is_not_admin)
def home(request):
    total_solicitations = UserSolicitation.objects.filter(user_id=request.user).count()
    return render(request, 'client/home.html', {'total_solicitations': total_solicitations})

@login_required(login_url="/users/login/")
@user_passes_test(is_not_admin)
def create_solicitation(request):
    if request.method == 'POST':
        form = UserSolicitationForm(request.POST, user=request.user)
        if form.is_valid():
            solicitation = form.save(commit=False)
            solicitation.user_id = request.user 
            solicitation.save()
            return render(request, 'client/solicitation_success.html')
        else: 
            return render(request, 'client/solicitation_error.html', {'form': form})
    else:
        form = UserSolicitationForm(user=request.user)
    
    return render(request, 'client/create_solicitation.html', {'form': form})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@login_required(login_url="/users/login/")
@user_passes_test(is_not_admin)
def solicitations(request):
    status = request.GET.get('status')
    query = request.GET.get('q')
    
    solicitations_list = UserSolicitation.objects.filter(user_id=request.user).order_by('-created_at')

    if status:
        solicitations_list = solicitations_list.filter(status=status)

    if query:
        solicitations_list = solicitations_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(policy_id__name__icontains=query)
        )

    paginator = Paginator(solicitations_list, 10)  # Show 10 solicitations per page
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
        'query': query,
        'status': status,
    })

@login_required(login_url="/users/login/")
@user_passes_test(is_not_admin)
def solicitation_details(request, solicitation_id):
    solicitation = UserSolicitation.objects.get(id=solicitation_id, user_id=request.user)
    return render(request, 'client/solicitation_details.html', {'solicitation': solicitation})
