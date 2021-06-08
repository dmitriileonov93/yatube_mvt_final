from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import only_author
from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User

posts_on_page = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, posts_on_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, })


@login_required
def follow_index(request):
    request_user = request.user
    post_list = Post.objects.filter(author__following__user=request_user)
    paginator = Paginator(post_list, posts_on_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page': page, })


@login_required
def profile_follow(request, username):
    user = request.user
    if user.username == username:
        return redirect('profile', username)
    following_author = User.objects.get(username=username)
    Follow.objects.get_or_create(user=user,
                                 author=following_author)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    unfollowing_author = User.objects.get(username=username)
    Follow.objects.get(user=user,
                       author=unfollowing_author).delete()
    return redirect('profile', username)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    if ((request.user.is_anonymous)
       or (author not in User.objects.filter(following__user=request.user))):
        following = False
    else:
        following = True
    post_list = author.posts.all()
    paginator = Paginator(post_list, posts_on_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'author': author,
                                            'page': page,
                                            'following': following})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()
    paginator = Paginator(posts, posts_on_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    author = post.author
    if ((request.user.is_anonymous)
       or (author not in User.objects.filter(following__user=request.user))):
        following = False
    else:
        following = True
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    return render(request, 'post.html', {'author': author,
                                         'post': post,
                                         'comments': comments,
                                         'form': form,
                                         'following': following})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('post', username, post_id)
    return render(request, 'post.html', {'author': post.author,
                                         'post': post,
                                         'form': form})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'new_post.html', {'form': form})


@login_required
@only_author
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post', username, post_id)
    return render(request, 'new_post.html', {'form': form, 'post': post})


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
