from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from django.http import HttpResponse
from .models import User, Post, Comment, Like, Notification, NotificationType
from .forms import PostForm, CommentForm, UserForm


# TODO seem not seen, editable own post 

current_user = get_object_or_404(User, pk=2)


def notifications(req):
    no = Notification.objects.filter(user=current_user)
    return render(req, 'app/notifications.html', {'current_user': current_user, 'notifications': no})


def profile(req, user_id):

    user = get_object_or_404(User, pk=user_id)
    owner = False
    following = False
    if current_user == user:
        owner = True

    if current_user.following.filter(id__icontains=user_id):
        following = True

    liked = [i for i in Post.objects.all() if Like.objects.filter(
        user=current_user, post=i)]

    return render(req, 'app/profile.html', {'user': user, 'owner': owner, 'following': following, 'liked': liked, 'current_user': current_user,})


def profile_edit(req):
    if req.method == 'POST':
        form = UserForm(req.POST, req.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{current_user.id}')
    else:
        form = UserForm(instance=current_user)
    return render(req, 'app/profile_edit.html', {'form': form, 'current_user' : current_user})


def home_feed(req):

    posts = Post.objects.filter(Q(user__in=current_user.following.all()) | Q(user=current_user)).order_by('-created_at')
    liked = [i for i in Post.objects.all() if Like.objects.filter(
        user=current_user, post=i)]
    return render(req, 'app/home.html', {'current_user': current_user, 'posts': posts, 'liked': liked})


def create_post(req):
    if req.method == 'POST':
        form = PostForm(req.POST, req.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = current_user
            form.save()
            return redirect('/')

    else:
        form = PostForm()
    return render(req, 'app/create.html', {'form': form, 'current_user' : current_user})


def comment(req, post_id):
    if req.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        c = Comment(text=req.POST['comment'], post=post, user=current_user)
        c.save()
        createNotification(post.user, current_user, NotificationType.COMMENT, post, c)

    return redirect('/')


def like(req, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = Like(user=current_user, post=post)
    like.save()

    createNotification(post.user, current_user, NotificationType.LIKE, post, like=like)

    return HttpResponse()


def unlike(req, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = Like.objects.filter(post=post, user=current_user)
    like.delete()

    return HttpResponse()


def livesearch(req, word, sid1, sid2):
    users = User.objects.filter(
        Q(username__icontains=word) | Q(email__icontains=word))

    if len(users) > 0:
        response = ''
        for u in users:
            response += '<a class="list-group-item list-group-item-action" href="' + \
                reverse('profile', args=(u.id,)) + f'">@{u.username}</a><br/>'
    else:
        response = '<span class="list-group-item">no suggestion<span/>'

    return HttpResponse(response)


def createNotification(user, inicializer, n_type, post=None, comment=None, like=None):
    n = Notification(user=user, inicializer=inicializer,
                     notification_type=n_type, post=post, comment=comment, like=like)
    n.save()


def follow(req, user_id):
    user_to_follow = get_object_or_404(User, pk=user_id)

    current_user.following.add(user_to_follow)
    response = "OK"
    createNotification(user_to_follow, current_user, NotificationType.FOLLOW)

    return HttpResponse(response)


def unfollow(req, user_id):
    user_to_unfollow = get_object_or_404(User, pk=user_id)
    current_user.following.remove(user_to_unfollow)
    response = "OK"

    return HttpResponse(response)
