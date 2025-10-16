from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserSolicitationForm

def is_not_admin(user):
    return not user.is_superuser

# Create your views here.
@login_required(login_url="/users/login/")
@user_passes_test(is_not_admin)
def home(request):
    return render(request, 'client/home.html')

@login_required(login_url="/users/login/")
@user_passes_test(is_not_admin)
def create_solicitation(request):
    if request.method == 'POST':
        form = UserSolicitationForm(request.POST)
        if form.is_valid():
            solicitation = form.save(commit=False)
            solicitation.user_id = request.user 
            solicitation.save()
            return render(request, 'client/solicitation_success.html')
        else: 
            return render(request, 'client/solicitation_error.html', {'form': form})
    else:
        form = UserSolicitationForm()
    
    return render(request, 'client/create_solicitation.html', {'form': form})
