from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard
    path('', views.dashboard_view, name='hisab_dashboard'),
    path('dashboard/', views.dashboard_view, name='hisab_dashboard'),
    
    # Account management
    path('account/create/', views.create_account, name='create_account'),
    path('account/<int:account_id>/edit/', views.edit_account, name='edit_account'),
    path('account/<int:account_id>/delete/', views.delete_account, name='delete_account'),
    path('account/<int:account_id>/details/', views.account_details, name='account_details'),
]