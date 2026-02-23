from django.contrib import admin
from .models import (
    AdvisoryCategory, AdvisoryArticle, Webinar,
    ExpertConsultation, FAQ, FarmingTip, TeleVetConsultation
)


@admin.register(AdvisoryCategory)
class AdvisoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(AdvisoryArticle)
class AdvisoryArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'language', 'is_published', 'published_at']
    list_filter = ['category', 'language', 'is_published']
    search_fields = ['title', 'content']
    date_hierarchy = 'published_at'


@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ['title', 'presenter', 'scheduled_date', 'status']
    list_filter = ['status', 'platform']
    date_hierarchy = 'scheduled_date'


@admin.register(ExpertConsultation)
class ExpertConsultationAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'topic', 'status', 'created_at']
    list_filter = ['status', 'category']
    date_hierarchy = 'created_at'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_published', 'view_count']
    list_filter = ['is_published']
    search_fields = ['question', 'answer']


@admin.register(FarmingTip)
class FarmingTipAdmin(admin.ModelAdmin):
    list_display = ['tip', 'display_date', 'is_active']
    list_filter = ['is_active']
    date_hierarchy = 'display_date'


@admin.register(TeleVetConsultation)
class TeleVetConsultationAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'animal_species', 'status', 'created_at']
    list_filter = ['status', 'animal_species']
    date_hierarchy = 'created_at'
