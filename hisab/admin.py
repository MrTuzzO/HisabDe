from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import Account, Transaction


class TransactionInline(admin.TabularInline):
    """Inline for managing transactions within Account admin"""
    model = Transaction
    extra = 1  # Number of empty forms to display
    fields = ('description', 'amount', 'date')
    readonly_fields = ('date',)  # Make date readonly since it's auto_now_add
    
    def get_readonly_fields(self, request, obj=None):
        # Make date editable when creating new transactions
        if obj:  # Editing existing account
            return ('date',)
        return ()  # Creating new account - allow date editing


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Admin interface for Account with inline transactions"""
    
    inlines = [TransactionInline]
    
    list_display = (
        'name', 
        'email', 
        'user', 
        'mobile', 
        'reminder_interval', 
        'total_amount_display', 
        'transaction_count',
        'created_at',
        'updated_at'
    )
    
    list_filter = (
        'reminder_interval', 
        'created_at', 
        'updated_at',
        'user'
    )
    
    search_fields = (
        'name', 
        'email', 
        'mobile',
        'user__email',
        'user__full_name'
    )
    
    readonly_fields = (
        'created_at', 
        'updated_at', 
        'total_amount_display', 
        'transaction_count'
    )
    
    fieldsets = (
        ('Account Information', {
            'fields': ('user', 'name', 'email', 'mobile')
        }),
        ('Settings', {
            'fields': ('reminder_interval',)
        }),
        ('Statistics', {
            'fields': ('total_amount_display', 'transaction_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_amount_display(self, obj):
        """Display total amount with color coding"""
        total = Transaction.objects.filter(account=obj).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        color = 'green' if total >= 0 else 'red'
        symbol = '+' if total >= 0 else ''
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} ₹{}</span>',
            color, symbol, abs(total)
        )
    total_amount_display.short_description = 'Total Amount'
    
    def transaction_count(self, obj):
        """Display number of transactions"""
        count = Transaction.objects.filter(account=obj).count()
        return f"{count} transactions"
    transaction_count.short_description = 'Transaction Count'
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related('user')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for individual Transaction management"""
    
    list_display = (
        'description', 
        'account_name',
        'account_user', 
        'amount_display',
        'date'
    )
    
    list_filter = (
        'date', 
        'account__user',
        'account__name'
    )
    
    search_fields = (
        'description', 
        'account__name',
        'account__email',
        'account__user__email'
    )
    
    readonly_fields = ('date',)
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('account', 'description', 'amount')
        }),
        ('Timestamp', {
            'fields': ('date',),
            'classes': ('collapse',)
        }),
    )
    
    def account_name(self, obj):
        """Display account name as link"""
        return format_html(
            '<a href="/admin/hisab/account/{}/change/">{}</a>',
            obj.account.id, obj.account.name
        )
    account_name.short_description = 'Account'
    
    def account_user(self, obj):
        """Display account owner"""
        return obj.account.user.get_full_name() or obj.account.user.email
    account_user.short_description = 'Owner'
    
    def amount_display(self, obj):
        """Display amount with color coding"""
        color = 'green' if obj.amount >= 0 else 'red'
        symbol = '+' if obj.amount >= 0 else ''
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} ₹{}</span>',
            color, symbol, abs(obj.amount)
        )
    amount_display.short_description = 'Amount'
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related('account', 'account__user')

