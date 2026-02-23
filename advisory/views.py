from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone

from .models import (
    AdvisoryCategory, AdvisoryArticle, Webinar,
    ExpertConsultation, FAQ, FarmingTip, TeleVetConsultation
)
from .forms import (
    ConsultationBookingForm, TeleVetConsultationForm, WebinarRegistrationForm
)


class AdvisoryHomeView(TemplateView):
    """Advisory home page"""
    template_name = 'advisory/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Featured articles
        context['featured_articles'] = AdvisoryArticle.objects.filter(
            is_published=True
        ).select_related('category')[:6]
        
        # Upcoming webinars
        context['upcoming_webinars'] = Webinar.objects.filter(
            status='upcoming',
            scheduled_date__gte=timezone.now().date()
        )[:3]
        
        # Today's tip
        from datetime import date
        try:
            context['daily_tip'] = FarmingTip.objects.get(
                display_date=date.today(),
                is_active=True
            )
        except FarmingTip.DoesNotExist:
            context['daily_tip'] = None
        
        # Categories
        context['categories'] = AdvisoryCategory.objects.all()
        
        # Popular FAQs
        context['popular_faqs'] = FAQ.objects.filter(
            is_published=True
        ).order_by('-view_count')[:5]
        
        return context


class ArticleListView(ListView):
    """List advisory articles"""
    model = AdvisoryArticle
    template_name = 'advisory/article_list.html'
    context_object_name = 'articles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = AdvisoryArticle.objects.filter(is_published=True)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by language
        language = self.request.GET.get('language')
        if language:
            queryset = queryset.filter(language=language)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(content__icontains=search)
        
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = AdvisoryCategory.objects.all()
        context['languages'] = AdvisoryArticle.LANGUAGE_CHOICES
        return context


class ArticleDetailView(DetailView):
    """Article details"""
    model = AdvisoryArticle
    template_name = 'advisory/article_detail.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return AdvisoryArticle.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Increment view count
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])
        
        # Related articles
        context['related_articles'] = AdvisoryArticle.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:3]
        
        return context


class WebinarListView(ListView):
    """List webinars"""
    model = Webinar
    template_name = 'advisory/webinar_list.html'
    context_object_name = 'webinars'
    
    def get_queryset(self):
        return Webinar.objects.filter(
            scheduled_date__gte=timezone.now().date()
        ).order_by('scheduled_date')


class WebinarDetailView(DetailView):
    """Webinar details"""
    model = Webinar
    template_name = 'advisory/webinar_detail.html'
    context_object_name = 'webinar'


class RegisterWebinarView(LoginRequiredMixin, View):
    """Register for webinar"""
    
    def post(self, request, pk):
        webinar = get_object_or_404(Webinar, pk=pk)
        
        if webinar.is_full:
            messages.error(request, 'This webinar is full.')
            return redirect('advisory:webinar_detail', pk=pk)
        
        webinar.registered_users.add(request.user)
        messages.success(request, 'Successfully registered for the webinar!')
        return redirect('advisory:webinar_detail', pk=pk)


class ConsultationListView(LoginRequiredMixin, ListView):
    """List user's consultations"""
    model = ExpertConsultation
    template_name = 'advisory/consultation_list.html'
    context_object_name = 'consultations'
    
    def get_queryset(self):
        return ExpertConsultation.objects.filter(
            farmer=self.request.user
        ).order_by('-created_at')


class BookConsultationView(LoginRequiredMixin, CreateView):
    """Book expert consultation"""
    model = ExpertConsultation
    form_class = ConsultationBookingForm
    template_name = 'advisory/book_consultation.html'
    success_url = '/advisory/consultations/'
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        messages.success(
            self.request,
            'Consultation request submitted. We will contact you shortly.'
        )
        return super().form_valid(form)


class TeleVetListView(LoginRequiredMixin, ListView):
    """List tele-vet consultations"""
    model = TeleVetConsultation
    template_name = 'advisory/tele_vet_list.html'
    context_object_name = 'consultations'
    
    def get_queryset(self):
        return TeleVetConsultation.objects.filter(
            farmer=self.request.user
        ).order_by('-created_at')


class TeleVetConsultView(LoginRequiredMixin, CreateView):
    """Request tele-vet consultation"""
    model = TeleVetConsultation
    form_class = TeleVetConsultationForm
    template_name = 'advisory/tele_vet_consult.html'
    success_url = '/advisory/tele-vet/'
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        messages.success(
            self.request,
            'Veterinary consultation request submitted. A vet will review and respond.'
        )
        return super().form_valid(form)


class FAQListView(ListView):
    """List FAQs"""
    model = FAQ
    template_name = 'advisory/faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        queryset = FAQ.objects.filter(is_published=True)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = AdvisoryCategory.objects.all()
        return context


class TipsView(ListView):
    """Farming tips"""
    model = FarmingTip
    template_name = 'advisory/tips.html'
    context_object_name = 'tips'
    paginate_by = 10
    
    def get_queryset(self):
        from datetime import date
        return FarmingTip.objects.filter(
            display_date__lte=date.today(),
            is_active=True
        ).order_by('-display_date')
