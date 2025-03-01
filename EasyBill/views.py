from django.contrib import messages
from .models import Client, Invoice
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, ClientForm, InvoiceForm, InvoiceItemForm



def Home(requests):
    # Renders the homepage
    return render(requests, 'easybill.html')

##################################### User Section ####################################################

def login_page(request):
    # Handles user login
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")

def register_page(request):
    # Handles user registration
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def dashboard(request):
    # Renders the dashboard page with real data
    total_invoices = Invoice.objects.count()
    pending_invoices = Invoice.objects.filter(status='pending').count()
    total_revenue = sum(invoice.total for invoice in Invoice.objects.filter(status='paid'))
    recent_invoices = Invoice.objects.all().order_by('-invoice_date')[:10]
    total_clients = Client.objects.count()
    
    context = {
        'total_invoices': total_invoices,
        'pending_invoices': pending_invoices,
        'total_revenue': total_revenue,
        'recent_invoices': recent_invoices,
        'total_clients': total_clients
    }
    return render(request, "dashboard.html", context)

def overview(request):
    from django.db.models import Count, Sum
    from django.db.models.functions import TruncMonth
    import json
    from datetime import datetime, timedelta

    # Basic stats
    total_clients = Client.objects.count()
    total_invoices = Invoice.objects.count()
    pending_payments = Invoice.objects.filter(status='pending').count()
    total_revenue = Invoice.objects.filter(status='paid').aggregate(Sum('total'))['total__sum'] or 0

    # Monthly revenue data (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_revenue = Invoice.objects.filter(
        status='paid',
        invoice_date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('invoice_date')
    ).values('month').annotate(
        total=Sum('total')
    ).order_by('month')

    revenue_data = {
        'labels': [entry['month'].strftime('%B %Y') for entry in monthly_revenue],
        'values': [float(entry['total']) for entry in monthly_revenue]
    }

    # Invoice status distribution
    status_distribution = Invoice.objects.values('status').annotate(
        count=Count('id')
    )
    status_data = {
        'labels': [entry['status'] for entry in status_distribution],
        'values': [entry['count'] for entry in status_distribution]
    }

    # Client growth by month
    client_growth = Client.objects.filter(
        creation_date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('creation_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    growth_data = {
        'labels': [entry['month'].strftime('%B %Y') for entry in client_growth],
        'values': [entry['count'] for entry in client_growth]
    }

    # Top clients by revenue
    top_clients = Invoice.objects.filter(
        status='paid'
    ).values(
        'client__name'
    ).annotate(
        total_revenue=Sum('total')
    ).order_by('-total_revenue')[:5]

    top_clients_data = {
        'labels': [entry['client__name'] for entry in top_clients],
        'values': [float(entry['total_revenue']) for entry in top_clients]
    }

    context = {
        'total_clients': total_clients,
        'total_invoices': total_invoices,
        'pending_payments': pending_payments,
        'total_revenue': total_revenue,
        'revenue_data': json.dumps(revenue_data),
        'status_data': json.dumps(status_data),
        'growth_data': json.dumps(growth_data),
        'top_clients_data': json.dumps(top_clients_data)
    }
    return render(request, "overview.html", context)

##################################### Clients Section ####################################################
# Lists all clients
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})

# Registers a new client
def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client registered successfully!')
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'register_client.html', {'form': form})

# Displays details for a single client
def client_detail(request, client_id):
    client = Client.objects.get(id=client_id)
    invoices = Invoice.objects.filter(client=client)
    return render(request, 'client_detail.html', {'client': client, 'invoices': invoices})

