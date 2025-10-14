from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm, TransactionFormSet

@login_required
def dashboard_view(request):
    """Simple dashboard view with all accounts"""
    # Check if user profile is complete
    if not request.user.is_profile_complete:
        messages.warning(
            request, 
            'Please complete your profile to access all features.'
        )
        return redirect('profile')

    accounts = Account.objects.filter(user=request.user).order_by('-updated_at')
    
    # Calculate totals for each account
    accounts_data = []
    for account in accounts:
        total = Transaction.objects.filter(account=account).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        accounts_data.append({
            'account': account,
            'total': total,
            'transactions': Transaction.objects.filter(account=account).order_by('-date')[:5]  # Show recent 5
        })

    context = {
        'accounts_data': accounts_data
    }
    return render(request, 'hisab/dashboard.html', context)

@login_required
def create_account(request):
    """Create new account with transactions using forms"""
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.user = request.user
            account.save()
            
            # Handle transactions using formset
            formset = TransactionFormSet(request.POST, instance=account)
            if formset.is_valid():
                formset.save()
                messages.success(request, f'Account "{account.name}" created successfully!')
            else:
                messages.warning(request, 'Account created, but some transactions had errors.')
            
            return redirect('hisab_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        account_form = AccountForm()
        # For create, show one empty transaction form (optional)
        formset = TransactionFormSet(extra=1)

    context = {
        'account_form': account_form,
        'transaction_formset': formset,
        'is_create': True,
        'title': 'Create New Account'
    }
    return render(request, 'hisab/account_form.html', context)

@login_required  
def edit_account(request, account_id):
    """Edit existing account with transactions using forms"""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        account_form = AccountForm(request.POST, instance=account)
        formset = TransactionFormSet(request.POST, instance=account)
        
        if account_form.is_valid() and formset.is_valid():
            account_form.save()
            formset.save()
            messages.success(request, f'Account "{account.name}" updated successfully!')
            return redirect('hisab_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        account_form = AccountForm(instance=account)
        formset = TransactionFormSet(instance=account)

    context = {
        'account_form': account_form,
        'transaction_formset': formset,
        'account': account,
        'is_create': False,
        'title': f'Edit Account: {account.name}'
    }
    return render(request, 'hisab/account_form.html', context)

@login_required
def delete_account(request, account_id):
    """Delete account with confirmation"""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        account_name = account.name
        account.delete()
        messages.success(request, f'Account "{account_name}" deleted successfully!')
        return redirect('hisab_dashboard')

    context = {
        'account': account,
        'total_transactions': Transaction.objects.filter(account=account).count()
    }
    return render(request, 'hisab/confirm_delete.html', context)



@login_required
def account_details(request, account_id):
    """View and manage account transactions using formsets - EXACT COPY of edit_account pattern"""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        # Use EXACT same pattern as edit_account
        print(f"POST data received: {dict(request.POST)}")  # Debug
        formset = TransactionFormSet(request.POST, instance=account)
        print(f"Formset errors: {formset.errors}")  # Debug
        print(f"Formset is_valid: {formset.is_valid()}")  # Debug
        
        if formset.is_valid():
            instances = formset.save()
            print(f"Saved instances: {len(instances)}")  # Debug
            messages.success(request, f'Transactions for "{account.name}" updated successfully!')
            return redirect('account_details', account_id=account.id)
        else:
            print(f"Form errors: {formset.errors}")  # Debug
            print(f"Non-form errors: {formset.non_form_errors()}")  # Debug
            messages.error(request, 'Please correct the errors below.')
    else:
        formset = TransactionFormSet(instance=account)

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    total = transactions.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'account': account,
        'transactions': transactions,
        'transaction_formset': formset,
        'total': total,
        'title': f'Account Details: {account.name}'
    }
    return render(request, 'hisab/account_details.html', context)