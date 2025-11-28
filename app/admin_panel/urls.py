from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),

    # Пользователи
    path('admin-users/', views.user_list, name='users_list'),
    path('admin-users/create/', views.user_create, name='user_create'),
    path('admin-users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('admin-users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Категории
    path('admin-categories/', views.categories_list, name='categories_list'),
    path('admin-categories/add/', views.category_add, name='category_add'),
    path('admin-categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('admin-categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Товары
    path('admin-products/', views.products_list, name='products_list'),
    path('admin-products/add/', views.product_add, name='product_add'),
    path('admin-products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('admin-products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Корзина
    path('admin-cart/', views.cart_detail, name='detail'),
    path('admin-cart/add/<int:product_id>/', views.add_to_cart, name='add'),
    path('admin-cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove'),

    # Заказы
    path('admin-orders/', views.orders_list, name='orders_list'),
    path('admin-order/create/', views.order_create, name='order_create'),
    path('admin-order/<int:pk>/', views.order_detail, name='order_detail'),
    path('admin-order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('admin-order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('admin-order/<int:order_pk>/item/create/', views.order_item_create, name='order_item_create'),
    path('admin-order/<int:order_pk>/item/<int:item_pk>/edit/', views.order_item_edit, name='order_item_edit'),
    path('admin-order/<int:order_pk>/item/<int:item_pk>/delete/', views.order_item_delete, name='order_item_delete'),
]