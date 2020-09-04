from django.urls import path
from .views import checkout, HomeView,ItemDetailView,add_to_cart

app_name = 'core'
urlpatterns = [
    # path('',item_list,name='item_list'),
    path('',HomeView.as_view(),name='item_list'),
    # path('products/<int:pk>/',ItemDetailView.as_view(),name='products'),
    path('product/<slug:slug>',ItemDetailView.as_view(),name='product'), # here we use slug which one provides by django detailview
    path('checkout/',checkout,name='checkout'),
    # path('products/',products,name='product'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
]
