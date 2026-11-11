from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
# from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils import timezone

from django.db.models import Q, Count

from .models import Ticket
from .utils import generate_unique_ticket_code

# Create your views here.
def home(request):
    if request.user.is_authenticated:
            return redirect('dashboard')  # Redirect to the dashboard if already logged in
    return render(request, 'index.html')

def user_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeatPassword', '')

        if not all([email, username, password, repeat_password]):
            return render(request, 'signup.html', {
                'error_message': 'Please fill in all fields.'
            })

        if password != repeat_password:
            return render(request, 'signup.html', {
                'error_message': 'Passwords do not match.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error_message': 'This username is already taken.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {
                'error_message': 'An account with this email already exists.'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Account created. Let the user log in separately.
        return redirect('login')

    return render(request, 'signup.html')

def user_login(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to the dashboard if already logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username, password = password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('staff-dashboard')
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {"error_message":error_message})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def ticket_login(request):
    ticket_code = (
        request.POST.get('ticket_code')
        if request.method == 'POST'
        else request.GET.get('ticket-code', '')
    )
    ticket_code = ticket_code.strip()

    context = {'ticket_code': ticket_code}

    if not ticket_code:
        context['error_message'] = (
            'Please open the registration link provided by your IT team.'
        )
        return render(request, 'ticket_login.html', context)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeatPassword', '')

        if not all([username, email, password, repeat_password]):
            context['error_message'] = 'Please fill in all fields.'
            return render(request, 'ticket_login.html', context)

        if password != repeat_password:
            context['error_message'] = 'Passwords do not match.'
            return render(request, 'ticket_login.html', context)

        if User.objects.filter(username=username).exists():
            context['error_message'] = 'This username is already taken.'
            return render(request, 'ticket_login.html', context)

        if User.objects.filter(email__iexact=email).exists():
            context['error_message'] = (
                'An account with this email already exists.'
            )
            return render(request, 'ticket_login.html', context)

        try:
            validate_password(password)
        except ValidationError as error:
            context['error_message'] = ' '.join(error.messages)
            return render(request, 'ticket_login.html', context)

        try:
            with transaction.atomic():
                ticket = (
                    Ticket.objects.select_for_update()
                    .get(ticket_code=ticket_code)
                )

                if ticket.user_id is not None:
                    context['error_message'] = (
                        'This ticket has already been claimed. '
                        'Please log in through the normal login page.'
                    )
                    return render(
                        request, 'ticket_login.html', context
                    )

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                ticket.user = user
                ticket.save(update_fields=['user'])

        except Ticket.DoesNotExist:
            context['error_message'] = (
                'This ticket code is invalid. Please contact your IT team.'
            )
            return render(request, 'ticket_login.html', context)

        return redirect('login')

    return render(request, 'ticket_login.html', context)

@login_required
def dashboard(request):
    
    tickets = Ticket.objects.filter(user = request.user)

    stats = tickets.aggregate(
        open_count=Count('id', filter=Q(ticket_status='Open')),
        progress_count=Count('id', filter=Q(ticket_status='In Progress')),
        resolved_count=Count('id', filter=Q(ticket_status='Resolved')),
        closed_count=Count('id', filter=Q(ticket_status='Closed')),
    )

    return render(
        request,
        'dashboard.html',
        {
            'stats': stats,
            'tickets':tickets
        }
    )
    
def profile(request, name):
    return render(request, 'profile.html')

@login_required
def create_ticket(request):

    if request.method == 'POST':

        ticket_title = request.POST['ticket_title']
        category = request.POST['category']
        priority = request.POST['priority']
        device_type = request.POST['device_type']
        description = request.POST['description']

        attachment = request.FILES.get('attachment')

        Ticket.objects.create(

            user=request.user,
            
            ticket_code=generate_unique_ticket_code(),

            ticket_title=ticket_title,

            category=category,

            priority=priority,

            device_type=device_type,

            description=description,

            attachment=attachment

        )

        return redirect('tickets')

    return render(
        request,
        'create_ticket.html'
    )

@login_required
def chatbox(request):
    # if request.method == 'POST':
    
    #     # Laptop = request.POST['laptop']
    #     # Printer = request.POST['printer']
    #     # Network = request.POST['network']
    #     # Password = request.POST['password']
    #     if request.POST['laptop'] or request.POST['printer'] or request.POST['network'] or request.POST['password']:
    #         button = request.POST['laptop', 'printer', 'network', 'password']
        
    #     description = request.POST['description']

    #     # attachment = request.FILES.get('attachment')

    #     Artificial_chat.objects.create(

    #         user=request.user,
            
    #         # ticket_code=generate_unique_ticket_code(),

    #         # ticket_title=ticket_title,

    #         # category=category,

    #         # priority=priority,

    #         # device_type=device_type,

    #         user_chat=description,

    #         # attachment=attachment

    #     )

        # return redirect('tickets')
    
    return render(
        request,
        'chatbox.html'
    )

@login_required
def view_tickets(request):
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    # Staff can see all tickets; ordinary users see only their own.
    if request.user.is_staff:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(user=request.user)

    # Apply status filter
    if status:
        tickets = tickets.filter(ticket_status=status)

    # Apply search filter
    if search:
        tickets = tickets.filter(
            Q(ticket_title__icontains=search) |
            Q(ticket_code__icontains=search) |
            Q(description__icontains=search)
        )

    tickets = tickets.order_by('-created_at')

    context = {
        'tickets': tickets,
        'status': status,
        'search': search,
        'is_staff_member': request.user.is_staff,
    }

    return render(request, 'view_tickets.html', context)

@login_required
def ticket_detail(request, ticket_code):

    ticket_detail = get_object_or_404(
        Ticket,
        ticket_code=ticket_code
    )

    # Check whether the logged-in user owns this ticket
    is_ticket_owner = request.user == ticket_detail.user

    # Check whether the logged-in user is authorized IT staff
    is_staff_member = request.user.is_staff

    # Only the owner or IT staff can view the ticket
    if not is_ticket_owner and not is_staff_member:
        return redirect('tickets')

    # Determine which actions the current user can perform
    can_claim = (
        is_staff_member
        and ticket_detail.ticket_status == 'Open'
        and ticket_detail.assigned_to is None
    )

    can_resolve = (
        is_staff_member
        and ticket_detail.assigned_to == request.user
        and ticket_detail.ticket_status == 'In Progress'
    )

    context = {
        'ticket_detail': ticket_detail,
        'is_ticket_owner': is_ticket_owner,
        'is_staff_member': is_staff_member,
        'can_claim': can_claim,
        'can_resolve': can_resolve,
    }

    return render(
        request,
        'ticket_detail.html',
        context
    )


@login_required
@user_passes_test(lambda user: user.is_staff)
def staff_dashboard(request):

    # Retrieve ticket statistics
    total_tickets = Ticket.objects.count()

    open_tickets = Ticket.objects.filter(
        ticket_status='Open'
    ).count()

    in_progress_tickets = Ticket.objects.filter(
        ticket_status='In Progress'
    ).count()

    resolved_tickets = Ticket.objects.filter(
        ticket_status='Resolved'
    ).count()

    # Retrieve the five most recently submitted tickets
    recent_tickets = Ticket.objects.order_by(
        '-created_at'
    )[:5]

    context = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'resolved_tickets': resolved_tickets,
        'recent_tickets': recent_tickets,
    }

    return render(
        request,
        'staff_dashboard.html',
        context
    )

@login_required
def notification(request):
    return render(request, 'notification.html')

@login_required
@require_POST
def claim_ticket(request, ticket_code):

    if not request.user.is_staff:
        return HttpResponseForbidden(
            "You are not authorized to perform this action."
        )

    ticket = get_object_or_404(
        Ticket,
        ticket_code=ticket_code
    )

    # Only unassigned, open tickets can be claimed
    if ticket.ticket_status == 'Open' and ticket.assigned_to is None:

        ticket.assigned_to = request.user
        ticket.ticket_status = 'In Progress'
        ticket.save()

    return redirect('ticket-detail', ticket_code=ticket.ticket_code)

@login_required
@require_POST
def resolve_ticket(request, ticket_code):

    if not request.user.is_staff:
        return HttpResponseForbidden(
            "You are not authorized to perform this action."
        )

    ticket = get_object_or_404(
        Ticket,
        ticket_code=ticket_code
    )

    # Only the assigned staff member can resolve the ticket
    if ticket.assigned_to != request.user:
        return HttpResponseForbidden(
            "You are not assigned to this ticket."
        )

    if ticket.ticket_status != 'In Progress':
        return redirect('ticket-detail', ticket_code=ticket.ticket_code)

    response = request.POST.get('resolution_response', '').strip()

    if not response:
        return redirect('ticket-detail', ticket_code=ticket.ticket_code)

    ticket.resolution_response = response
    ticket.ticket_status = 'Resolved'
    ticket.resolved_at = timezone.now()

    ticket.save()

    return redirect('ticket-detail', ticket_code=ticket.ticket_code)