from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from client.models import UserSolicitation, UserPolicy, Policy

from .forms import UserPolicyForm, PolicyForm, AddPolicyToUserForm, UserPolicyDatesForm
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def edit_policy(request, policy_id):
    policy = Policy.objects.get(id=policy_id)
    if request.method == 'POST':
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            return redirect('company:policies')
    else:
        form = PolicyForm(instance=policy)
    return render(request, 'company/edit_policy.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_policy(request, policy_id):
    policy = Policy.objects.get(id=policy_id)
    if request.method == 'POST':
        policy.delete()
        return redirect('company:policies')
    return render(request, 'company/delete_policy.html', {'policy': policy})

@login_required
@user_passes_test(is_admin)
def home(request):
    return render(request, 'company/home.html')

@login_required
@user_passes_test(is_admin)
def solicitations(request):
    solicitations = UserSolicitation.objects.all()
    return render(request, 'company/solicitations.html', {'solicitations': solicitations})

from django.contrib import messages

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
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'A user with this username already exists.')
                return render(request, 'company/create_user_with_policy.html', {'form': form})

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Assign the policy to the user
            UserPolicy.objects.create(user_id=user, policy_id=policy, start_date=start_date, end_date=end_date)

            return redirect('company:home')
    else:
        form = UserPolicyForm()
    return render(request, 'company/create_user_with_policy.html', {'form': form})

@login_required

@user_passes_test(is_admin)

def create_policy(request):

    if request.method == 'POST':

        form = PolicyForm(request.POST)

        if form.is_valid():

            form.save()

            return render(request, 'company/policy_creation_success.html')

        else:

            return render(request, 'company/policy_creation_error.html', {'form': form})

    else:

        form = PolicyForm()

    return render(request, 'company/create_policy.html', {'form': form})



@login_required



@user_passes_test(is_admin)



def policies(request):



    policy_type = request.GET.get('policy_type')



    if policy_type:



        policies = Policy.objects.filter(policy_type=policy_type)



    else:



        policies = Policy.objects.all()



    return render(request, 'company/policies.html', {'policies': policies})

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.filter(is_superuser=False)
    user_policies = UserPolicy.objects.select_related('policy_id', 'user_id').filter(user_id__in=users)

    users_with_policies = {}
    for user in users:
        users_with_policies[user] = []

    for up in user_policies:
        users_with_policies[up.user_id].append(up)

    return render(request, 'company/user_list.html', {'users_with_policies': users_with_policies})

@login_required
@user_passes_test(is_admin)
def add_policy_to_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = AddPolicyToUserForm(request.POST, user=user) # Pass user to the form
        if form.is_valid():
            policy = form.cleaned_data['policy']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if not UserPolicy.objects.filter(user_id=user, policy_id=policy).exists():
                UserPolicy.objects.create(user_id=user, policy_id=policy, start_date=start_date, end_date=end_date)
            return redirect('company:user_list')
    else:
        form = AddPolicyToUserForm(user=user) # Pass user to the form
    return render(request, 'company/add_policy_to_user.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_admin)
def edit_user_policy(request, user_policy_id):
    user_policy = UserPolicy.objects.get(id=user_policy_id)
    policy = user_policy.policy_id # Get the related Policy object

    if request.method == 'POST':
        form = UserPolicyDatesForm(request.POST, instance=user_policy)
        if form.is_valid():
            form.save()
            # Handle form submission to update policy details
            # For now, let's just toggle is_active
            policy.is_active = not policy.is_active
            policy.save()
            return redirect('company:user_list')
    else:
        form = UserPolicyDatesForm(instance=user_policy)
        # Render a form to edit the policy
        # For simplicity, we'll just display current status and a toggle button
    return render(request, 'company/edit_user_policy.html', {'user_policy': user_policy, 'policy': policy, 'form': form})

@login_required
@user_passes_test(is_admin)
def policy_details(request, policy_id):
    policy = Policy.objects.get(id=policy_id)
    return render(request, 'company/policy_details.html', {'policy': policy})

@login_required
@user_passes_test(is_admin)
def solicitation_details(request, solicitation_id):
    solicitation = UserSolicitation.objects.get(id=solicitation_id)
    return render(request, 'company/solicitation_details.html', {'solicitation': solicitation})




