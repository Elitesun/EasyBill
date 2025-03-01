from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Client, Invoice

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'description', 'tax', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tax': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_forms = []

    def add_item_form(self):
        self.item_forms.append(InvoiceItemForm(prefix=f'item-{len(self.item_forms)}'))

    def is_valid(self):
        is_valid = super().is_valid()
        if self.item_forms:
            for form in self.item_forms:
                is_valid = form.is_valid() and is_valid
        return is_valid

    def save(self, commit=True):
        # Create the invoice instance
        instance = super().save(commit=False)
        
        # Prepare items data
        items = []
        for form in self.item_forms:
            if form.is_valid():
                item_data = {
                    'item_name': form.cleaned_data['item_name'],
                    'quantity': form.cleaned_data['quantity'],
                    'unit_price': form.cleaned_data['unit_price']
                }
                items.append(item_data)
        
        # Set the items as a JSON field
        instance.items = items
        
        # Calculate total
        instance.total = instance.calculate_total
        
        if commit:
            instance.save()
        
        return instance

class InvoiceItemForm(forms.Form):
    item_name = forms.CharField(max_length=255, required=True)
    quantity = forms.IntegerField(min_value=1, required=True)
    unit_price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
