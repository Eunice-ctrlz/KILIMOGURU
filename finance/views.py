from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import (
    MPesaTransaction, LoanProduct, LoanApplication,
    LoanRepayment, InsuranceProduct, InsurancePolicy,
    Wallet, WalletTransaction
)
from .forms import (
    MPesaPaymentForm, LoanApplicationForm,
    InsurancePurchaseForm, WalletDepositForm
)


class FinanceDashboardView(LoginRequiredMixin, TemplateView):
    """Finance dashboard"""
    template_name = 'finance/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Wallet
        try:
            context['wallet'] = user.wallet
        except Wallet.DoesNotExist:
            context['wallet'] = Wallet.objects.create(user=user)
        
        # Recent M-Pesa transactions
        context['mpesa_transactions'] = MPesaTransaction.objects.filter(
            user=user
        )[:5]
        
        # Active loans
        context['active_loans'] = LoanApplication.objects.filter(
            farmer=user,
            status__in=['active', 'disbursed']
        )
        
        # Insurance policies
        context['insurance_policies'] = InsurancePolicy.objects.filter(
            farmer=user,
            status='active'
        )
        
        # Available loan products
        context['loan_products'] = LoanProduct.objects.filter(is_active=True)[:3]
        
        # Available insurance products
        context['insurance_products'] = InsuranceProduct.objects.filter(is_active=True)[:3]
        
        return context


class MPesaPaymentView(LoginRequiredMixin, CreateView):
    """M-Pesa payment"""
    model = MPesaTransaction
    form_class = MPesaPaymentForm
    template_name = 'finance/mpesa_payment.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'pending'
        
        # TODO: Integrate with M-Pesa API
        # For now, simulate payment
        messages.info(self.request, 'M-Pesa payment request initiated. Check your phone.')
        
        return super().form_valid(form)


class MPesaCallbackView(View):
    """M-Pesa callback endpoint"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        """Handle M-Pesa callback"""
        try:
            data = json.loads(request.body)
            
            # Process callback data
            checkout_request_id = data.get('CheckoutRequestID')
            result_code = data.get('ResultCode')
            result_desc = data.get('ResultDesc')
            
            try:
                transaction = MPesaTransaction.objects.get(
                    checkout_request_id=checkout_request_id
                )
                
                if result_code == 0:
                    transaction.status = 'completed'
                    transaction.mpesa_receipt_number = data.get('MpesaReceiptNumber')
                else:
                    transaction.status = 'failed'
                
                transaction.result_code = result_code
                transaction.result_description = result_desc
                transaction.save()
                
                return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Success'})
                
            except MPesaTransaction.DoesNotExist:
                return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Transaction not found'})
                
        except json.JSONDecodeError:
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid JSON'})


class MPesaHistoryView(LoginRequiredMixin, ListView):
    """M-Pesa transaction history"""
    model = MPesaTransaction
    template_name = 'finance/mpesa_history.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        return MPesaTransaction.objects.filter(
            user=self.request.user
        ).order_by('-initiated_at')


class LoanListView(LoginRequiredMixin, ListView):
    """List available loan products"""
    model = LoanProduct
    template_name = 'finance/loan_list.html'
    context_object_name = 'loan_products'
    
    def get_queryset(self):
        return LoanProduct.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_loans'] = LoanApplication.objects.filter(
            farmer=self.request.user
        ).order_by('-application_date')
        return context


class LoanDetailView(LoginRequiredMixin, DetailView):
    """Loan product details"""
    model = LoanProduct
    template_name = 'finance/loan_detail.html'
    context_object_name = 'loan'


class LoanApplyView(LoginRequiredMixin, CreateView):
    """Apply for a loan"""
    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = 'finance/loan_apply.html'
    success_url = '/finance/loans/'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        form.instance.status = 'submitted'
        messages.success(self.request, 'Loan application submitted successfully!')
        return super().form_valid(form)


class LoanRepayView(LoginRequiredMixin, View):
    """Repay a loan"""
    template_name = 'finance/loan_repay.html'
    
    def get(self, request, pk):
        loan = get_object_or_404(
            LoanApplication,
            pk=pk,
            farmer=request.user
        )
        return render(request, self.template_name, {'loan': loan})
    
    def post(self, request, pk):
        loan = get_object_or_404(
            LoanApplication,
            pk=pk,
            farmer=request.user
        )
        
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        
        # Create repayment record
        repayment = LoanRepayment.objects.create(
            loan=loan,
            amount=amount,
            payment_method=payment_method
        )
        
        # Update loan
        loan.total_repaid += float(amount)
        if loan.total_repaid >= loan.disbursed_amount:
            loan.status = 'repaid'
        loan.save()
        
        messages.success(request, 'Loan repayment recorded successfully!')
        return redirect('finance:loan_list')


class InsuranceListView(LoginRequiredMixin, ListView):
    """List insurance products"""
    model = InsuranceProduct
    template_name = 'finance/insurance_list.html'
    context_object_name = 'insurance_products'
    
    def get_queryset(self):
        return InsuranceProduct.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_policies'] = InsurancePolicy.objects.filter(
            farmer=self.request.user
        ).order_by('-created_at')
        return context


class InsuranceDetailView(LoginRequiredMixin, DetailView):
    """Insurance product details"""
    model = InsuranceProduct
    template_name = 'finance/insurance_detail.html'
    context_object_name = 'insurance'


class InsuranceBuyView(LoginRequiredMixin, CreateView):
    """Buy insurance"""
    model = InsurancePolicy
    form_class = InsurancePurchaseForm
    template_name = 'finance/insurance_buy.html'
    success_url = '/finance/insurance/'
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        form.instance.policy_number = self.generate_policy_number()
        form.instance.status = 'pending'
        messages.success(self.request, 'Insurance purchase initiated!')
        return super().form_valid(form)
    
    def generate_policy_number(self):
        import uuid
        return f"KIL-{uuid.uuid4().hex[:8].upper()}"


class WalletView(LoginRequiredMixin, TemplateView):
    """Wallet view"""
    template_name = 'finance/wallet.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            wallet = user.wallet
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=user)
        
        context['wallet'] = wallet
        context['transactions'] = WalletTransaction.objects.filter(
            wallet=wallet
        )[:20]
        
        return context


class WalletDepositView(LoginRequiredMixin, CreateView):
    """Deposit to wallet"""
    model = WalletTransaction
    form_class = WalletDepositForm
    template_name = 'finance/wallet_deposit.html'
    
    def form_valid(self, form):
        wallet = self.request.user.wallet
        
        form.instance.wallet = wallet
        form.instance.transaction_type = 'deposit'
        form.instance.balance_after = wallet.balance + form.instance.amount
        
        # Update wallet balance
        wallet.balance = form.instance.balance_after
        wallet.save()
        
        messages.success(self.request, 'Deposit successful!')
        return redirect('finance:wallet')


class WalletWithdrawView(LoginRequiredMixin, View):
    """Withdraw from wallet"""
    template_name = 'finance/wallet_withdraw.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        amount = float(request.POST.get('amount', 0))
        wallet = request.user.wallet
        
        if amount > wallet.balance:
            messages.error(request, 'Insufficient balance!')
            return render(request, self.template_name)
        
        # Create transaction
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type='withdrawal',
            amount=amount,
            balance_after=wallet.balance - amount,
            description='Wallet withdrawal'
        )
        
        # Update balance
        wallet.balance -= amount
        wallet.save()
        
        messages.success(request, 'Withdrawal successful!')
        return redirect('finance:wallet')
