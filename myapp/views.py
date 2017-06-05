from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post # import our Post to views

# Create your views here.
# 'request' is everything we receive from user via internet
# 'myapp/post_list.html' is giving template file; {} is a place in which we can add some things for the template to use

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myapp/post_list.html', {'posts': posts})
	
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'myapp/post_detail.html', {'post': post})