from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Avg

from .models import (
    MarketPrice, ProduceListing, LivestockListing,
    BuyerInquiry, BuyerRequest, Transaction
)
from .forms import (
    ProduceListingForm, LivestockListingForm, BuyerInquiryForm,
    BuyerRequestForm, InquiryResponseForm
)


class MarketPriceListView(ListView):
    """List current market prices"""
    model = MarketPrice
    template_name = 'marketplace/prices.html'
    context_object_name = 'prices'
    paginate_by = 30
    
    def get_queryset(self):
        from datetime import date, timedelta
        # Get prices from last 7 days
        recent_date = date.today() - timedelta(days=7)
        queryset = MarketPrice.objects.filter(price_date__gte=recent_date)
        
        # Filter by market
        market = self.request.GET.get('market')
        if market:
            queryset = queryset.filter(market=market)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(product_name__icontains=search)
        
        return queryset.order_by('-price_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markets'] = MarketPrice.MARKET_CHOICES
        context['categories'] = MarketPrice.category.field.choices
        context['selected_market'] = self.request.GET.get('market', '')
        context['selected_category'] = self.request.GET.get('category', '')
        
        # Price trends
        from datetime import date
        today = date.today()
        context['trending_up'] = self.get_queryset().filter(
            price_date=today
        )[:5]
        
        return context


class MarketPriceByMarketView(ListView):
    """Prices by specific market"""
    model = MarketPrice
    template_name = 'marketplace/prices_by_market.html'
    context_object_name = 'prices'
    
    def get_queryset(self):
        market = self.kwargs.get('market')
        from datetime import date, timedelta
        recent_date = date.today() - timedelta(days=7)
        return MarketPrice.objects.filter(
            market=market,
            price_date__gte=recent_date
        ).order_by('product_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['market'] = self.kwargs.get('market')
        context['market_display'] = dict(MarketPrice.MARKET_CHOICES).get(
            self.kwargs.get('market')
        )
        return context


class ProduceListingListView(ListView):
    """List produce listings"""
    model = ProduceListing
    template_name = 'marketplace/produce_list.html'
    context_object_name = 'listings'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ProduceListing.objects.filter(status='active')
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by county
        county = self.request.GET.get('county')
        if county:
            queryset = queryset.filter(county__icontains=county)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price_per_unit__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_unit__lte=max_price)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(product_name__icontains=search) |
                Q(description__icontains=search) |
                Q(variety__icontains=search)
            )
        
        return queryset.select_related('farmer')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProduceListing.category.field.choices
        return context


class ProduceListingDetailView(DetailView):
    """Produce listing details"""
    model = ProduceListing
    template_name = 'marketplace/produce_detail.html'
    context_object_name = 'listing'
    
    def get_queryset(self):
        return ProduceListing.objects.filter(status='active')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Increment view count
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])
        
        # Similar listings
        context['similar_listings'] = ProduceListing.objects.filter(
            category=self.object.category,
            status='active'
        ).exclude(id=self.object.id)[:4]
        
        return context


class ProduceListingCreateView(LoginRequiredMixin, CreateView):
    """Create produce listing"""
    model = ProduceListing
    form_class = ProduceListingForm
    template_name = 'marketplace/produce_form.html'
    success_url = reverse_lazy('marketplace:my_listings')
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        messages.success(self.request, 'Listing created successfully!')
        return super().form_valid(form)


