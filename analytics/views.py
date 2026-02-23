from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Sum, Avg, Count, F
from django.utils import timezone
from datetime import datetime, timedelta

from farmers.models import FarmerProfile, FarmingHistory
from marketplace.models import Transaction
from .models import FarmerAnalytics, MarketTrend


class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    """Main analytics dashboard"""
    template_name = 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            profile = user.farmer_profile
        except:
            profile = None
        
        if profile:
            # Yield data
            current_year = timezone.now().year
            
            context['total_yield'] = FarmingHistory.objects.filter(
                farmer_profile=profile,
                year=current_year,
                actual_yield__isnull=False
            ).aggregate(total=Sum('actual_yield'))['total'] or 0
            
            # Revenue
            context['total_revenue'] = FarmingHistory.objects.filter(
                farmer_profile=profile,
                year=current_year,
                total_revenue__isnull=False
            ).aggregate(total=Sum('total_revenue'))['total'] or 0
            
            # Profit
            context['total_profit'] = FarmingHistory.objects.filter(
                farmer_profile=profile,
                year=current_year,
                total_revenue__isnull=False,
                total_cost__isnull=False
            ).aggregate(
                profit=Sum(F('total_revenue') - F('total_cost'))
            )['profit'] or 0
            
            # Top crops
            context['top_crops'] = FarmingHistory.objects.filter(
                farmer_profile=profile,
                year=current_year
            ).values('crop_name').annotate(
                total_yield=Sum('actual_yield')
            ).order_by('-total_yield')[:5]
            
            # Monthly data for charts
            context['monthly_data'] = self.get_monthly_data(profile, current_year)
        
        return context
    
    def get_monthly_data(self, profile, year):
        """Get monthly yield and revenue data"""
        data = []
        for month in range(1, 13):
            month_data = FarmingHistory.objects.filter(
                farmer_profile=profile,
                year=year,
                planting_date__month=month
            ).aggregate(
                yield_total=Sum('actual_yield'),
                revenue_total=Sum('total_revenue')
            )
            data.append({
                'month': month,
                'yield': float(month_data['yield_total'] or 0),
                'revenue': float(month_data['revenue_total'] or 0)
            })
        return data


class YieldAnalyticsView(LoginRequiredMixin, TemplateView):
    """Yield analytics view"""
    template_name = 'analytics/yield.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            profile = user.farmer_profile
        except:
            profile = None
        
        if profile:
            # Yield by crop
            context['yield_by_crop'] = FarmingHistory.objects.filter(
                farmer_profile=profile,
                actual_yield__isnull=False
            ).values('crop_name').annotate(
                total_yield=Sum('actual_yield'),
                avg_yield=Avg('actual_yield'),
                count=Count('id')
            ).order_by('-total_yield')
            
            # Yield by year
            context['yield_by_year'] = FarmingHistory.objects.filter(
                farmer_profile=profile,
                actual_yield__isnull=False
            ).values('year').annotate(
                total_yield=Sum('actual_yield')
            ).order_by('year')
            
            # Yield by parcel
            context['yield_by_parcel'] = FarmingHistory.objects.filter(
                farmer_profile=profile,
                parcel__isnull=False,
                actual_yield__isnull=False
            ).values('parcel__parcel_name').annotate(
                total_yield=Sum('actual_yield')
            ).order_by('-total_yield')
        
        return context


class ProfitabilityView(LoginRequiredMixin, TemplateView):
    """Profitability analysis"""
    template_name = 'analytics/profitability.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            profile = user.farmer_profile
        except:
            profile = None
        
        if profile:
            # Profit by crop
            context['profit_by_crop'] = FarmingHistory.objects.filter(
                farmer_profile=profile,
                total_revenue__isnull=False,
                total_cost__isnull=False
            ).values('crop_name').annotate(
                total_revenue=Sum('total_revenue'),
                total_cost=Sum('total_cost'),
                profit=Sum(F('total_revenue') - F('total_cost'))
            ).order_by('-profit')
            
            # ROI by crop
            for item in context['profit_by_crop']:
                if item['total_cost'] > 0:
                    item['roi'] = (item['profit'] / item['total_cost']) * 100
                else:
                    item['roi'] = 0
            
            # Cost breakdown
            context['total_costs'] = FarmingHistory.objects.filter(
                farmer_profile=profile
            ).aggregate(total=Sum('total_cost'))['total'] or 0
        
        return context


class MarketTrendsView(LoginRequiredMixin, TemplateView):
    """Market trends view"""
    template_name = 'analytics/market_trends.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Recent market trends
        context['trends'] = MarketTrend.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).order_by('-price_change_percentage')[:20]
        
        # Top gaining products
        context['top_gainers'] = MarketTrend.objects.filter(
            price_change_percentage__gt=0
        ).order_by('-price_change_percentage')[:5]
        
        # Top losing products
        context['top_losers'] = MarketTrend.objects.filter(
            price_change_percentage__lt=0
        ).order_by('price_change_percentage')[:5]
        
        return context


