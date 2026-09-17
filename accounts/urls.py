from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('product/', views.product, name='product'),
    path('customer/<int:pk>/', views.customer, name='customer'),
    
    path('create_order/<int:pk>/', views.createOrder, name='create_order'),
    path('update_order/<int:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<int:pk>/', views.deleteOrder, name='delete_order'),

    path('create_customer/', views.createCustomer, name='create_customer'),
    path('update_customer/<int:pk>/', views.updateCustomer, name='update_customer'),
    path('delete_customer/<int:pk>/', views.deleteCustomer, name='delete_customer'),

]
