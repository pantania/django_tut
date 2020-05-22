from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Account, Profile
from django.utils import timezone
from .forms import PostForm, AccountForm
from django.contrib.auth.decorators import login_required
from push_notifications.models import GCMDevice


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":  # 새 글이 추가(저장)되어야 함 i.e. 저장이 클릭되었을때
        form = AccountForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:  # 처음 페이지에 접속했을때
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


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


@login_required
def notify_user(request, ):
    account = get_object_or_404(Account, pk=pk)
    # device = GCMDevice.objects.get(registration_id=fcm_reg_id)
    devices = GCMDevice.objects.filter(account__alert=True).filter(account__started=True)
    devices.send_message("Notification sent")


@login_required
def account_list(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            profile.accounts.add(account)
            
            return redirect('account_list')
    else:
        form = AccountForm()
    accounts = request.user.profile.accounts
    return render(request, 'account/account_list.html', {'form': form, 'accounts': accounts})
