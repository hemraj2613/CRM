from django.shortcuts import render, redirect
from .models import Product, Customer, Order
from .forms import OrderForm, CustomerForm

from django.forms import inlineformset_factory #create multiple fields to create in form 

# Create your views here.
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

def product(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product.html', context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders':total_orders,
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
        

        