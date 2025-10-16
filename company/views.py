from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from client.models import UserSolicitation, UserPolicy
from .forms import UserPolicyForm
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def home(request):
    return render(request, 'company/home.html')

@login_required
@user_passes_test(is_admin)
def solicitations(request):
    solicitations = UserSolicitation.objects.all()
    return render(request, 'company/solicitations.html', {'solicitations': solicitations})

@login_required
@user_passes_test(is_admin)
def create_user_with_policy(request):
    if request.method == 'POST':
        form = UserPolicyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            policy = form.cleaned_data['policy']

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Assign the policy to the user
            UserPolicy.objects.create(user_id=user.id, policy_id=policy.id)

            return redirect('company:home')
    else:
        form = UserPolicyForm()
    return render(request, 'company/create_user_with_policy.html', {'form': form})