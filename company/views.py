from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from client.models import UserSolicitation, UserPolicy, Policy
from django.contrib import messages

from .forms import UserPolicyForm, PolicyForm, AddPolicyToUserForm, UserPolicyDatesForm, SolicitationStatusForm
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def change_solicitation_status(request, solicitation_id):
    solicitation = get_object_or_404(UserSolicitation, id=solicitation_id)

    if solicitation.status == 'Approved' or solicitation.status == 'Rejected':
        messages.error(request, "Cannot change status of an approved or rejected solicitation.")
        return redirect('company:solicitations')

    if request.method == 'POST':
        form = SolicitationStatusForm(request.POST, instance=solicitation)
        if form.is_valid():
            form.save()
            messages.success(request, f"Solicitation {solicitation.pk} status changed to {solicitation.get_status_display()}.")
            return redirect('company:solicitations')
        else:
            messages.error(request, "Invalid status provided.")
    else:
        initial_status = request.GET.get('status')
        if initial_status and initial_status in [s[0] for s in UserSolicitation.STATUS_CHOICES]:
            form = SolicitationStatusForm(instance=solicitation, initial={'status': initial_status})
        else:
            form = SolicitationStatusForm(instance=solicitation)
    
    return render(request, 'company/change_solicitation_status.html', {'solicitation': solicitation, 'form': form})

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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count

@login_required
@user_passes_test(is_admin)
def solicitations(request):
    status = request.GET.get('status')
    query = request.GET.get('q')
    
    solicitations_list = UserSolicitation.objects.select_related('user', 'policy').all().order_by('-created_at')

    if status:
        solicitations_list = solicitations_list.filter(status=status)

    if query:
        solicitations_list = solicitations_list.filter(
            Q(user__username__icontains=query) |
            Q(incident_cause__icontains=query) |
            Q(incident_description__icontains=query) |
            Q(policy__policy_number__icontains=query)
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

    # Calculate solicitation counts by status
    solicitation_counts = {}
    for status_code, status_name in status_choices:
        solicitation_counts[status_code] = UserSolicitation.objects.filter(status=status_code).count()
    
    return render(request, 'company/solicitations.html', {
        'solicitations': solicitations,
        'status_choices': status_choices,
        'query': query,
        'status': status,
        'solicitation_counts': solicitation_counts,
    })

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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.filter(is_superuser=False).annotate(
        policy_count=Count('user_policies', distinct=True),
        solicitation_count=Count('solicitations', distinct=True)
    )
    user_policies = UserPolicy.objects.select_related('policy', 'user').filter(user__in=users)

    users_with_policies = {}
    for user in users:
        users_with_policies[user] = {
            'policies': [],
            'policy_count': user.policy_count,
            'solicitation_count': user.solicitation_count,
        }

    for up in user_policies:
        users_with_policies[up.user]['policies'].append(up)

    # Pagination for users
    paginator = Paginator(list(users_with_policies.keys()), 10) # Paginate users, not policies
    page = request.GET.get('page')

    try:
        paginated_users = paginator.page(page)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)

    # Search functionality
    query = request.GET.get('q')
    if query:
        paginated_users_list = []
        for user_obj in paginated_users:
            if query.lower() in user_obj.username.lower() or query.lower() in user_obj.email.lower():
                paginated_users_list.append(user_obj)
        paginated_users = Paginator(paginated_users_list, 10).page(1) # Re-paginate search results

    return render(request, 'company/user_list.html', {
        'users_with_policies': users_with_policies,
        'paginated_users': paginated_users,
        'query': query,
    })

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
    if request.method == 'POST':
        form = UserPolicyDatesForm(request.POST, instance=user_policy)
        if form.is_valid():
            form.save()
            return redirect('company:user_list')
    else:
        form = UserPolicyDatesForm(instance=user_policy)
    return render(request, 'company/edit_user_policy.html', {'user_policy': user_policy, 'form': form})

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


@login_required
@user_passes_test(is_admin)
def user_solicitations(request, user_id):
    user = get_object_or_404(User, id=user_id)
    solicitations = UserSolicitation.objects.filter(user=user).order_by('-created_at')
    return render(request, 'company/user_solicitations.html', {'user': user, 'solicitations': solicitations})




