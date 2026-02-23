from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Sum, Count

from .models import (
    Crop, CropVariety, FarmerCrop, PestDisease, PestDiseaseDetection,
    Livestock, LivestockProduction, PlantingCalendar
)
from .forms import (
    FarmerCropForm, LivestockForm, LivestockProductionForm,
    PestDiseaseDetectionForm
)


class CropListView(ListView):
    """List all crops"""
    model = Crop
    template_name = 'crops/crop_list.html'
    context_object_name = 'crops'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Crop.objects.filter(is_active=True)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Crop.CROP_CATEGORIES
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class CropDetailView(DetailView):
    """Crop details"""
    model = Crop
    template_name = 'crops/crop_detail.html'
    context_object_name = 'crop'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['varieties'] = self.object.varieties.all()
        context['pests_diseases'] = self.object.pests_diseases.filter(is_active=True)
        context['planting_calendars'] = self.object.planting_calendars.all()
        return context


class MyCropsView(LoginRequiredMixin, ListView):
    """List farmer's crops"""
    model = FarmerCrop
    template_name = 'crops/my_crops.html'
    context_object_name = 'crops'
    
    def get_queryset(self):
        return FarmerCrop.objects.filter(farmer=self.request.user).select_related('crop', 'variety')


class FarmerCropCreateView(LoginRequiredMixin, CreateView):
    """Add a new crop planting"""
    model = FarmerCrop
    form_class = FarmerCropForm
    template_name = 'crops/farmercrop_form.html'
    success_url = reverse_lazy('crops:my_crops')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        messages.success(self.request, 'Crop added successfully!')
        return super().form_valid(form)


class FarmerCropUpdateView(LoginRequiredMixin, UpdateView):
    """Update crop planting"""
    model = FarmerCrop
    form_class = FarmerCropForm
    template_name = 'crops/farmercrop_form.html'
    success_url = reverse_lazy('crops:my_crops')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        return FarmerCrop.objects.filter(farmer=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Crop updated successfully!')
        return super().form_valid(form)


class FarmerCropDeleteView(LoginRequiredMixin, DeleteView):
    """Delete crop planting"""
    model = FarmerCrop
    template_name = 'crops/farmercrop_confirm_delete.html'
    success_url = reverse_lazy('crops:my_crops')
    
    def get_queryset(self):
        return FarmerCrop.objects.filter(farmer=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Crop record deleted successfully!')
        return super().delete(request, *args, **kwargs)


class PlantingCalendarView(TemplateView):
    """Planting calendar view"""
    template_name = 'crops/planting_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = PlantingCalendar.objects.values_list(
            'region', flat=True
        ).distinct()
        context['crops'] = Crop.objects.filter(is_active=True)
        
        # Current month activities
        from datetime import datetime
        current_month = datetime.now().month
        
        context['current_month_activities'] = PlantingCalendar.objects.filter(
            short_rains_start=current_month
        ) | PlantingCalendar.objects.filter(
            long_rains_start=current_month
        )
        
        return context


class RegionalCalendarView(TemplateView):
    """Regional planting calendar"""
    template_name = 'crops/regional_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        region = self.kwargs.get('region')
        context['region'] = region
        context['calendars'] = PlantingCalendar.objects.filter(
            region=region
        ).select_related('crop')
        return context


class PestDiseaseListView(ListView):
    """List pests and diseases"""
    model = PestDisease
    template_name = 'crops/pest_disease_list.html'
    context_object_name = 'pests_diseases'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = PestDisease.objects.filter(is_active=True)
        
        # Filter by type
        pest_type = self.request.GET.get('type')
        if pest_type:
            queryset = queryset.filter(pest_disease_type=pest_type)
        
        # Filter by crop
        crop_id = self.request.GET.get('crop')
        if crop_id:
            queryset = queryset.filter(affected_crops__id=crop_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = PestDisease.TYPE_CHOICES
        context['crops'] = Crop.objects.filter(is_active=True)
        return context


class PestDiseaseDetailView(DetailView):
    """Pest/Disease details"""
    model = PestDisease
    template_name = 'crops/pest_disease_detail.html'
    context_object_name = 'pest_disease'


class PestDiseaseDetectView(LoginRequiredMixin, CreateView):
    """AI pest/disease detection"""
    model = PestDiseaseDetection
    form_class = PestDiseaseDetectionForm
    template_name = 'crops/detect.html'
    success_url = reverse_lazy('crops:my_detections')
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        
        # TODO: Integrate with AI model for detection
        # For now, simulate detection
        messages.info(
            self.request,
            'Image uploaded for analysis. Our AI is processing your image.'
        )
        
        return super().form_valid(form)


class MyDetectionsView(LoginRequiredMixin, ListView):
    """List user's pest/disease detections"""
    model = PestDiseaseDetection
    template_name = 'crops/my_detections.html'
    context_object_name = 'detections'
    
    def get_queryset(self):
        return PestDiseaseDetection.objects.filter(
            farmer=self.request.user
        ).select_related('detected_pest_disease')


class LivestockListView(LoginRequiredMixin, ListView):
    """List farmer's livestock"""
    model = Livestock
    template_name = 'crops/livestock_list.html'
    context_object_name = 'livestock_list'
    
    def get_queryset(self):
        return Livestock.objects.filter(
            farmer=self.request.user,
            is_active=True
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        livestock = self.get_queryset()
        context['total_animals'] = livestock.count()
        context['species_count'] = livestock.values('species').distinct().count()
        
        # Count by species
        context['species_breakdown'] = livestock.values('species').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return context


class LivestockCreateView(LoginRequiredMixin, CreateView):
    """Add new livestock"""
    model = Livestock
    form_class = LivestockForm
    template_name = 'crops/livestock_form.html'
    success_url = reverse_lazy('crops:livestock_list')
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        messages.success(self.request, 'Livestock added successfully!')
        return super().form_valid(form)


class LivestockDetailView(LoginRequiredMixin, DetailView):
    """Livestock details"""
    model = Livestock
    template_name = 'crops/livestock_detail.html'
    context_object_name = 'animal'
    
    def get_queryset(self):
        return Livestock.objects.filter(farmer=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['production_records'] = LivestockProduction.objects.filter(
            livestock=self.object
        )[:10]
        return context


class LivestockUpdateView(LoginRequiredMixin, UpdateView):
    """Update livestock"""
    model = Livestock
    form_class = LivestockForm
    template_name = 'crops/livestock_form.html'
    success_url = reverse_lazy('crops:livestock_list')
    
    def get_queryset(self):
        return Livestock.objects.filter(farmer=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Livestock updated successfully!')
        return super().form_valid(form)


class LivestockDeleteView(LoginRequiredMixin, DeleteView):
    """Delete livestock"""
    model = Livestock
    template_name = 'crops/livestock_confirm_delete.html'
    success_url = reverse_lazy('crops:livestock_list')
    
    def get_queryset(self):
        return Livestock.objects.filter(farmer=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Livestock record deleted successfully!')
        return super().delete(request, *args, **kwargs)


class AddProductionView(LoginRequiredMixin, CreateView):
    """Add production record"""
    model = LivestockProduction
    form_class = LivestockProductionForm
    template_name = 'crops/production_form.html'
    
    def get_livestock(self):
        return get_object_or_404(
            Livestock,
            pk=self.kwargs.get('pk'),
            farmer=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animal'] = self.get_livestock()
        return context
    
    def form_valid(self, form):
        form.instance.livestock = self.get_livestock()
        messages.success(self.request, 'Production record added successfully!')
        return redirect('crops:livestock_detail', pk=self.kwargs.get('pk'))
