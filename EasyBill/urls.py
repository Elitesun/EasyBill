from django.urls import path 
from .views import (
    Home, login_page, register_page, dashboard, overview,
    client_list, register_client, client_detail, 
    create_invoice, edit_invoice, delete_invoice, update_invoice_status,
    invoice_list
)

urlpatterns=[
    path('', Home , name='home'),
    path('login', login_page , name='login'),
    path('register', register_page , name='register'),
    path('dashboard', dashboard , name='dashboard'),
    path('overview', overview , name='overview'),

    # Client URLs
    path('clients/', client_list, name='client_list'),
    path('clients/register/', register_client, name='register_client'),
    path('clients/<int:client_id>/', client_detail, name='client_detail'),

    # Invoice URLs
    path('invoices/', invoice_list, name='invoice_list'),
    path('invoice/create/', create_invoice, name='create_invoice'),
    path('invoice/edit/<int:invoice_id>/', edit_invoice, name='edit_invoice'),
    path('invoice/delete/<int:invoice_id>/', delete_invoice, name='delete_invoice'),
    path('invoice/update-status/<int:invoice_id>/', update_invoice_status, name='update_invoice_status'),
]
