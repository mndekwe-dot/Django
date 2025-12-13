from django.shortcuts import render
from django.db.models import Value , F , Func, Count
from store.models import Product , Customer
from tags.models import TaggedItem

# Create your views here.
def say_hello(request):
    taggedItems = TaggedItem.objects.get_tags_for(Product, 1)
    return render(request, "Hello.html", {"name":"Merci","product":product})