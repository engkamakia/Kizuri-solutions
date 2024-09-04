from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.index, name = "home"),
    #path('about/', views.about_us, name = "about"),
    path('contact/', views.contact, name = "contact"),
    path('dashboard/', views.client_info_view, name = "dashboard"),
    path('client/', views.client_submission_form, name='client'),
    path('guarantor/<str:loan_id>/', views.guarantor_view, name='guarantor'),
    #path('user/<int:user_id>/', views.user_profile, name='user_profile'),   
    #path('payment/', views.make_payment, name = "payment"),
    #path('initiate/', views.initiate_stk_push, name='initiate'),
    #path('access/token', views.get_access_token, name='get_mpesa_access_token'),
    #path('query/', views.query_stk_status, name='query_stk_status'),
    #path('callback', views.process_stk_callback, name='mpesa_callback'),
    #path('transaction/', views.mpesa_payment, name='transaction'),
    path('profile/<str:client_id>', views.client_profile, name='client_profile'),
    path('login/', views.sign_in, name = "login"),
    path('registration/', views.sign_up, name = "registration"),
    path('logout/', views.logoutUser, name = "logout"),
    
    
]