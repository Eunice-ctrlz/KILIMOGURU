from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Market prices
    path('prices/', views.MarketPriceListView.as_view(), name='prices'),
    path('prices/<str:market>/', views.MarketPriceByMarketView.as_view(), name='prices_by_market'),
    
    # Produce listings
    path('produce/', views.ProduceListingListView.as_view(), name='produce_list'),
    path('produce/create/', views.ProduceListingCreateView.as_view(), name='produce_create'),
    path('produce/<int:pk>/', views.ProduceListingDetailView.as_view(), name='produce_detail'),
    path('produce/<int:pk>/edit/', views.ProduceListingUpdateView.as_view(), name='produce_edit'),
    path('produce/<int:pk>/delete/', views.ProduceListingDeleteView.as_view(), name='produce_delete'),
    path('produce/<int:pk>/inquire/', views.BuyerInquiryCreateView.as_view(), name='inquire'),
    
    # Livestock listings
    path('livestock/', views.LivestockListingListView.as_view(), name='livestock_list'),
    path('livestock/create/', views.LivestockListingCreateView.as_view(), name='livestock_create'),
    path('livestock/<int:pk>/', views.LivestockListingDetailView.as_view(), name='livestock_detail'),
    
    # Buyer requests
    path('requests/', views.BuyerRequestListView.as_view(), name='request_list'),
    path('requests/create/', views.BuyerRequestCreateView.as_view(), name='request_create'),
    
    # Farmer's listings
    path('my-listings/', views.MyListingsView.as_view(), name='my_listings'),
    path('my-inquiries/', views.MyInquiriesView.as_view(), name='my_inquiries'),
    path('inquiries/<int:pk>/respond/', views.RespondInquiryView.as_view(), name='respond_inquiry'),
    
    # Transactions
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    
    # Buyer dashboard
    path('buyer/dashboard/', views.BuyerDashboardView.as_view(), name='buyer_dashboard'),
]
