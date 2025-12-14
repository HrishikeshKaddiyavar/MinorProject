from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum

from .models import MenuItem, Order, Category, OrderItem

# --- Helper Functions (Cart Management in Session) ---
def get_cart(request):
    """Retrieves the cart from the session."""
    return request.session.get('cart', {})

def save_cart(request, cart):
    """Saves the cart back to the session."""
    request.session['cart'] = cart

def get_cart_total(request):
    """Calculates the total price of items in the cart."""
    cart = get_cart(request)
    total = 0
    for item_id, item_data in cart.items():
        total += item_data['price'] * item_data['quantity']
    return total

# --- Role Simulation Views ---
def login_view(request):
    """Simulates the login screen."""
    if request.method == 'POST':
        role = request.POST.get('role')
        if role in ['customer', 'kitchen', 'admin']:
            request.session['user_role'] = role
            # Start a new cart for the customer session
            if role == 'customer':
                request.session['cart'] = {}
            if role == 'kitchen':
                return redirect('/admin_login')
            if role == 'admin':
                return redirect('/admin_login')
            return redirect(f'/{role}/') # Redirect to role-specific dashboard
    return render(request, 'food/login.html')

def admin_chef_login_view(request):
    context = {'login_verified' : True}
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'customer':
            return redirect('/customer/')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'chef' and password == 'chef123':
            return redirect('/kitchen/')
        
        if username == 'admin' and password == 'admin123':
            return redirect('/dashboard/')
        context = {'login_verified' : False}
    return render(request, 'food/admin_chef_login.html', context)

def logout_view(request):
    """Logs out the user."""
    if 'user_role' in request.session:
        del request.session['user_role']
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('login')

def check_role(request, required_role):
    """Decorator-like check for user role."""
    return request.session.get('user_role') == required_role

# --- Customer Views ---
def customer_view(request):
    if not check_role(request, 'customer'):
        return redirect('login')

    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', 'all')
    
    menu_items = MenuItem.objects.filter(available=True)
    
    if category_slug != 'all':
        menu_items = menu_items.filter(category__name=category_slug)
        
    if search_query:
        menu_items = menu_items.filter(name__icontains=search_query)

    context = {
        'menu_items': menu_items,
        'categories': Category.objects.all(),
        'selected_category': category_slug,
        'search_query': search_query,
        'cart': get_cart(request),
        'cart_total': get_cart_total(request),
    }
    return render(request, 'food/customer_view.html', context)

@require_POST
def add_to_cart(request, item_id):
    if not check_role(request, 'customer'):
        return redirect('login')
        
    menu_item = get_object_or_404(MenuItem, pk=item_id)
    cart = get_cart(request)
    item_id_str = str(item_id)

    if item_id_str in cart:
        cart[item_id_str]['quantity'] += 1
    else:
        cart[item_id_str] = {
            'id': menu_item.pk,
            'name': menu_item.name,
            'price': float(menu_item.price),
            'image': menu_item.image,
            'quantity': 1,
        }
        
    save_cart(request, cart)
    # Redirect back to the menu view
    return redirect(request.META.get('HTTP_REFERER', 'customer_view')) 

@require_POST
def update_cart(request, item_id):
    if not check_role(request, 'customer'):
        return redirect('login')
        
    action = request.POST.get('action')
    cart = get_cart(request)
    item_id_str = str(item_id)

    if item_id_str in cart:
        if action == 'increment':
            cart[item_id_str]['quantity'] += 1
        elif action == 'decrement':
            cart[item_id_str]['quantity'] -= 1
            if cart[item_id_str]['quantity'] <= 0:
                del cart[item_id_str]
        elif action == 'remove':
            del cart[item_id_str]
            
    save_cart(request, cart)
    return redirect('customer_view')

@require_POST
def place_order(request):
    if not check_role(request, 'customer'):
        return redirect('login')
        
    cart = get_cart(request)
    if not cart:
        return redirect('customer_view')

    # 1. Create the Order
    total = get_cart_total(request)
    order = Order.objects.create(total=total)

    # 2. Create the OrderItems
    for item_id_str, item_data in cart.items():
        menu_item = get_object_or_404(MenuItem, pk=item_data['id'])
        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=item_data['quantity'],
            price_at_order=item_data['price']
        )
        
    # 3. Clear the cart
    request.session['cart'] = {}
    
    # Simple success message redirect
    return redirect(f'/customer/?order_placed={order.order_id}')


# --- Kitchen Views ---
def kitchen_view(request):
    if not check_role(request, 'kitchen'):
        return redirect('login')
        
    # Get all orders that are not yet Delivered/Cancelled
    pending_orders = Order.objects.exclude(status__in=['Delivered', 'Cancelled']).order_by('-created_at')
    
    context = {
        'pending_orders': pending_orders
    }
    return render(request, 'food/kitchen_view.html', context)

@require_POST
def update_kitchen_status(request, order_id):
    if not check_role(request, 'kitchen'):
        return redirect('login')
        
    order = get_object_or_404(Order, pk=order_id)
    current_status = order.status
    
    if current_status == 'Pending':
        order.status = 'Preparing'
    elif current_status == 'Preparing':
        order.status = 'Ready'
        
    order.save()
    return redirect('kitchen_view')


# --- Admin Views ---
def admin_view(request):
    if not check_role(request, 'admin'):
        return redirect('login')
        
    total_sales = Order.objects.filter(status='Delivered').aggregate(Sum('total'))['total__sum'] or 0
    total_orders = Order.objects.count()
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    orders = Order.objects.all().order_by('-created_at')[:5] # Recent 5 orders

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'menu_items': menu_items,
        'recent_orders': orders,
        'categories': Category.objects.all(),
    }
    return render(request, 'food/admin_view.html', context)

# Add/Edit Item View (requires forms or manual processing for full functionality)
def add_edit_menu_item(request, item_id=None):
    if not check_role(request, 'admin'):
        return redirect('login')

    item = None
    if item_id:
        item = get_object_or_404(MenuItem, pk=item_id)

    if request.method == 'POST':
        # In a real app, use Django Forms for validation
        name = request.POST.get('name')
        category_name = request.POST.get('category')
        price = request.POST.get('price')
        image = request.POST.get('image')
        description = request.POST.get('description')
        available = request.POST.get('available') == 'on'

        category, created = Category.objects.get_or_create(name=category_name)

        if item:
            # Edit existing item
            item.name = name
            item.category = category
            item.price = price
            item.image = image
            item.description = description
            item.available = available
            item.save()
        else:
            # Add new item
            MenuItem.objects.create(
                name=name, category=category, price=price, image=image, 
                description=description, available=available
            )
        return redirect('admin_view')

    context = {
        'item': item,
        'categories': Category.objects.all(),
        # For the template to use the correct action URL
        'action_url': '/admin/menu/add/' if not item_id else f'/admin/menu/edit/{item_id}/'
    }
    return render(request, 'food/admin_menu_form.html', context)

@require_POST
def delete_menu_item(request, item_id):
    if not check_role(request, 'admin'):
        return redirect('login')
        
    item = get_object_or_404(MenuItem, pk=item_id)
    item.delete()
    return redirect('admin_view')

@require_POST
def update_order_status(request, order_id):
    if not check_role(request, 'admin'):
        return redirect('login')
        
    order = get_object_or_404(Order, pk=order_id)
    new_status = request.POST.get('status')
    if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
        order.status = new_status
        order.save()
    return redirect('admin_view')