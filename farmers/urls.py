from django.urls import path
from . import views

app_name = 'farmers'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.FarmerDashboardView.as_view(), name='dashboard'),
    
    # Profile Management
    path('profile/', views.FarmerProfileView.as_view(), name='profile'),
    path('profile/edit/', views.FarmerProfileEditView.as_view(), name='profile_edit'),
    path('profile/complete/', views.CompleteProfileView.as_view(), name='complete_profile'),
    
    # Farm Parcels
    path('parcels/', views.FarmParcelListView.as_view(), name='parcel_list'),
    path('parcels/add/', views.FarmParcelCreateView.as_view(), name='parcel_add'),
    path('parcels/<int:pk>/', views.FarmParcelDetailView.as_view(), name='parcel_detail'),
    path('parcels/<int:pk>/edit/', views.FarmParcelUpdateView.as_view(), name='parcel_edit'),
    path('parcels/<int:pk>/delete/', views.FarmParcelDeleteView.as_view(), name='parcel_delete'),
    
    # Farming History
    path('history/', views.FarmingHistoryListView.as_view(), name='history_list'),
    path('history/add/', views.FarmingHistoryCreateView.as_view(), name='history_add'),
    path('history/<int:pk>/edit/', views.FarmingHistoryUpdateView.as_view(), name='history_edit'),
    
    # Crop Rotation Planner
    path('rotation-planner/', views.CropRotationPlannerView.as_view(), name='rotation_planner'),
    
    # GPS Mapping
    path('map-farm/', views.FarmMappingView.as_view(), name='map_farm'),
    path('api/save-boundary/', views.SaveFarmBoundaryView.as_view(), name='save_boundary'),
    
    # KIAMIS Integration
    path('kiamis/sync/', views.KIAMISSyncView.as_view(), name='kiamis_sync'),
    
    # Credit Score
    path('credit-score/', views.CreditScoreView.as_view(), name='credit_score'),
]
