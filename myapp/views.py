from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment # import our Post, Comment model to views
from .forms import PostForm, CommentForm # import our form to views
from django.contrib.auth.decorators import login_required

# Create your views here.
# 'request' is everything we receive from user via internet
# 'myapp/post_list.html' is giving template file; {} is a place in which we can add some things for the template to use

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'myapp/post_list.html', {'posts': posts})
	
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'myapp/post_detail.html', {'post': post})
	
@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST) # new fields' data from new post are now in request.POST
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
#			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'myapp/post_edit.html', {'form': form})

@login_required	
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
#			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'myapp/post_edit.html', {'form': form})

@login_required	
def draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'myapp/draft_list.html', {'posts': posts})

@login_required	
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

@login_required	
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
	
def add_comment(request,pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST) # use CommentForm to create a form
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'myapp/add_comment_form.html', {'form': form})
	
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)