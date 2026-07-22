from django.shortcuts import render, redirect
from .models import Blog, Post
from .forms import BlogForm, PostForm

# view queries the database and pass that data to an HTML template.

def index(request):
    """The home page showing all posts."""
    blogs = Blog.objects.order_by('-date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/index.html', context)

def new_blog(request):
    """Add a new Blog."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BlogForm()
    else:
        # POST data submitted; process data.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            form.save()
        return redirect('blogs:index')
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)

def new_post(request, blog_id): # blog_id is coming from urls.py --> int:<blog_id> part
    "Add a new Post for a particular Blog."
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
        # No data submitted; create a blank form
        form = PostForm()
    else:
        # POST data submitted; process data.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blogs:blog', blog_id=blog_id) # we didn't passed any extra arguments cause index
            # is the home page and it doesn't require one.
        
    # Display a blank or invalid form.
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_post.html', context)

def edit_post(request, post_id):
    """Edit an existing post."""
    # Fetch the specific post and its associated blog
    post = Post.objects.get(id=post_id)
    blog = post.blog

    if request.method != 'POST':
        # Initial request; pre-fill the form with the current post's data
        form = PostForm(instance=post)
    else:
        # POST data submitted; process the data and update the specific instance
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            # Redirect back to the blog page using the blog's ID
            return redirect('blogs:blog', blog_id=blog.id)

    # Package the context and render the template
    context = {'post': post, 'blog': blog, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

def blog(request, blog_id):
    """The blog page showing all the posts made on a blog."""
    blog = Blog.objects.get(id=blog_id)
    # Fetch all posts related to this specific blog
    posts = blog.post_set.all() 
    # Package the data
    context = {'blog': blog, 'posts': posts}
    # Send to the template
    return render(request, 'blogs/blog.html', context)