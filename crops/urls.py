from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    # Crops
    path('', views.CropListView.as_view(), name='crop_list'),
    path('<int:pk>/', views.CropDetailView.as_view(), name='crop_detail'),
    path('my-crops/', views.MyCropsView.as_view(), name='my_crops'),
    path('my-crops/add/', views.FarmerCropCreateView.as_view(), name='add_crop'),
    path('my-crops/<int:pk>/update/', views.FarmerCropUpdateView.as_view(), name='update_crop'),
    path('my-crops/<int:pk>/delete/', views.FarmerCropDeleteView.as_view(), name='delete_crop'),
    
    # Planting Calendar
    path('planting-calendar/', views.PlantingCalendarView.as_view(), name='planting_calendar'),
    path('planting-calendar/<str:region>/', views.RegionalCalendarView.as_view(), name='regional_calendar'),
    
    # Pest & Disease
    path('pests-diseases/', views.PestDiseaseListView.as_view(), name='pest_disease_list'),
    path('pests-diseases/<int:pk>/', views.PestDiseaseDetailView.as_view(), name='pest_disease_detail'),
    path('detect/', views.PestDiseaseDetectView.as_view(), name='detect'),
    path('detections/', views.MyDetectionsView.as_view(), name='my_detections'),
    
    # Livestock
    path('livestock/', views.LivestockListView.as_view(), name='livestock_list'),
    path('livestock/add/', views.LivestockCreateView.as_view(), name='add_livestock'),
    path('livestock/<int:pk>/', views.LivestockDetailView.as_view(), name='livestock_detail'),
    path('livestock/<int:pk>/edit/', views.LivestockUpdateView.as_view(), name='edit_livestock'),
    path('livestock/<int:pk>/delete/', views.LivestockDeleteView.as_view(), name='delete_livestock'),
    path('livestock/<int:pk>/production/', views.AddProductionView.as_view(), name='add_production'),
]
