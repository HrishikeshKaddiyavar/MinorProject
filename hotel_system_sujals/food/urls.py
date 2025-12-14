from django.urls import path
from . import views

urlpatterns = [
    # Login/Logout
    path('', views.login_view, name='login'),
    path('admin_login', views.admin_chef_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Customer
    path('customer/', views.customer_view, name='customer_view'),
    path('customer/add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('customer/update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('customer/place_order/', views.place_order, name='place_order'),
    
    # Kitchen
    path('kitchen/', views.kitchen_view, name='kitchen_view'),
    path('kitchen/update_status/<int:order_id>/', views.update_kitchen_status, name='update_kitchen_status'),
    
    # Admin
    path('dashboard/', views.admin_view, name='admin_view'),
    path('dashboard/menu/add/', views.add_edit_menu_item, name='add_menu_item'),
    path('dashboard/menu/edit/<int:item_id>/', views.add_edit_menu_item, name='edit_menu_item'),
    path('dashboard/menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('dashboard/order/update_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]