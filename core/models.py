from django.db import models
from django.conf import settings


# here create a tuple,where left side is from database(admin page) and right side is show in page
from django.urls import reverse

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)
# here create another tuple where left side shows from database(admin page) and right side show in html page
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model): # this class shows the item of E commerce
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2) # take the category value from 'CATEGORY_CHOICES' tuple
    label = models.CharField(choices=LABEL_CHOICES,max_length=1) # take the label from 'LABEL_CHOICES' tuple
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self): # string representation of this model
        return self.title

    def get_absolute_url(self):
        return reverse("core:product",kwargs={ # if we use args then we write only 'slug',don't need a dictionary
            'slug': self.slug   # we can use kwargs or args for passing the parameter,when we use detail view,then we have to pass slug as parameter,because in urls.py file we declare the slug which one comes from user
        })

    def get_add_to_cart_url(self):
        return reverse("core:product",kwargs={
            'slug': self.slug
        })

# in OrderItem class here we track how many order item we order
class OrderItem(models.Model): # this class is using for which items wants to buy by user
    item = models.ForeignKey(Item,on_delete=models.CASCADE) # this one using fk relation with Item,it is intermidiary between Item and order class
    quantity = models.IntegerField(default=1) # this field counts how much item you ordered,keep tracking

    def __str__(self):
        return f"{self.quantity} of {self.item.title}" # here item is the fk of Item , show the quantity of each item and show the item(which is fk here) title(item has title)


class Order(models.Model): # this class shows the product which one order by user and it's add into the cart
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) # user is the fk relation with User,which means user is have to a current registered user
    items = models.ManyToManyField(OrderItem) # it links with OrderItem class,the items which one wants to order its must be include in OrderItem class
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField() # we don't need to use auto_now_add here
    ordered = models.BooleanField() # it shows ordered or not

    def __str__(self):
        return self.user.username # username is build in django field
