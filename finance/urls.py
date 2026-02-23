from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Dashboard
    path('', views.FinanceDashboardView.as_view(), name='dashboard'),
    
    # M-Pesa
    path('mpesa/pay/', views.MPesaPaymentView.as_view(), name='mpesa_pay'),
    path('mpesa/callback/', views.MPesaCallbackView.as_view(), name='mpesa_callback'),
    path('mpesa/history/', views.MPesaHistoryView.as_view(), name='mpesa_history'),
    
    # Loans
    path('loans/', views.LoanListView.as_view(), name='loan_list'),
    path('loans/<int:pk>/', views.LoanDetailView.as_view(), name='loan_detail'),
    path('loans/apply/', views.LoanApplyView.as_view(), name='loan_apply'),
    path('loans/<int:pk>/repay/', views.LoanRepayView.as_view(), name='loan_repay'),
    
    # Insurance
    path('insurance/', views.InsuranceListView.as_view(), name='insurance_list'),
    path('insurance/<int:pk>/', views.InsuranceDetailView.as_view(), name='insurance_detail'),
    path('insurance/buy/', views.InsuranceBuyView.as_view(), name='insurance_buy'),
    
    # Wallet
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('wallet/deposit/', views.WalletDepositView.as_view(), name='wallet_deposit'),
    path('wallet/withdraw/', views.WalletWithdrawView.as_view(), name='wallet_withdraw'),
]
