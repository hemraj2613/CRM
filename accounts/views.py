from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users, unauthenticated_user

from accounts.decorators import unauthenticated_user
from accounts.filters import OrderFilter
from .models import Product, Customer, Order
from .forms import OrderForm, CustomerForm, CreateUserForm

from django.forms import inlineformset_factory #create multiple fields to create in form 

# Create your views here.
# register view
@unauthenticated_user
def register_view(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully!")
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


# login view
@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/')

        else:
            messages.error(request, "Invalid username or password.")

    context = {}
    return render(request, 'login.html', context)


# logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# home view
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    customers = Customer.objects.all()
    orders= Order.objects.all()

    total_orders = orders.count()

    total_customers = customers.count()

    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context = {
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
def product(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product.html', context)

@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    # filter by customer_order
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders':total_orders,
        'myFilter': myFilter,
    }
    return render(request, 'customer.html',context)


# create order
# def createOrder(request):
#     form = OrderForm()
#     # save to database after create data
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')

#     context = {
#         'form': form,
#     }
#     return render(request, 'order_form.html', context)


# create multiple fields for customer form
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=2)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    # form = OrderForm(initial={'customer': customer})

    # save to database after create data
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        # 'form': form,
        'formset': formset
    }
    return render(request, 'order_form.html', context)


# update order
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'order_form.html', context)


# delete order
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item': order,
    }
    return render(request, 'delete.html', context)


# createCustomer
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form' : form
    }
    return render(request, 'customer_form.html', context)

# update form
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    # else:
    #     form = CustomerForm()

    context = {
        'form': form,
    }

    return render(request, 'customer_form.html', context)


# deletecustomer
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')

    context = {
        'item': customer,
    }
    return render(request, 'delete_customer.html', context)
        




