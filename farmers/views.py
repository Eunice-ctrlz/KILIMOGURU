from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Sum, Avg, Count
import json

from .models import FarmerProfile, FarmParcel, FarmingHistory, CreditHistory
from .forms import (
    FarmerProfileForm, FarmParcelForm, FarmingHistoryForm,
    CompleteProfileForm, CreditApplicationForm
)


class FarmerRequiredMixin(LoginRequiredMixin):
    """Mixin to ensure user is a farmer"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_farmer:
            messages.error(request, 'Access denied. Farmer account required.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class FarmerDashboardView(FarmerRequiredMixin, TemplateView):
    """Farmer dashboard with overview"""
    template_name = 'farmers/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            profile = user.farmer_profile
        except FarmerProfile.DoesNotExist:
            profile = FarmerProfile.objects.create(user=user)
        
        # Farm statistics
        context['profile'] = profile
        context['total_parcels'] = profile.parcels.filter(is_active=True).count()
        context['total_farm_area'] = profile.parcels.filter(
            is_active=True
        ).aggregate(total=Sum('size'))['total'] or 0
        
        # Current crops
        context['current_crops'] = FarmingHistory.objects.filter(
            farmer_profile=profile,
            harvest_date__isnull=True
        ).select_related('parcel')[:5]
        
        # Recent farming history
        context['recent_history'] = FarmingHistory.objects.filter(
            farmer_profile=profile
        ).order_by('-created_at')[:5]
        
        # Credit information
        context['credit_score'] = profile.credit_score
        context['credit_limit'] = profile.credit_limit
        context['active_loans'] = CreditHistory.objects.filter(
            farmer_profile=profile,
            status__in=['active', 'disbursed']
        )
        context['total_outstanding'] = context['active_loans'].aggregate(
            total=Sum('outstanding_amount')
        )['total'] or 0
        
        # Yield statistics
        context['total_yield_this_year'] = FarmingHistory.objects.filter(
            farmer_profile=profile,
            year=2024,
            actual_yield__isnull=False
        ).aggregate(total=Sum('actual_yield'))['total'] or 0
        
        # Profit statistics
        profits = FarmingHistory.objects.filter(
            farmer_profile=profile,
            total_revenue__isnull=False,
            total_cost__isnull=False
        )
        context['total_profit'] = sum([h.profit for h in profits if h.profit]) if profits else 0
        
        return context


class FarmerProfileView(FarmerRequiredMixin, View):
    """View farmer profile"""
    template_name = 'farmers/profile.html'
    
    def get(self, request):
        try:
            profile = request.user.farmer_profile
        except FarmerProfile.DoesNotExist:
            profile = FarmerProfile.objects.create(user=request.user)
        
        return render(request, self.template_name, {'profile': profile})


class FarmerProfileEditView(FarmerRequiredMixin, UpdateView):
    """Edit farmer profile"""
    model = FarmerProfile
    form_class = FarmerProfileForm
    template_name = 'farmers/profile_edit.html'
    success_url = reverse_lazy('farmers:profile')
    
    def get_object(self):
        try:
            return self.request.user.farmer_profile
        except FarmerProfile.DoesNotExist:
            return FarmerProfile.objects.create(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class CompleteProfileView(FarmerRequiredMixin, UpdateView):
    """Complete farmer profile setup"""
    model = FarmerProfile
    form_class = CompleteProfileForm
    template_name = 'farmers/complete_profile.html'
    success_url = reverse_lazy('farmers:dashboard')
    
    def get_object(self):
        try:
            return self.request.user.farmer_profile
        except FarmerProfile.DoesNotExist:
            return FarmerProfile.objects.create(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Profile completed successfully! Welcome to KILIMO GURU.'
        )
        return super().form_valid(form)


class FarmParcelListView(FarmerRequiredMixin, ListView):
    """List all farm parcels"""
    model = FarmParcel
    template_name = 'farmers/parcel_list.html'
    context_object_name = 'parcels'
    
    def get_queryset(self):
        try:
            profile = self.request.user.farmer_profile
            return FarmParcel.objects.filter(farmer_profile=profile)
        except FarmerProfile.DoesNotExist:
            return FarmParcel.objects.none()


class FarmParcelCreateView(FarmerRequiredMixin, CreateView):
    """Create new farm parcel"""
    model = FarmParcel
    form_class = FarmParcelForm
    template_name = 'farmers/parcel_form.html'
    success_url = reverse_lazy('farmers:parcel_list')
    
    def form_valid(self, form):
        try:
            profile = self.request.user.farmer_profile
        except FarmerProfile.DoesNotExist:
            profile = FarmerProfile.objects.create(user=self.request.user)
        
        form.instance.farmer_profile = profile
        messages.success(self.request, 'Farm parcel added successfully!')
        return super().form_valid(form)


class FarmParcelDetailView(FarmerRequiredMixin, DetailView):
    """View farm parcel details"""
    model = FarmParcel
    template_name = 'farmers/parcel_detail.html'
    context_object_name = 'parcel'
    
    def get_queryset(self):
        try:
            profile = self.request.user.farmer_profile
            return FarmParcel.objects.filter(farmer_profile=profile)
        except FarmerProfile.DoesNotExist:
            return FarmParcel.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crop_history'] = FarmingHistory.objects.filter(
            parcel=self.object
        ).order_by('-year', '-season')
        return context


class FarmParcelUpdateView(FarmerRequiredMixin, UpdateView):
    """Update farm parcel"""
    model = FarmParcel
    form_class = FarmParcelForm
    template_name = 'farmers/parcel_form.html'
    success_url = reverse_lazy('farmers:parcel_list')
    
    def get_queryset(self):
        try:
            profile = self.request.user.farmer_profile
            return FarmParcel.objects.filter(farmer_profile=profile)
        except FarmerProfile.DoesNotExist:
            return FarmParcel.objects.none()
    
    def form_valid(self, form):
        messages.success(self.request, 'Farm parcel updated successfully!')
        return super().form_valid(form)


class FarmParcelDeleteView(FarmerRequiredMixin, DeleteView):
    """Delete farm parcel"""
    model = FarmParcel
    template_name = 'farmers/parcel_confirm_delete.html'
    success_url = reverse_lazy('farmers:parcel_list')
    
    def get_queryset(self):
        try:
            profile = self.request.user.farmer_profile
            return FarmParcel.objects.filter(farmer_profile=profile)
        except FarmerProfile.DoesNotExist:
            return FarmParcel.objects.none()
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Farm parcel deleted successfully!')
        return super().delete(request, *args, **kwargs)


class FarmingHistoryListView(FarmerRequiredMixin, ListView):
    """List farming history"""
    model = FarmingHistory
    template_name = 'farmers/history_list.html'
    context_object_name = 'history_list'
    paginate_by = 20
    
    def get_queryset(self):
        try:
            profile = self.request.user.farmer_profile
            return FarmingHistory.objects.filter(farmer_profile=profile)
        except FarmerProfile.DoesNotExist:
            return FarmingHistory.objects.none()


class FarmingHistoryCreateView(FarmerRequiredMixin, CreateView):
    """Add farming history record"""
    model = FarmingHistory
    form_class = FarmingHistoryForm
    template_name = 'farmers/history_form.html'
    success_url = reverse_lazy('farmers:history_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        try:
            profile = self.request.user.farmer_profile
        except FarmerProfile.DoesNotExist:
            profile = FarmerProfile.objects.create(user=self.request.user)
        
        form.instance.farmer_profile = profile
        messages.success(self.request, 'Farming record added successfully!')
        return super().form_valid(form)


class FarmingHistoryUpdateView(FarmerRequiredMixin, UpdateView):
    """Update farming history record"""
    model = FarmingHistory
    form_class = FarmingHistoryForm
    template_name = 'farmers/history_form.html'
    success_url = reverse_lazy('farmers:history_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        try:
            profile = self.request.user.farmer_profile
            return FarmingHistory.objects.filter(farmer_profile=profile)
        except FarmerProfile.DoesNotExist:
            return FarmingHistory.objects.none()
    
    def form_valid(self, form):
        messages.success(self.request, 'Farming record updated successfully!')
        return super().form_valid(form)


class CropRotationPlannerView(FarmerRequiredMixin, TemplateView):
    """Crop rotation planning tool"""
    template_name = 'farmers/rotation_planner.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = self.request.user.farmer_profile
            
            # Get crop history for rotation suggestions
            crop_history = FarmingHistory.objects.filter(
                farmer_profile=profile
            ).values('crop_name').annotate(
                count=Count('id'),
                last_year=Avg('year')
            ).order_by('-last_year')
            
            context['crop_history'] = crop_history
            context['parcels'] = FarmParcel.objects.filter(
                farmer_profile=profile,
                is_active=True
            )
            
            # Rotation suggestions based on common Kenyan crops
            context['rotation_suggestions'] = {
                'maize': ['beans', 'peas', 'potatoes', 'cabbage'],
                'beans': ['maize', 'sorghum', 'millet', 'sweet_potatoes'],
                'wheat': ['peas', 'lentils', 'fallow', 'canola'],
                'coffee': ['bananas', 'macadamia', 'shade_trees'],
                'tea': ['shade_trees', 'cover_crops'],
            }
            
        except FarmerProfile.DoesNotExist:
            context['crop_history'] = []
            context['parcels'] = []
        
        return context


class FarmMappingView(FarmerRequiredMixin, TemplateView):
    """GPS farm mapping view"""
    template_name = 'farmers/map_farm.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = self.request.user.farmer_profile
            context['parcels'] = FarmParcel.objects.filter(farmer_profile=profile)
            context['profile'] = profile
        except FarmerProfile.DoesNotExist:
            context['parcels'] = []
            context['profile'] = None
        return context


class SaveFarmBoundaryView(FarmerRequiredMixin, View):
    """API endpoint to save farm boundary coordinates"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            parcel_id = data.get('parcel_id')
            coordinates = data.get('coordinates')
            
            if not coordinates:
                return JsonResponse({
                    'success': False,
                    'error': 'No coordinates provided'
                })
            
            try:
                profile = request.user.farmer_profile
            except FarmerProfile.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Farmer profile not found'
                })
            
            if parcel_id:
                parcel = get_object_or_404(
                    FarmParcel,
                    id=parcel_id,
                    farmer_profile=profile
                )
                parcel.boundary_coordinates = coordinates
                parcel.save()
            else:
                # Create new parcel with boundary
                parcel = FarmParcel.objects.create(
                    farmer_profile=profile,
                    parcel_name=data.get('parcel_name', 'New Parcel'),
                    size=data.get('size', 0),
                    boundary_coordinates=coordinates
                )
            
            return JsonResponse({
                'success': True,
                'parcel_id': parcel.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


class KIAMISSyncView(FarmerRequiredMixin, View):
    """Sync farmer data with KIAMIS"""
    template_name = 'farmers/kiamis_sync.html'
    
    def get(self, request):
        # TODO: Implement actual KIAMIS API integration
        context = {
            'sync_status': 'pending',
            'message': 'KIAMIS integration is being configured.'
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        # TODO: Implement actual sync logic
        messages.info(request, 'KIAMIS sync initiated. This may take a few minutes.')
        return redirect('farmers:kiamis_sync')


class CreditScoreView(FarmerRequiredMixin, TemplateView):
    """View credit score and history"""
    template_name = 'farmers/credit_score.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = self.request.user.farmer_profile
            context['profile'] = profile
            context['credit_history'] = CreditHistory.objects.filter(
                farmer_profile=profile
            ).order_by('-application_date')[:10]
            
            # Calculate credit score factors
            context['score_factors'] = {
                'payment_history': min(100, profile.credit_score * 0.35),
                'credit_utilization': min(100, profile.credit_score * 0.30),
                'farm_performance': min(100, profile.credit_score * 0.20),
                'account_age': min(100, profile.credit_score * 0.15),
            }
            
        except FarmerProfile.DoesNotExist:
            context['profile'] = None
            context['credit_history'] = []
        
        return context
