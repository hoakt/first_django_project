from django.shortcuts import render
from django.utils import timezone
from .models import Post # import Post to views

# Create your views here.
# 'request' is everything we receive from user via internet
# 'myapp/post_list.html' is giving template file; {} is a place in which we can add some things for the template to use

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myapp/post_list.html', {'posts': posts})