################################ Invoice Section ############################################################
# creating invoices
def create_invoice(request):
    """Create a new invoice"""
    invoice_form = InvoiceForm()

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        
        # Get all form data for items
        item_count = int(request.POST.get('item_count', 0))
        item_forms = []
        valid_items = True
        
        # Create and validate each item form
        for i in range(item_count):
            prefix = f'item-{i}'
            form_data = {
                f'{prefix}-item_name': request.POST.get(f'{prefix}-item_name'),
                f'{prefix}-quantity': request.POST.get(f'{prefix}-quantity'),
                f'{prefix}-unit_price': request.POST.get(f'{prefix}-unit_price')
            }
            if any(form_data.values()):
                form = InvoiceItemForm(form_data, prefix=prefix)
                if not form.is_valid():
                    valid_items = False
                item_forms.append(form)
        
        invoice_form.item_forms = item_forms
        
        if invoice_form.is_valid() and valid_items and item_forms:
            try:
                invoice = invoice_form.save(commit=False)
                items_data = []
                for form in item_forms:
                    items_data.append({
                        'item_name': form.cleaned_data['item_name'],
                        'quantity': form.cleaned_data['quantity'],
                        'unit_price': str(form.cleaned_data['unit_price'])
                    })
                invoice.items = items_data
                invoice.save()
                messages.success(request, 'Invoice created successfully!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error saving invoice: {str(e)}')
        else:
            if not item_forms:
                messages.error(request, 'Please add at least one item to the invoice.')
            else:
                messages.error(request, 'Please correct the errors below.')

    return render(request, 'invoice_create.html', {
        'form': invoice_form,
        'invoice': None,
    })

def edit_invoice(request, invoice_id):
    """Edit an existing invoice"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice_form = InvoiceForm(instance=invoice)

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        
        # Get all form data for items
        item_count = int(request.POST.get('item_count', 0))
        item_forms = []
        valid_items = True
        
        # Create and validate each item form
        for i in range(item_count):
            prefix = f'item-{i}'
            form_data = {
                f'{prefix}-item_name': request.POST.get(f'{prefix}-item_name'),
                f'{prefix}-quantity': request.POST.get(f'{prefix}-quantity'),
                f'{prefix}-unit_price': request.POST.get(f'{prefix}-unit_price')
            }
            if any(form_data.values()):
                form = InvoiceItemForm(form_data, prefix=prefix)
                if not form.is_valid():
                    valid_items = False
                item_forms.append(form)
        
        invoice_form.item_forms = item_forms
        
        if invoice_form.is_valid() and valid_items and item_forms:
            try:
                invoice = invoice_form.save(commit=False)
                items_data = []
                for form in item_forms:
                    items_data.append({
                        'item_name': form.cleaned_data['item_name'],
                        'quantity': form.cleaned_data['quantity'],
                        'unit_price': str(form.cleaned_data['unit_price'])
                    })
                invoice.items = items_data
                invoice.save()
                messages.success(request, 'Invoice updated successfully!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error updating invoice: {str(e)}')
        else:
            if not item_forms:
                messages.error(request, 'Please add at least one item to the invoice.')
            else:
                messages.error(request, 'Please correct the errors below.')

    # Pre-populate item forms for existing items
    if invoice.items:
        item_forms = []
        for i, item in enumerate(invoice.items):
            prefix = f'item-{i}'
            form = InvoiceItemForm(
                initial={
                    'item_name': item['item_name'],
                    'quantity': item['quantity'],
                    'unit_price': item['unit_price']
                },
                prefix=prefix
            )
            item_forms.append(form)
        invoice_form.item_forms = item_forms

    return render(request, 'invoice_create.html', {
        'form': invoice_form,
        'invoice': invoice,
    })

def delete_invoice(request, invoice_id):
    """Delete an invoice"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        try:
            invoice.delete()
            messages.success(request, 'Invoice deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting invoice: {str(e)}')
    else:
        messages.error(request, 'Invalid request method for deletion.')
    
    return redirect('dashboard')

def update_invoice_status(request, invoice_id):
    """Update invoice status"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['paid', 'pending', 'unpaid']:
            try:
                invoice.status = status
                invoice.save()
                messages.success(request, 'Invoice status updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating invoice status: {str(e)}')
        else:
            messages.error(request, 'Invalid status value')
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def invoice_list(request):
    """List all invoices"""
    invoices = Invoice.objects.all().order_by('-invoice_date')
    return render(request, 'invoices.html', {'invoices': invoices})




