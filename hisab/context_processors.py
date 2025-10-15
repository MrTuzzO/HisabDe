from django.db.models import Sum
from .models import Account, Transaction


def overall_balance(request):
    """Context processor to calculate overall balance for authenticated users"""
    if request.user.is_authenticated:
        # Get all accounts for the user
        accounts = Account.objects.filter(user=request.user)
        
        # Calculate overall total from all transactions
        overall_total = Transaction.objects.filter(
            account__user=request.user
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return {
            'overall_total': overall_total
        }
    return {
        'overall_total': 0
    }
