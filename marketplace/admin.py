from django.contrib import admin
from .models import (
    MarketPrice, ProduceListing, LivestockListing,
    BuyerInquiry, BuyerRequest, Transaction
)


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = [
        'product_name', 'market', 'average_price', 'unit', 'price_date'
    ]
    list_filter = ['market', 'category', 'price_date']
    search_fields = ['product_name']
    date_hierarchy = 'price_date'


@admin.register(ProduceListing)
class ProduceListingAdmin(admin.ModelAdmin):
    list_display = [
        'product_name', 'farmer', 'quantity_available', 'unit',
        'price_per_unit', 'quality_grade', 'status', 'created_at'
    ]
    list_filter = ['status', 'category', 'quality_grade', 'is_organic']
    search_fields = ['product_name', 'farmer__username', 'county']
    date_hierarchy = 'created_at'


@admin.register(LivestockListing)
class LivestockListingAdmin(admin.ModelAdmin):
    list_display = [
        'species', 'breed', 'farmer', 'quantity',
        'price_per_animal', 'status', 'created_at'
    ]
    list_filter = ['status', 'species']
    search_fields = ['breed', 'farmer__username', 'county']


@admin.register(BuyerInquiry)
class BuyerInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'listing', 'buyer', 'quantity_requested', 'status', 'created_at'
    ]
    list_filter = ['status']
    search_fields = ['listing__product_name', 'buyer__username']


@admin.register(BuyerRequest)
class BuyerRequestAdmin(admin.ModelAdmin):
    list_display = [
        'product_name', 'buyer', 'quantity_required', 'max_price_per_unit', 'status'
    ]
    list_filter = ['status', 'category']
    search_fields = ['product_name', 'buyer__username']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'product_name', 'farmer', 'buyer', 'total_amount',
        'payment_status', 'status', 'transaction_date'
    ]
    list_filter = ['status', 'payment_status', 'payment_method']
    search_fields = ['product_name', 'farmer__username', 'buyer__username']
    date_hierarchy = 'transaction_date'
