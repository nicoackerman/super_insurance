from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserSolicitationForm

# Create your views here.
@login_required(login_url="/users/login/")
def home(request):
    return render(request, 'client/home.html')

@login_required(login_url="/users/login/")
def create_solicitation(request):
    if request.method == 'POST':
        form = UserSolicitationForm(request.POST)
        if form.is_valid():
            solicitation = form.save(commit=False)
            solicitation.user_id = request.user 
            solicitation.save()
            return render(request, 'client/solicitation_success')
        else: 
            return render(request, 'client/solicitation_success')
    else:
        form = UserSolicitationForm()
    
    return render(request, 'client/create_solicitation.html', {'form': form})
