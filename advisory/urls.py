from django.urls import path
from . import views

app_name = 'advisory'

urlpatterns = [
    # Articles
    path('', views.AdvisoryHomeView.as_view(), name='home'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    
    # Webinars
    path('webinars/', views.WebinarListView.as_view(), name='webinar_list'),
    path('webinars/<int:pk>/', views.WebinarDetailView.as_view(), name='webinar_detail'),
    path('webinars/<int:pk>/register/', views.RegisterWebinarView.as_view(), name='register_webinar'),
    
    # Consultations
    path('consultations/', views.ConsultationListView.as_view(), name='consultation_list'),
    path('consultations/book/', views.BookConsultationView.as_view(), name='book_consultation'),
    
    # Tele-Vet
    path('tele-vet/', views.TeleVetListView.as_view(), name='tele_vet_list'),
    path('tele-vet/consult/', views.TeleVetConsultView.as_view(), name='tele_vet_consult'),
    
    # FAQ
    path('faq/', views.FAQListView.as_view(), name='faq'),
    
    # Tips
    path('tips/', views.TipsView.as_view(), name='tips'),
]