class FarmPerformanceView(LoginRequiredMixin, TemplateView):
    """Farm performance comparison"""
    template_name = 'analytics/farm_performance.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            profile = user.farmer_profile
        except:
            profile = None
        
        if profile:
            # Performance metrics
            current_year = timezone.now().year
            
            context['yield_per_acre'] = self.calculate_yield_per_acre(profile, current_year)
            context['revenue_per_acre'] = self.calculate_revenue_per_acre(profile, current_year)
            
            # Comparison with previous year
            prev_year = current_year - 1
            
            current_yield = FarmingHistory.objects.filter(
                farmer_profile=profile,
                year=current_year,
                actual_yield__isnull=False
            ).aggregate(total=Sum('actual_yield'))['total'] or 0
            
            previous_yield = FarmingHistory.objects.filter(
                farmer_profile=profile,
                year=prev_year,
                actual_yield__isnull=False
            ).aggregate(total=Sum('actual_yield'))['total'] or 0
            
            if previous_yield > 0:
                context['yield_growth'] = ((current_yield - previous_yield) / previous_yield) * 100
            else:
                context['yield_growth'] = 0
        
        return context
    
    def calculate_yield_per_acre(self, profile, year):
        total_yield = FarmingHistory.objects.filter(
            farmer_profile=profile,
            year=year,
            actual_yield__isnull=False
        ).aggregate(total=Sum('actual_yield'))['total'] or 0
        
        total_area = FarmingHistory.objects.filter(
            farmer_profile=profile,
            year=year,
            area_planted__isnull=False
        ).aggregate(total=Sum('area_planted'))['total'] or 1
        
        return total_yield / total_area if total_area > 0 else 0
    
    def calculate_revenue_per_acre(self, profile, year):
        total_revenue = FarmingHistory.objects.filter(
            farmer_profile=profile,
            year=year,
            total_revenue__isnull=False
        ).aggregate(total=Sum('total_revenue'))['total'] or 0
        
        total_area = FarmingHistory.objects.filter(
            farmer_profile=profile,
            year=year,
            area_planted__isnull=False
        ).aggregate(total=Sum('area_planted'))['total'] or 1
        
        return total_revenue / total_area if total_area > 0 else 0


class ReportsView(LoginRequiredMixin, TemplateView):
    """Reports view"""
    template_name = 'analytics/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Available reports
        context['reports'] = [
            {
                'name': 'Annual Production Report',
                'description': 'Complete production summary for the year',
                'icon': 'chart-bar'
            },
            {
                'name': 'Financial Statement',
                'description': 'Revenue, costs, and profit analysis',
                'icon': 'currency-dollar'
            },
            {
                'name': 'Crop Performance Report',
                'description': 'Detailed analysis by crop type',
                'icon': 'seedling'
            },
            {
                'name': 'Market Price Report',
                'description': 'Price trends and market analysis',
                'icon': 'trending-up'
            },
        ]
        
        return context


class AnalyticsDataAPIView(LoginRequiredMixin, View):
    """API endpoint for analytics data"""
    
    def get(self, request):
        metric = request.GET.get('metric')
        
        if metric == 'yield_by_month':
            return self.get_yield_by_month(request)
        elif metric == 'revenue_by_crop':
            return self.get_revenue_by_crop(request)
        elif metric == 'cost_breakdown':
            return self.get_cost_breakdown(request)
        
        return JsonResponse({'error': 'Unknown metric'}, status=400)
    
    def get_yield_by_month(self, request):
        user = request.user
        year = int(request.GET.get('year', timezone.now().year))
        
        try:
            profile = user.farmer_profile
        except:
            return JsonResponse({'data': []})
        
        data = []
        for month in range(1, 13):
            total = FarmingHistory.objects.filter(
                farmer_profile=profile,
                year=year,
                planting_date__month=month,
                actual_yield__isnull=False
            ).aggregate(total=Sum('actual_yield'))['total'] or 0
            
            data.append({
                'month': month,
                'yield': float(total)
            })
        
        return JsonResponse({'data': data})
    
    def get_revenue_by_crop(self, request):
        user = request.user
        year = int(request.GET.get('year', timezone.now().year))
        
        try:
            profile = user.farmer_profile
        except:
            return JsonResponse({'data': []})
        
        data = list(FarmingHistory.objects.filter(
            farmer_profile=profile,
            year=year,
            total_revenue__isnull=False
        ).values('crop_name').annotate(
            revenue=Sum('total_revenue')
        ).order_by('-revenue'))
        
        return JsonResponse({'data': data})
    
    def get_cost_breakdown(self, request):
        user = request.user
        year = int(request.GET.get('year', timezone.now().year))
        
        try:
            profile = user.farmer_profile
        except:
            return JsonResponse({'data': []})
        
        # This is simplified - in reality you'd have detailed cost categories
        data = {
            'labels': ['Seeds', 'Fertilizers', 'Pesticides', 'Labor', 'Other'],
            'data': [30, 25, 15, 20, 10]  # Percentage breakdown
        }
        
        return JsonResponse(data)
