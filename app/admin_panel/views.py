from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
from users.forms import UserRegistrationForm, ProfileForm
from goods.models import Categories, Products
from carts.models import Cart
from orders.models import Order, OrderItem
from goods.forms import CategoryForm, ProductForm
from orders.forms import OrderForm, OrderItemForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponseForbidden


def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden("У вас нет доступа к этой панели.")
    return render(request, 'admin_panel/dashboard.html')


# *****************************Пользователи
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_panel/users_list.html', {'users': users})


# Создание нового пользователя
def user_create(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь был успешно создан.')
            return redirect('admin_panel:users_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'admin_panel/user_form.html', {'form': form, 'action': 'Создать'})


# Обновление пользователя
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о пользователе обновлена.')
            return redirect('admin_panel:users_list')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'admin_panel/user_form.html', {'form': form, 'action': 'Редактировать', 'user': user})


# Удаление пользователя
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь был удален.')
        return redirect('admin_panel:users_list')
    return render(request, 'admin_panel/user_confirm_delete.html', {'user': user})


# *****************************Товары

def categories_list(request):
    categories = Categories.objects.all()
    return render(request, 'admin_panel/categories_list.html', {'categories': categories})


def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:categories_list')
    else:
        form = CategoryForm()
    return render(request, 'admin_panel/category_form.html', {'form': form})


def category_edit(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:categories_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin_panel/category_form.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if category.products.exists():
        messages.error(request, "You cannot delete this category because it has products.")
        return redirect('admin_panel:categories_list')
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('admin_panel:categories_list')
    return render(request, 'admin_panel/category_confirm_delete.html', {'object': category})


def products_list(request):
    products = Products.objects.select_related('category').all()
    return render(request, 'admin_panel/products_list.html', {'products': products})


def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:products_list')
    else:
        form = ProductForm()
    return render(request, 'admin_panel/product_form.html', {'form': form})


def product_edit(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:products_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_panel/product_form.html', {'form': form})


def product_delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_panel:products_list')
    return render(request, 'admin_panel/product_confirm_delete.html', {'object': product})


# ****************Корзина
def cart_detail(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key)

    total_price = cart_items.total_price()

    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_item, created = Cart.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    return redirect('cart:detail')


def remove_from_cart(request, cart_id):
    try:
        cart_item = get_object_or_404(Cart, pk=cart_id)
        cart_item.delete()
    except Cart.DoesNotExist:
        return redirect('cart:detail')
    return redirect('cart:detail')


#  ***********************Заказы
def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'admin_panel/orders_list.html', {'orders': orders})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, 'admin_panel/order_detail.html', {'order': order, 'order_items': order_items})


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Заказ успешно создан!')
            return redirect('admin_panel:order_detail', order.pk)
    else:
        form = OrderForm()
    return render(request, 'admin_panel/order_form.html', {'form': form})


def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно обновлен!')
            return redirect('admin_panel:order_detail', order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'admin_panel/order_form.html', {'form': form})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заказ успешно удален!')
        return redirect('admin_panel:orders_list')
    return render(request, 'admin_panel/order_confirm_delete.html', {'order': order})


def order_item_create(request, order_pk, item_pk=None):
    order = get_object_or_404(Order, pk=order_pk)
    if item_pk:
        order_item = get_object_or_404(OrderItem, pk=item_pk)
    else:
        order_item = None

    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
            messages.success(request, 'Товар был успешно добавлен в заказ.')
            return redirect('admin_panel:order_detail', pk=order.pk)
    else:
        form = OrderItemForm()

    return render(request, 'admin_panel/order_item_form.html', {'form': form, 'order': order, 'action': 'Добавить товар'})


def order_item_edit(request, order_pk, item_pk):
    order = get_object_or_404(Order, pk=order_pk)
    item = get_object_or_404(OrderItem, pk=item_pk, order=order)

    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар был успешно обновлен.')
            return redirect('admin_panel:order_detail', pk=order.pk)
    else:
        form = OrderItemForm(instance=item)

    return render(request, 'admin_panel/order_item_form.html', {'form': form, 'order': order, 'action': 'Редактировать товар'})


def order_item_delete(request, order_pk, item_pk):
    order = get_object_or_404(Order, pk=order_pk)
    item = get_object_or_404(OrderItem, pk=item_pk, order=order)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Товар был успешно удален.')
        return redirect('admin_panel:order_detail', pk=order.pk)

    return render(request, 'admin_panel/order_item_confirm_delete.html', {'item': item})