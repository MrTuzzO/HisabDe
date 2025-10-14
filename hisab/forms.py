from django import forms
from django.forms import inlineformset_factory
from .models import Account, Transaction

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'email', 'mobile', 'reminder_interval']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',  # Space for floating label
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': ' '  # Space for floating label
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '  # Space for floating label
            }),
            'reminder_interval': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'date']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '  # Space for floating label
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': ' '  # Space for floating label
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': ' '  # Space for floating label
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default date to today
        if not self.instance.pk:
            from django.utils import timezone
            self.fields['date'].initial = timezone.now().date()

# Create formset for handling multiple transactions
TransactionFormSet = inlineformset_factory(
    Account, 
    Transaction,
    form=TransactionForm,
    extra=0,  # No extra forms by default (can be overridden in views)
    can_delete=True  # Allow deletion of transactions
)