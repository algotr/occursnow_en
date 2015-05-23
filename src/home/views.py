from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from home.forms import PostForm
from .models import Post
from utils import constants


def index(request, form=None):
    if request.user.is_authenticated():
        post_form = form or PostForm()
        user = request.user
        posts_self = Post.objects.select_related().filter(user=user)
        posts_buddies = Post.objects.select_related().filter(user__userprofile__in=user.userprofile.follows.all)

        posts_list = posts_self | posts_buddies
        paginator = Paginator(posts_list, constants.PER_PAGE)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {'post_form': post_form, 'user': user, 'posts': posts, 'next': '/'}

        return render(request, 'home/index.html', context)
    else:
        posts_list = Post.objects.prefetch_related().all()
        paginator = Paginator(posts_list, constants.PER_PAGE)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context = {'posts': posts, 'next': '/'}
        return render(request, 'home/index.html', context)


@login_required()
def public_posts(request, form=None):
    post_form = form or PostForm()
    posts_list = Post.objects.select_related().all()
    user = request.user
    paginator = Paginator(posts_list, constants.PER_PAGE)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'title': _('الصفحة العامة'), 'post_form': post_form, 'user': user, 'posts': posts, 'next': '/public/'}

    return render(request, 'home/index.html', context)


@login_required()
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        next_url = request.POST.get('next', '/')
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                post.tags.add(tag.strip())
            post.save()
            return redirect(next_url)
        else:
            if 'public' in next_url:
                return public_posts(request, form)
            if 'user' in next_url:
                return user_page(request, request.user, form)
            return index(request, form)

    return redirect('home')


@login_required()
def del_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        success = "false"

        if request.user == post.user:
            post.rated_by.remove()
            post.delete()
            success = "success"

        if request.is_ajax():
            return HttpResponse(success)
        else:
            next_url = request.POST.get('next', '/')
            if len(next_url) == 0:
                next_url = '/'
            return redirect(next_url)


@login_required()
def users_list(request):
    current_user = request.user
    authors_list = User.objects.exclude(userprofile__in=current_user.userprofile.follows.all()) \
        .exclude(username=current_user.username).order_by('username')

    paginator = Paginator(authors_list, constants.PER_PAGE)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    next_url = reverse('user_list')
    context = {'users': users, 'next': next_url, 'title': _('صفحة الكتاب')}
    return render(request, 'home/users_list.html', context)


@login_required()
def user_page(request, username, form=None):
    form = form or PostForm()
    req_user = get_object_or_404(User, username=username)
    posts_list = Post.objects.select_related().filter(user=req_user)

    paginator = Paginator(posts_list, constants.PER_PAGE)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    next_url = reverse('user_page', args=(req_user.username,))
    context = {'req_user': req_user, 'posts': posts, 'title': _(' صفحة المستخدم ' + req_user.username),
               'post_form': form, 'next': next_url}
    return render(request, 'home/user_page.html', context)


@login_required()
def follows_list(request):
    user = request.user
    req_user = user
    followings_list = user.userprofile.follows.select_related().all()
    paginator = Paginator(followings_list, constants.PER_PAGE)
    page = request.GET.get('page')

    try:
        follows = paginator.page(page)
    except PageNotAnInteger:
        follows = paginator.page(1)
    except EmptyPage:
        follows = paginator.page(paginator.num_pages)
    next_url = reverse('followings')
    context = {'user_profiles': follows, 'title': _('اصدقاء'), 'user': user, 'req_user': req_user, 'next': next_url}
    return render(request, 'home/follows_list.html', context)


@login_required()
def followed_by_list(request):
    user = request.user
    req_user = user
    followers_list = user.userprofile.followed_by.select_related().all()
    paginator = Paginator(followers_list, constants.PER_PAGE)
    page = request.GET.get('page')

    try:
        followed_by = paginator.page(page)
    except PageNotAnInteger:
        followed_by = paginator.page(1)
    except EmptyPage:
        followed_by = paginator.page(paginator.num_pages)
    next_url = reverse('followers')
    context = {'user_profiles': followed_by, 'title': _('متابعين'), 'user': user, 'req_user': req_user,
               'next': next_url}
    return render(request, 'home/followed_by_list.html', context)


def tag_page(request, tag_name):
    form = PostForm()
    posts_list = Post.objects.select_related().filter(tags__name__in=[tag_name])
    title = _('القسم') + ": " + tag_name

    paginator = Paginator(posts_list, constants.PER_PAGE)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'post_form': form, 'title': title}
    return render(request, 'home/tag.html', context)


@login_required()
def follow(request, username):
    user = request.user
    follow_user = User.objects.get(username=username)
    user.userprofile.follows.add(follow_user.userprofile)
    next_url = request.POST.get('next', 'home:index')
    return redirect(next_url)


@login_required()
def unfollow(request, username):
    user = request.user
    unfollow_user = User.objects.get(username=username)
    user.userprofile.follows.remove(unfollow_user)
    next_url = request.POST.get('next', 'home:index')
    return redirect(next_url)


@login_required()
def rate_up(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        success = "false"

        if request.user not in post.rated_by.all():
            post.ratings += 1
            post.rated_by.add(request.user)
            post.save()
            success = "success"

        if request.is_ajax():
            return HttpResponse(success)
        else:
            next_url = request.POST.get('next')
            if len(next_url) > 0:
                return redirect(next_url)
            else:
                return redirect('home:index')
    return redirect('home:index')


@login_required()
def rate_down(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        success = "false"

        if request.user not in post.rated_by.all():
            post.ratings -= 1
            post.rated_by.add(request.user)
            post.save()
            success = "success"

        if request.is_ajax():
            return HttpResponse(success)
        else:
            next_url = request.POST.get('next')
            if len(next_url) > 0:
                return redirect(next_url)
            else:
                return redirect('home:index')

    return redirect('home:index')
