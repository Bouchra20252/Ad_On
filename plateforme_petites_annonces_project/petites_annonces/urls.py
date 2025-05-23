from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='petites_annonces/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='petites_annonces/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='petites_annonces/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='petites_annonces/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Advertisements
    path('ad/new/', views.advertisement_create, name='ad-create'),
    path('ad/<slug:slug>/', views.AdvertisementDetailView.as_view(), name='ad-detail'),
    path('ad/<slug:slug>/update/', views.advertisement_update, name='ad-update'),
    path('ad/<slug:slug>/delete/', views.advertisement_delete, name='ad-delete'),
    
    # Search and favorites
    path('search/', views.search_results, name='search'),
    path('save-search/', views.save_search, name='save-search'),
    path('delete-search/<int:pk>/', views.delete_saved_search, name='delete-search'),
    path('toggle-favorite/<slug:slug>/', views.toggle_favorite, name='toggle-favorite'),
    
    # Comments and reports
    path('ad/<slug:slug>/comment/', views.add_comment, name='add-comment'),
    path('ad/<slug:slug>/report/', views.report_ad, name='report-ad'),
    
    # Messaging
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation-detail'),
    path('new-message/<int:user_id>/', views.new_message, name='new-message'),
    path('new-message/<int:user_id>/<slug:ad_slug>/', views.new_message, name='new-message-ad'),
    
    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('moderate-ad/<int:pk>/<str:action>/', views.moderate_ad, name='moderate-ad'),
    path('moderate-report/<int:pk>/', views.moderate_report, name='moderate-report'),
    
    # User ads
    path('user/<str:username>/ads/', views.user_ads, name='user-ads'),
] 