from django.shortcuts import render, get_object_or_404, redirect
from .models import Item,Order,OrderItem
from django.views.generic import ListView,DetailView
from django.utils import timezone


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"


class ItemDetailView(DetailView): # in class based DetailView,it needs slug or pk,which came from urls.py file,if you using slug then you define this in mdoel
    model = Item
    template_name = "product-page.html"


def checkout(request):
    return render(request,"checkout-page.html")


def add_to_cart(request,slug): # here for add to cart we need the parameter slug
    # take the current item using the slug
    item = get_object_or_404(Item,slug=slug) # take the product from Item model use slug for matching,and store it to the item variable
    # create a instance of OrderItem class
    order_item = OrderItem.objects.create(item=item) # now create a instance of OrderItem class which is place to be order
    # using filter for check the current user and check that this is not ordered already
    order_qs = Order.objects.filter(user=request.user,ordered=False) # using filter method for checking where user of the order is current user(request.user) or not and ordered=false means this particular product are not ordered previously
    # if the order_qs is true then take the first value of order_qs list
    # when you wants to order more than one item
    if order_qs.exists():  # exist means order_qs already in database, it checks if the order_qs is true then take the first value of list
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists(): # it means if the order item is already exists in cart then add one more in oreder_item,if order's slug (which is ordered) is same as item's slug then we increase quantity of order_item(which is instance of OrderItem class),here item is the instance of Item class
            order_item.quantity += 1 # if user wants to order multiple item then add the quantity
            order_item.save()

    else:  # in first time you order a item
        ordered_date = timezone.now() # take the ordered_date and set this
        order = Order.objects.create(user=request.user,ordered_date=ordered_date) # create a instance of order class
        order.items.add(order_item) # add the order_item in items field in order instance
    return redirect("core:product", slug= slug) # here order objects create two parameter which is user and ordered_date,so we can't kwargs for passing parameter, in product url it needs slug parameter

'''
def products(request):
    return render(request,"product-page.html")

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request,"home-page.html",context)
'''