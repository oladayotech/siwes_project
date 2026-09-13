from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q, Count

from .models import Ticket
from .utils import generate_unique_ticket_code

# Create your views here.
def home(request):
    return render(request, 'index.html')

def user_signup(request):

    if request.method == 'POST':

        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password != repeatPassword:

            error_message = "Passwords do not match."

            return render(
                request,
                'signup.html',
                {'error_message': error_message}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('dashboard')

    return render(request, 'signup.html')

def user_signup(request):

    if request.method == 'POST':

        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password != repeatPassword:

            error_message = "Passwords do not match."

            return render(
                request,
                'signup.html',
                {'error_message': error_message}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('dashboard')

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
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        ticket_code = request.POST['ticket_code']
        password = request.POST['ticket_code']
        
        
    return render(request, 'ticket_login.html')

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
    return render(request, 'chatbox.html')

@login_required
def view_tickets(request):
    search = request.GET.get('search')

    status = request.GET.get('status')

    tickets = Ticket.objects.filter(user=request.user)

    if status:
        # filter tickets by status here
        tickets = tickets.filter(ticket_status = status)
        
    if search:
        # filter tickets by search here
        tickets = tickets.filter(
            Q(ticket_title__icontains=search) |
            Q(ticket_code__icontains=search) |
            Q(description__icontains=search)
        )
    
    return render(
        request,
        'view_tickets.html',
        {
            'tickets': tickets,
            'status': status,
        }
    )

@login_required
def ticket_detail(request, pk):
    ticket_details = Ticket.objects.get(ticket_code=pk)
    if request.user == ticket_details.user:
        return render(request, 'ticket_detail.html', {'ticket_detail':ticket_details})
    return redirect('tickets')

@login_required
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

@login_required
def notification(request):
    return render(request, 'notification.html')