class ProduceListingUpdateView(LoginRequiredMixin, UpdateView):
    """Update produce listing"""
    model = ProduceListing
    form_class = ProduceListingForm
    template_name = 'marketplace/produce_form.html'
    success_url = reverse_lazy('marketplace:my_listings')
    
    def get_queryset(self):
        return ProduceListing.objects.filter(farmer=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Listing updated successfully!')
        return super().form_valid(form)


class ProduceListingDeleteView(LoginRequiredMixin, DeleteView):
    """Delete produce listing"""
    model = ProduceListing
    template_name = 'marketplace/produce_confirm_delete.html'
    success_url = reverse_lazy('marketplace:my_listings')
    
    def get_queryset(self):
        return ProduceListing.objects.filter(farmer=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Listing deleted successfully!')
        return super().delete(request, *args, **kwargs)


class LivestockListingListView(ListView):
    """List livestock listings"""
    model = LivestockListing
    template_name = 'marketplace/livestock_list.html'
    context_object_name = 'listings'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = LivestockListing.objects.filter(status='active')
        
        # Filter by species
        species = self.request.GET.get('species')
        if species:
            queryset = queryset.filter(species=species)
        
        return queryset


class LivestockListingDetailView(DetailView):
    """Livestock listing details"""
    model = LivestockListing
    template_name = 'marketplace/livestock_detail.html'
    context_object_name = 'listing'
    
    def get_queryset(self):
        return LivestockListing.objects.filter(status='active')


class LivestockListingCreateView(LoginRequiredMixin, CreateView):
    """Create livestock listing"""
    model = LivestockListing
    form_class = LivestockListingForm
    template_name = 'marketplace/livestock_form.html'
    success_url = reverse_lazy('marketplace:my_listings')
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        messages.success(self.request, 'Livestock listing created successfully!')
        return super().form_valid(form)


class BuyerInquiryCreateView(LoginRequiredMixin, CreateView):
    """Create buyer inquiry"""
    model = BuyerInquiry
    form_class = BuyerInquiryForm
    template_name = 'marketplace/inquiry_form.html'
    
    def get_listing(self):
        return get_object_or_404(ProduceListing, pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = self.get_listing()
        return context
    
    def form_valid(self, form):
        form.instance.buyer = self.request.user
        form.instance.listing = self.get_listing()
        
        # Update listing inquiry count
        listing = self.get_listing()
        listing.inquiry_count += 1
        listing.save(update_fields=['inquiry_count'])
        
        messages.success(self.request, 'Inquiry sent successfully!')
        return redirect('marketplace:produce_detail', pk=listing.pk)


class BuyerRequestListView(ListView):
    """List buyer requests"""
    model = BuyerRequest
    template_name = 'marketplace/request_list.html'
    context_object_name = 'requests'
    paginate_by = 20
    
    def get_queryset(self):
        return BuyerRequest.objects.filter(status='active')


class BuyerRequestCreateView(LoginRequiredMixin, CreateView):
    """Create buyer request"""
    model = BuyerRequest
    form_class = BuyerRequestForm
    template_name = 'marketplace/request_form.html'
    success_url = reverse_lazy('marketplace:request_list')
    
    def form_valid(self, form):
        form.instance.buyer = self.request.user
        messages.success(self.request, 'Request posted successfully!')
        return super().form_valid(form)


class MyListingsView(LoginRequiredMixin, ListView):
    """Farmer's own listings"""
    model = ProduceListing
    template_name = 'marketplace/my_listings.html'
    context_object_name = 'listings'
    
    def get_queryset(self):
        return ProduceListing.objects.filter(
            farmer=self.request.user
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['livestock_listings'] = LivestockListing.objects.filter(
            farmer=self.request.user
        ).order_by('-created_at')
        return context


class MyInquiriesView(LoginRequiredMixin, ListView):
    """Farmer's received inquiries"""
    model = BuyerInquiry
    template_name = 'marketplace/my_inquiries.html'
    context_object_name = 'inquiries'
    
    def get_queryset(self):
        return BuyerInquiry.objects.filter(
            listing__farmer=self.request.user
        ).order_by('-created_at')


class RespondInquiryView(LoginRequiredMixin, UpdateView):
    """Respond to buyer inquiry"""
    model = BuyerInquiry
    form_class = InquiryResponseForm
    template_name = 'marketplace/respond_inquiry.html'
    success_url = reverse_lazy('marketplace:my_inquiries')
    
    def get_queryset(self):
        return BuyerInquiry.objects.filter(
            listing__farmer=self.request.user
        )
    
    def form_valid(self, form):
        from django.utils import timezone
        form.instance.response_date = timezone.now()
        messages.success(self.request, 'Response sent successfully!')
        return super().form_valid(form)


class TransactionListView(LoginRequiredMixin, ListView):
    """List user's transactions"""
    model = Transaction
    template_name = 'marketplace/transactions.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        return Transaction.objects.filter(
            Q(farmer=self.request.user) | Q(buyer=self.request.user)
        ).order_by('-transaction_date')


class TransactionDetailView(LoginRequiredMixin, DetailView):
    """Transaction details"""
    model = Transaction
    template_name = 'marketplace/transaction_detail.html'
    context_object_name = 'transaction'
    
    def get_queryset(self):
        return Transaction.objects.filter(
            Q(farmer=self.request.user) | Q(buyer=self.request.user)
        )


class BuyerDashboardView(LoginRequiredMixin, TemplateView):
    """Buyer dashboard"""
    template_name = 'marketplace/buyer_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['my_requests'] = BuyerRequest.objects.filter(
            buyer=user
        )[:5]
        
        context['my_inquiries'] = BuyerInquiry.objects.filter(
            buyer=user
        )[:5]
        
        context['my_purchases'] = Transaction.objects.filter(
            buyer=user
        )[:5]
        
        # Recommended listings based on inquiries
        inquiry_products = BuyerInquiry.objects.filter(
            buyer=user
        ).values_list('listing__category', flat=True).distinct()
        
        context['recommended'] = ProduceListing.objects.filter(
            category__in=inquiry_products,
            status='active'
        ).exclude(
            inquiries__buyer=user
        )[:4]
        
        return context
